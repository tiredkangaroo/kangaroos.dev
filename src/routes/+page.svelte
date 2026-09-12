<script>
  import photos_urls from "$lib/assets/photos_urls.txt?raw";

  const birthday = new Date("2010-02-01");
  const today = new Date();
  const age = Math.floor((today.getTime() - birthday.getTime()) / (1000 * 60 * 60 * 24 * 365)); // 1000 ms -> s, 60s -> min, 60 min -> hr -> 24 hr -> day, 365 days -> year

  let photos = photos_urls.split("\n").filter((url) => url.trim() !== ""); // grab out all the urls and filter out empty lines
</script>

<div class="main">
  <nav>
    <!-- <div class="card"> -->
    <div class="card">
      <h1 class="my-freaking-name">hi, i'm aji!</h1>
      <p class="desc">i'm a <span id="age">{age}</span>-year-old from new york!</p>
      <p><a role="button" href="https://github.com/tiredkangaroo" class="card-button">github</a></p>
    </div>
    <!-- </div> -->
    <div></div>
  </nav>
  <h1>photography</h1>
  <div class="photos">
    {#each photos as photo}
      <img src={photo} alt="photo" class="photo" />
    {/each}
  </div>
</div>

<style>
  nav {
    /* display: grid; */
    /* grid-template-columns: 1fr 1fr; */
    /* gap: 2rem; */
    width: 100%;
    /* background-color: #f5f5f5; */
    /* padding: 1rem; */
  }
  .my-freaking-name {
    font-size: 4rem;
    font-weight: bold;
    color: var(--card-border);
    /* text-align: center; */
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
    /* color: var(--card-border); */
    /* text-align: center; */
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
    /* background-color: var(--card-bg);
    border: 1px solid var(--card-border);
    padding: 1rem; */
  }
</style>
