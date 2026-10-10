<script>
  import { onMount } from "svelte";
  import photos from "$lib/assets/photos.json";
  import grand_ol_photos_data from "$lib/assets/grand_ol_photos.txt?raw";
  import ProjectCard from "$lib/ProjectCard.svelte";
  import pfp from "$lib/assets/pfp.png";

  const birthday = new Date("2010-02-01");
  const today = new Date();
  const age = Math.floor((today.getTime() - birthday.getTime()) / (1000 * 60 * 60 * 24 * 365)); // 1000 ms -> s, 60s -> min, 60 min -> hr -> 24 hr -> day, 365 days -> year

  const numPerPage = 9;
  const numPages = Math.ceil(photos.length / numPerPage);
  let currentPage = $state(1);
  let startIndex = $derived((currentPage - 1) * numPerPage);
  let selected_photos = $derived(photos.slice(startIndex, startIndex + numPerPage));

  // Background tiles are local thumbnails; the originals are 1-16 MB each.
  const bg_photos = grand_ol_photos_data
    .split("\n")
    .map((url) => url.trim())
    .filter((url) => url !== "")
    .map((url) => "/bg/" + url.slice(url.lastIndexOf("/") + 1).replace(/\.[^.]+$/, ".webp"));

  // The grid repeats the photos until it covers the viewport. Its metrics have to
  // stay in sync with .bg-grid in the stylesheet below.
  const tile_min = 180;
  const tile_row = 140;
  const tile_gap = 8;
  // Enough tiles for a common laptop screen, so the prerendered html already has a
  // full grid and hydration only ever adds the couple of tiles a bigger screen needs.
  const default_tiles = 49;

  let num_tiles = $state(default_tiles);
  // Unkeyed on purpose: the photos cycle, so `src` repeats and a key would be a lie.
  let bg_tiles = $derived(Array.from({ length: num_tiles }, (_, i) => bg_photos[i % bg_photos.length]));

  onMount(() => {
    const grid = document.getElementById("bg-grid");
    if (!grid) return;

    let frame = 0;
    const fit = () => {
      // Mirrors `repeat(auto-fill, minmax(180px, 1fr))` over 140px rows, so we
      // render exactly the tiles the grid can actually show and no more.
      const cols = Math.max(1, Math.floor((grid.clientWidth + tile_gap) / (tile_min + tile_gap)));
      const rows = Math.ceil((grid.clientHeight + tile_gap) / (tile_row + tile_gap));
      const needed = cols * rows;
      if (needed !== num_tiles) num_tiles = needed;
    };

    // Fires once on observe, which covers the initial fit. Resizes are coalesced
    // into one pass per frame because they arrive in bursts while a window drags.
    const observer = new ResizeObserver(() => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(fit);
    });
    observer.observe(grid);

    return () => {
      observer.disconnect();
      cancelAnimationFrame(frame);
    };
  });
</script>

