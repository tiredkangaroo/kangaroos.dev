<script>
  import { onMount } from "svelte";
  import photos_data from "$lib/assets/photos.json?raw";

  const birthday = new Date("2010-02-01");
  const today = new Date();
  const age = Math.floor((today.getTime() - birthday.getTime()) / (1000 * 60 * 60 * 24 * 365)); // 1000 ms -> s, 60s -> min, 60 min -> hr -> 24 hr -> day, 365 days -> year

  let photos = JSON.parse(photos_data);

  // returns the hieghit of the tallest column in the grid in px
  function calculateGridHeight() {
    const items = Array.from(document.getElementsByClassName("photo"));
    const columnHeights = [0, 0, 0]; // 3 per column; i should make this a const

    items.forEach((item, index) => {
      // get the full height (including margins) of the item
      const style = window.getComputedStyle(item);
      const marginTop = parseFloat(style.marginTop) || 0;
      const marginBottom = parseFloat(style.marginBottom) || 0;
      const totalItemHeight = item.getBoundingClientRect().height + marginTop + marginBottom;

      const order = parseInt(style.order) || 1;
      const columnIndex = (order - 1) % 3;
      columnHeights[columnIndex] += totalItemHeight; // set the height of the column to the total height of the items in that column
    });

    const maxHeight = Math.max(...columnHeights);
    return maxHeight;
  }

  onMount(() => {
    const grid = document.getElementById("photos-grid");
    if (grid) {
      const gridHeight = calculateGridHeight();
      grid.style.height = `${gridHeight}px`;
    }
    window.addEventListener("resize", () => {
      if (grid) {
        const gridHeight = calculateGridHeight();
        grid.style.height = `${gridHeight}px`;
      }
    });
    return () => {
      window.removeEventListener("resize", calculateGridHeight);
    };
  });
</script>

<div class="main">
  <nav>
    <div class="card">
      <h1 class="my-freaking-name">hi, i'm aji!</h1>
      <p class="desc">i'm a <span id="age">{age}</span>-year-old from new york!</p>
      <p><a role="button" href="https://github.com/tiredkangaroo" class="card-button">github</a></p>
    </div>
  </nav>
  <h1>photography</h1>
  <div class="photos" id="photos-grid">
    {#each photos as photo, index}
      <img
        src={photo.url}
        alt={photo.description}
        class="photo"
        onclick={window.location.assign(`/photo?id=${index}`)}
      />
    {/each}
  </div>
</div>

<style>
  nav {
    width: 100%;
  }
  .my-freaking-name {
    font-size: 4rem;
    font-weight: bold;
    color: var(--card-border);
    line-height: 1.7;
    margin: 0;
  }
  .photos {
    display: grid;
    grid-template-columns: masonry;
    grid-template-rows: masonry;
  }
  /* https://tobiasahlin.com/blog/masonry-with-css/ */
  .photos {
    display: flex;
    flex-flow: column wrap;
    height: 1200px;
  }
  .photo {
    width: 33%;
    position: relative;
    margin-bottom: 2%;
    box-sizing: border-box;
    cursor: pointer;
  }
  .photo:nth-of-type(3n + 1) {
    order: 1;
  }
  .photo:nth-of-type(3n + 2) {
    order: 2;
  }
  .photo:nth-of-type(3n + 3) {
    order: 3;
  }
  .photo:nth-of-type(3n) {
    order: 4;
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
    align-items: center;
  }
  @media (max-width: 1000px) {
    .main {
      width: 90%;
    }
  }
</style>
