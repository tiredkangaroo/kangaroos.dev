<script lang="ts">
  import { onMount } from "svelte";
  let { title, screenshot_url, github_repo } = $props();

  let description = $state<undefined | string>(undefined);
  let last_commit = $state<undefined | string>(undefined);
  let homepage = $state<undefined | null | string>(undefined);

  onMount(() => {
    fetch("https://api.github.com/repos/" + github_repo)
      .then((res) => res.json())
      .then((data) => {
        description = data.description;
        last_commit = data.pushed_at;
        homepage = data.homepage;
      });
  });
</script>

{#if description && last_commit && homepage !== undefined}
  <div class="project-card">
    <img src={screenshot_url} alt={title + " screenshot"} class="project-screenshot" />
    <div class="project-info">
      <h2 class="project-title">{title}</h2>
      <p class="project-description">{description}</p>
      <p class="project-last-commit">Last commit: {new Date(last_commit).toLocaleDateString()}</p>
      <a href={"https://github.com/" + github_repo} target="_blank" rel="noopener noreferrer" class="card-button"
        >github</a
      >
      {#if homepage}
        <a href={homepage} target="_blank" rel="noopener noreferrer" class="card-button">demo</a>
      {/if}
    </div>
  </div>
{/if}

<style>
  .project-card {
    display: flex;
    flex-direction: column;
    background-color: var(--card-bg);
    border: 2px solid var(--card-border);
    padding: 1rem;
    margin: 1rem;
  }
  .project-screenshot {
    width: 100%;
    height: auto;
  }
  .card-button {
    display: inline-block;
    padding: 0.5rem 1rem;
    margin-top: 0.5rem;
    background-color: var(--card-border);
    color: white;
    text-decoration: none;
  }
</style>