<!-- hi aria im hidden. hi hidden im dad -->
<div class="bg-grid" id="bg-grid" aria-hidden="true">
  {#each bg_tiles as src}
    <img {src} alt="" class="bg-photo" decoding="async" fetchpriority="low" />
  {/each}
</div>

<div class="main">
  <nav>
    <img src={pfp} alt="favicon" width="30%" height="30%" decoding="async" />
    <div class="card" id="heading-card">
      <h1 class="my-freaking-name">hi, i'm aji!</h1>
      <p class="desc">i'm a <span id="age">{age}</span>-year-old from new york! i like coding & photography.</p>
      <p><a href="/photoboard" class="card-button">go to photoboard</a></p>
    </div>
  </nav>
  <h1 class="section-heading">projects</h1>
  <div class="projects">
    <ProjectCard
      title="mechanical dinosaurs"
      screenshot_url="https://user-cdn.hackclub-assets.com/019f8c90-2179-7b13-a541-f6955e07ec66/Screenshot%202026-07-22%20at%206.21.12%C3%A2%C2%80%C2%AFPM.png"
      screenshot_size={[2286, 1732]}
      github_repo="tiredkangaroo/mechanicaldinosaurs"
      desc="my personal infra manager. machines, vms, deployments and automations! made with go and django"
    ></ProjectCard>
    <ProjectCard
      title="lights out!"
      github_repo="Xtrrae/switch-defense"
      desc="turn off all the lights before they get to you! controller: a set of four light switches. made in godot with two others & won campfire flagship!"
      screenshot_url="https://user-cdn.hackclub-assets.com/01a09cb4-98ac-789e-8e01-8fa8b6653819/Screenshot%202026-09-13%20at%205.35.21%E2%80%AFPM.jpg"
      screenshot_size={[2422, 1628]}
    ></ProjectCard>
    <ProjectCard
      title="swirl"
      github_repo="hackclub/swirl"
      desc="a jekyll website for a hack club YSWS! made and maintained by dhyan & aj."
      screenshot_url="https://cdn.hackclub.com/01a10d32-8ec3-7043-8cd4-e0c0a580aebe/screenshot_2026-10-05_at_1.52.34___pm.png"
      screenshot_size={[1920, 1080]}
    ></ProjectCard>
    <ProjectCard
      title="cap"
      github_repo="tiredkangaroo/cap"
      desc="proxy server that allows you to inspect, block, and modify http traffic; made in go and react - also my first hack club ship!"
      screenshot_url="https://raw.githubusercontent.com/tiredkangaroo/cap/refs/heads/main/screenshots/1.png"
      screenshot_size={[1920, 1080]}
    ></ProjectCard>
    <ProjectCard
      title="music"
      github_repo="tiredkangaroo/music"
      desc="music downloader & player app; made in go and react"
      screenshot_url="https://cdn.hackclub.com/01a10ea8-c813-7682-bb3a-6c67f1a7c0a6/image.png"
      screenshot_size={[1920, 1080]}
    ></ProjectCard>
  </div>
  <h1 class="section-heading">photography</h1>
  <p>to be updated!</p>
  <div class="photos" id="photos-grid">
    {#each selected_photos as photo, index (photo.url)}
      <a class="photo" href={`/photo?id=${startIndex + index}`}>
        <!-- column-count fills top to bottom, so the first three are the ones
             sitting in the viewport on load. -->
        <img
          src={photo.thumb}
          alt={photo.description}
          width={photo.w}
          height={photo.h}
          loading={index < 3 ? "eager" : "lazy"}
          fetchpriority={index === 0 ? "high" : "auto"}
          decoding="async"
        />
      </a>
    {/each}
  </div>
  <div class="pagination">
    {#each Array(numPages) as _, pageIndex}
      <button
        aria-current={pageIndex + 1 === currentPage ? "page" : undefined}
        onclick={() => {
          currentPage = pageIndex + 1;
        }}
      >
        {pageIndex + 1}
      </button>
    {/each}
  </div>
  <h1 class="section-heading">contact & socials</h1>
  <ul>
    <li>
      <b>github:</b> <a href="https://github.com/tiredkangaroo" target="_blank">tiredkangaroo</a>
    </li>
    <li>
      <b>email:</b> <a href="mailto:aji@kangaroos.dev">aji@kangaroos.dev</a>
    </li>
    <li>
      <b>hack club:</b> <a href="https://hackclub.slack.com/team/U08RH4J9WQ5" target="_blank">slack</a>
    </li>
  </ul>
</div>

<style>
  nav {
    display: flex;
    flex-direction: row;
    gap: 1rem;
    width: 100%;
  }

  /* begin mostly ai code */
  .bg-grid {
    position: fixed;
    /* Same box as `width: 100vw; height: 100vh`, minus the scrollbar overflow. */
    inset: 0;
    z-index: 0; /* Keep it behind main content */
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    grid-auto-rows: 140px;
    gap: 8px;
    overflow: hidden;
    pointer-events: none; /* Allows scrolling/clicking through the grid */
    /* Makes the grid its own invalidation root, so a tile repainting can't drag
       the translucent .main above it into the repaint. */
    contain: layout paint;
  }

  .bg-photo {
    width: 100%;
    height: 100%;
    opacity: 0.25;
    object-fit: cover;
    display: block;
    transition:
      transform 0.2s ease,
      opacity 0.2s ease;
    pointer-events: auto; /* Re-enables hover effects on the background photos */
    /* Own compositor layer, built once at load. Without this the layer is created
       and torn down around every hover, and that churn is what made hovering lag;
       it also keeps the 200ms opacity/scale animation off the main thread. */
    will-change: transform, opacity;
  }

  /* No z-index bump here: changing it repaints the whole fixed grid (and the
     translucent .main above it) on every hover, which reads as lag. The scale
     is enough to make the hovered tile stand out. */
  .bg-photo:hover {
    opacity: 1;
    transform: scale(1.08);
  }

  /* Ensure .main is layered correctly above the background grid */
  .main {
    position: relative;
    z-index: 10;
    background-color: rgba(255, 255, 255, 0.92);
    padding: 1.5rem;
    border-radius: 8px;
  }
  /* end ai code */
  .projects {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
  }
  #heading-card {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
  }
  .section-heading {
    background-color: var(--card-bg);
    color: var(--card-border);
    padding: 0.4rem 1rem;
  }
  .section-heading {
    font-size: 1.5rem;
  }
  .my-freaking-name {
    font-size: 4rem;
    font-weight: bold;
    color: var(--card-border);
    line-height: 1.7;
    margin: 0;
  }
  /* https://tobiasahlin.com/blog/masonry-with-css/ */
  .photos {
    column-count: 3;
    column-gap: 1rem;
  }
  .pagination {
    display: flex;
    justify-content: center;
    margin-top: 1rem;
    gap: 0.5rem;
  }
  /* The anchor is the masonry item so it can carry break-inside/margins; the
     intrinsic width/height on the img reserve space before it loads. */
  .photo {
    display: block;
    width: 100%;
    margin-bottom: 1rem;
    break-inside: avoid; /* Prevents an image from getting split across columns */
    cursor: pointer;
    text-decoration: none;
    color: inherit;
  }
  .photo img {
    width: 100%;
    height: auto;
    display: block;
  }
  .desc {
    font-size: 1.5rem;
  }
  .card {
    background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    color: var(--card-border);
    padding: 0.4rem 1rem;
  }
  .card-button {
    background-color: var(--card-border);
    text-decoration: none;
    color: white;
    padding: 0.4rem 1rem;
  }
  .main {
    display: flex;
    flex-direction: column;
    width: 50%;
    height: 100%;
    margin: 20px auto;
    pointer-events: none;
    /* background-color: #abfff9; */
    /* padding: 1rem; */
    /* align-items: center; */
  }
  .main nav,
  .main .projects,
  .main .photos,
  .main .pagination,
  .main ul,
  .main a,
  .main button {
    pointer-events: auto;
  }
  @media (max-width: 1000px) {
    .main {
      width: 90%;
    }
  }
  @media (max-width: 700px) {
    .projects {
      grid-template-columns: 1fr;
    }
    .photos {
      column-count: 2;
    }
  }
  @media (max-width: 500px) {
    .photos {
      column-count: 1;
      column-gap: 1rem;
      display: flex;
      flex-direction: column;
    }
    .photo {
      width: 100%;
    }
  }
</style>
