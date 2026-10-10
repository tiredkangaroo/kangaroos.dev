<script lang="ts">
  import photos from "$lib/assets/photos.json";
  import type { Photo } from "$lib/types";

  const all_photos = photos as Photo[];
  let photo = $state<Photo | undefined>(undefined);
  try {
    const id = Number.parseInt(new URLSearchParams(window.location.search).get("id") ?? "", 10);
    // An id outside the list would otherwise render an empty page.
    const match = Number.isInteger(id) ? all_photos[id] : undefined;
    if (match === undefined) {
      throw new Error("No such photo"); // just to make it go to the catch block
    }
    photo = match;
  } catch (e) {
    window.location.replace("/");
  }

  function normalDate(dateString: string): string {
    const date = new Date(dateString);
    const options: Intl.DateTimeFormatOptions = {
      year: "numeric",
      month: "long",
      day: "numeric",
    };
    return date.toLocaleDateString(undefined, options);
  }
</script>

{#if photo}
  <div class="page">
    <!-- The local render keeps this page from pulling a 10-16 MB original;
         the image still links through to the full resolution file. -->
    <a href={photo.url} target="_blank" rel="noopener noreferrer" class="photo-link">
      <!-- `large` and `thumb` are the same crop at different widths, so the
           thumb's intrinsic ratio reserves the right box before the 190 KB
           render decodes. Without it the whole page reflows on load. -->
      <img
        src={photo.large}
        alt={photo.description}
        class="photo"
        decoding="async"
        style="aspect-ratio: {photo.w} / {photo.h}"
      />
    </a>
  </div>
{/if}

<style>
  .page {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    height: 100vh;
  }
  .photo-link {
    display: block;
    line-height: 0;
  }
  .photo {
    max-width: 90vw;
    max-height: 90vh;
  }
</style>
