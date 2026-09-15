<script lang="ts">
  import photos_data from "$lib/assets/photos.json?raw";
  import type { Photo } from "$lib/types";

  let photos = JSON.parse<Array<Photo>>(photos_data);
  let photo = $state(null);
  try {
    const id = new URLSearchParams(window.location.search).get("id");
    if (id === null) {
      throw new Error("No id provided"); // just to make it go to the catch block
    }
    photo = photos[parseInt(id)];
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
    <img src={photo.url} alt={photo.description} class="photo" />
    <div class="photo-info">
      <p class="photo-description">{photo.description}</p>
      <p class="photo-date">{photo.date ? normalDate(photo.date) : ""}</p>
      <p class="photo-location">{photo.location}</p>
    </div>
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
  .photo {
    max-width: 90%;
    max-height: 80%;
    object-fit: contain;
  }
  .photo-info {
    margin-top: 1rem;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.5rem;
  }
  .photo-info p {
    margin: 0;
  }
  .photo-description {
    font-size: 2rem;
    font-weight: bold;
    margin-top: 1rem;
  }
</style>
