<script>
  import { onMount } from "svelte";
  import grand_ol_photos_data from "$lib/assets/grand_ol_photos.txt?raw";

  // Parse into an array of objects containing both original url and local image path
  const bg_photos = grand_ol_photos_data
    .split("\n")
    .map((url) => url.trim())
    .filter((url) => url !== "")
    .map((originalUrl) => ({
      href: originalUrl,
      src: "/bg/" + originalUrl.slice(originalUrl.lastIndexOf("/") + 1).replace(/\.[^.]+$/, ".webp"),
    }));

  const tile_min = 180;
  const tile_row = 140;
  const tile_gap = 8;
  const default_tiles = 200;

  let num_tiles = $state(default_tiles);
  let bg_tiles = $derived(Array.from({ length: num_tiles }, (_, i) => bg_photos[i % bg_photos.length]));

  onMount(() => {
    const grid = document.getElementById("bg-grid-full");
    if (!grid) return;

    let frame = 0;
    const fit = () => {
      const cols = Math.max(1, Math.floor((grid.clientWidth + tile_gap) / (tile_min + tile_gap)));
      const rows = Math.ceil((grid.clientHeight + tile_gap) / (tile_row + tile_gap));
      const needed = cols * rows;
      if (needed > num_tiles) num_tiles = needed;
    };

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

<div class="bg-grid-full" id="bg-grid-full" aria-hidden="true">
  {#each bg_tiles as { href, src }}
    <a {href} target="_blank" rel="noopener noreferrer">
      <img {src} alt="" class="bg-photo" decoding="async" fetchpriority="low" />
    </a>
  {/each}
</div>

<style>
  .bg-grid-full {
    position: absolute;
    inset: 0;
    width: 100%;
    min-height: 100vh;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    grid-auto-rows: 140px;
    gap: 8px;
    overflow: visible;
    pointer-events: none;
    contain: layout paint;
  }

  .bg-photo {
    width: 100%;
    height: 100%;
    /* opacity: 0.6; */
    filter: grayscale(100%);
    object-fit: cover;
    display: block;
    transition:
      transform 0.2s ease,
      opacity 0.2s ease;
    pointer-events: auto;
    will-change: transform, opacity;
  }

  .bg-photo:hover {
    opacity: 1;
    transform: scale(1.08);
    filter: grayscale(0%);
  }
</style>
