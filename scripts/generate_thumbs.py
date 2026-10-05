#!/usr/bin/env python3
"""Download the photo originals and cut down local thumbnails for them.

The originals on media.kangaroos.dev are full-resolution camera files (some are
over 16 MB), which is far more data than the site needs: background grid tiles
render at ~180x140 css px and gallery tiles at ~300 css px wide.

Run this after adding a photo to photos.json or a url to grand_ol_photos.txt:

    python3 scripts/generate_thumbs.py

Originals are cached in .thumb-cache/ so re-runs are cheap. Thumbnails are
written to static/bg/ and static/photos/, and photos.json is updated with the
thumbnail path and intrinsic size so the markup can reserve layout space.
"""

import json
import pathlib
import shutil
import struct
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

ROOT = pathlib.Path(__file__).resolve().parent.parent
CACHE = ROOT / ".thumb-cache"
PHOTOS_JSON = ROOT / "src/lib/assets/photos.json"
BG_URLS = ROOT / "src/lib/assets/grand_ol_photos.txt"
BASE = "https://media.kangaroos.dev/"

# Sized for 2x displays: bg tiles are ~180px css wide, gallery tiles ~320px css wide,
# and the photo page shows an image up to ~1700px css wide.
BG_WIDTH, BG_QUALITY = 360, 60
GALLERY_WIDTH, GALLERY_QUALITY = 640, 72
LARGE_WIDTH, LARGE_QUALITY = 1600, 76


def dims(path):
    out = subprocess.run(
        ["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    values = {}
    for line in out.splitlines():
        key, _, value = line.partition(":")
        if key.strip() in ("pixelWidth", "pixelHeight"):
            values[key.strip()] = int(value)
    return values["pixelWidth"], values["pixelHeight"]


def download(url, dest):
    """Cache the original at dest. Returns True on success."""
    if dest.exists() and dest.stat().st_size > 0:
        return True
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "curl/8.7.1"})
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            dest.write_bytes(resp.read())
    except Exception as exc:
        print(f"  FAILED {url}: {exc}", file=sys.stderr)
        return False
    return True


def exif_orientation(path):
    """Read the EXIF orientation tag (1-8) straight out of the JPEG APP1 segment.

    Browsers apply this tag when displaying a photo, but neither sips nor cwebp
    does, so anything we generate from the raw pixels has to be rotated to match.
    """
    blob = path.read_bytes()
    start = blob.find(b"Exif\x00\x00")
    if start < 0:
        return None
    tiff = start + 6
    endian = ">" if blob[tiff:tiff + 2] == b"MM" else "<"
    (ifd,) = struct.unpack(endian + "I", blob[tiff + 4:tiff + 8])
    node = tiff + ifd
    (count,) = struct.unpack(endian + "H", blob[node:node + 2])
    for i in range(count):
        entry = node + 2 + i * 12
        tag = struct.unpack(endian + "H", blob[entry:entry + 2])[0]
        if tag == 0x0112:
            return struct.unpack(endian + "H", blob[entry + 8:entry + 10])[0]
    return None


# EXIF orientation -> clockwise rotation needed to display it upright.
ROTATIONS = {1: 0, 3: 180, 6: 90, 8: 270}


def upright(src):
    """Return a path to src rotated upright, plus its displayed (w, h).

    sips can rotate but not mirror, so a mirrored orientation is an error rather
    than a silently wrong thumbnail.
    """
    orientation = exif_orientation(src)
    if orientation in (None, 1):
        return src, dims(src)
    if orientation not in ROTATIONS:
        raise SystemExit(
            f"{src.name}: EXIF orientation {orientation} is mirrored, which sips "
            f"cannot correct. Rotate the original and re-run."
        )
    turned = CACHE / "rotated" / f"{src.stem}.rot{ROTATIONS[orientation]}.jpg"
    if not turned.exists():
        turned.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(src, turned)
        subprocess.run(
            ["sips", "-r", str(ROTATIONS[orientation]), str(turned)],
            check=True, capture_output=True,
        )
    return turned, dims(turned)


def make_thumb(src, dest, width, quality):
    """Write a webp thumbnail of src at dest. Returns its actual (width, height)."""
    src, (src_w, _) = upright(src)
    if src_w <= width:
        return dims(src)
    dest.parent.mkdir(parents=True, exist_ok=True)
    # -resize <width> 0 keeps the aspect ratio; read the result back so the size
    # recorded in photos.json is exactly what shipped.
    subprocess.run(
        ["cwebp", "-quiet", "-q", str(quality), "-resize", str(width), "0",
         "-m", "4", "-o", str(dest), str(src)],
        check=True,
    )
    return dims(dest)


def absolute(url):
    return url if url.startswith(("http://", "https://")) else BASE + url


def stem(url):
    return url.rsplit("/", 1)[-1].rsplit(".", 1)[0]


def basename(url):
    return url.rsplit("/", 1)[-1]


def main():
    photos = json.loads(PHOTOS_JSON.read_text())
    bg_urls = [line.strip() for line in BG_URLS.read_text().splitlines() if line.strip()]

    # (cache subdir, url, output path, width, quality) for every variant we ship.
    jobs = [("bg", u, ROOT / "static/bg" / (stem(u) + ".webp"), BG_WIDTH, BG_QUALITY)
            for u in bg_urls]
    for photo in photos:
        url = photo["url"]
        jobs.append(("gallery", url, ROOT / "static/photos" / (stem(url) + ".webp"),
                     GALLERY_WIDTH, GALLERY_QUALITY))
        jobs.append(("gallery", url, ROOT / "static/photos/lg" / (stem(url) + ".webp"),
                     LARGE_WIDTH, LARGE_QUALITY))

    # Keep the extension in the cache path so the cached files stay recognisable.
    jobs = [(kind, absolute(url), CACHE / kind / basename(url), dest, w, q)
            for kind, url, dest, w, q in jobs]

    originals = sorted({(kind, url) for kind, url, _, _, _, _ in jobs})
    print(f"fetching {len(originals)} originals...")
    with ThreadPoolExecutor(max_workers=8) as pool:
        ok = list(pool.map(lambda o: download(o[1], CACHE / o[0] / basename(o[1])), originals))
    if not all(ok):
        print("some originals could not be fetched; not regenerating.", file=sys.stderr)
        return 1

    print(f"encoding {len(jobs)} thumbnails...")
    with ThreadPoolExecutor(max_workers=8) as pool:
        sizes = list(pool.map(lambda j: make_thumb(j[2], j[3], j[4], j[5]), jobs))
    # Keyed by output path so the grid size wins over the larger variants.
    size_by_dest = {dest: size for (_, _, _, dest, _, _), size in zip(jobs, sizes)}

    for photo in photos:
        grid = ROOT / "static" / ("photos/" + stem(photo["url"]) + ".webp")
        photo["thumb"] = "/photos/" + stem(photo["url"]) + ".webp"
        photo["large"] = "/photos/lg/" + stem(photo["url"]) + ".webp"
        photo["w"], photo["h"] = size_by_dest[grid]

    PHOTOS_JSON.write_text(json.dumps(photos, indent=2) + "\n")

    for kind in ("bg", "photos", "photos/lg"):
        files = sorted((ROOT / "static" / kind).glob("*.webp"))
        total = sum(f.stat().st_size for f in files)
        print(f"static/{kind:<10} {len(files):>3} files, {total / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())