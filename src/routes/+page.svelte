<script>
  import { onMount, tick } from "svelte";
  import photos_data from "$lib/assets/photos.json?raw";
  import grand_ol_photos_data from "$lib/assets/grand_ol_photos.txt?raw";
  import ProjectCard from "$lib/ProjectCard.svelte";

  const birthday = new Date("2010-02-01");
  const today = new Date();
  const age = Math.floor((today.getTime() - birthday.getTime()) / (1000 * 60 * 60 * 24 * 365)); // 1000 ms -> s, 60s -> min, 60 min -> hr -> 24 hr -> day, 365 days -> year

  let photos = JSON.parse(photos_data);

  const numPerPage = 9;
  let numPages = Math.ceil(photos.length / numPerPage);
  let currentPage = $state(1);
  let selected_photos = $state(photos.slice(0, numPerPage));

  const grand_ol_photos_links = grand_ol_photos_data.split("\n").filter((link) => link.trim() !== "");
</script>

<!-- hi aria im hidden. hi hidden im dad -->
<div class="bg-grid" aria-hidden="true">
  {#each Array(4).fill(grand_ol_photos_links).flat() as src}
    <img {src} alt="" class="bg-photo" loading="lazy" />
  {/each}
</div>

<div class="main">
  <nav>
    <img src="https://avatars.githubusercontent.com/u/81335306?v=4" alt="favicon" width="30%" />
    <div class="card" id="heading-card">
      <h1 class="my-freaking-name">hi, i'm aji!</h1>
      <p class="desc">i'm a <span id="age">{age}</span>-year-old from new york! i like coding & photography.</p>
      <!-- <p><a role="button" href="https://github.com/tiredkangaroo" class="card-button">github</a></p> -->
    </div>
  </nav>
  <h1 class="section-heading">projects</h1>
  <div class="projects">
    <ProjectCard
      title="mechanical dinosaurs"
      screenshot_url="https://user-cdn.hackclub-assets.com/019f8c90-2179-7b13-a541-f6955e07ec66/Screenshot%202026-07-22%20at%206.21.12%C3%A2%C2%80%C2%AFPM.png"
      github_repo="tiredkangaroo/mechanicaldinosaurs"
      override_desc=""
    ></ProjectCard>
    <ProjectCard
      title="lights out!"
      github_repo="Xtrrae/switch-defense"
      override_desc="turn off all the lights before they get to you! controller: a set of four light switches. made in godot with two others & won campfire flagship!"
      screenshot_url="https://user-cdn.hackclub-assets.com/01a09cb4-98ac-789e-8e01-8fa8b6653819/Screenshot%202026-09-13%20at%205.35.21%E2%80%AFPM.jpg"
    ></ProjectCard>
  </div>
  <h1 class="section-heading">photography</h1>
  <div class="photos" id="photos-grid">
    {#each selected_photos as photo, index}
      <img
        src={photo.url}
        alt={photo.description}
        class="photo"
        onclick={window.location.assign(`/photo?id=${index}`)}
      />
    {/each}
  </div>
  <div class="pagination">
    {#each Array(numPages) as _, pageIndex}
      <button
        onclick={() => {
          currentPage = pageIndex + 1;
          const startIndex = (currentPage - 1) * numPerPage;
          const endIndex = startIndex + numPerPage;
          selected_photos = photos.slice(startIndex, endIndex);
          console.log("selecting", startIndex, "to", endIndex, "photos:", selected_photos);
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
  .bg-grid {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: 0; /* Keep it behind main content */
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    grid-auto-rows: 140px;
    gap: 8px;
    overflow: hidden;
    pointer-events: none; /* Allows scrolling/clicking through the grid */
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
  }

  .bg-photo:hover {
    opacity: 1;
    transform: scale(1.08);
    z-index: 2;
  }

  /* Ensure .main is layered correctly above the background grid */
  .main {
    position: relative;
    z-index: 10;
    background-color: rgba(255, 255, 255, 0.92);
    padding: 1.5rem;
    border-radius: 8px;
  }
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
  .photo {
    width: 100%;
    display: block;
    margin-bottom: 1rem;
    break-inside: avoid; /* Prevents an image from getting split across columns */
    cursor: pointer;
  }
  .photo:nth-of-type(3n + 1) {
    order: 1;
  }
  .photo:nth-of-type(3n + 2) {
    order: 2;
  }
  .photo:nth-of-type(3n) {
    order: 3;
  }
  .photos::before,
  .photos::after {
    content: "";
    flex-basis: 100%;
    width: 0;
    order: 2;
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
    .photo:nth-of-type(3n + 1) {
      order: 1;
    }
    .photo:nth-of-type(3n + 2) {
      order: 1;
    }
    .photo:nth-of-type(3n + 3) {
      order: 1;
    }
    .photo:nth-of-type(3n) {
      order: 1;
    }
  }
</style>
