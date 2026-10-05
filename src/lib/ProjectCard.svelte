<script lang="ts">
  import { onMount } from "svelte";

  let { title, screenshot_url, screenshot_size, github_repo, override_desc } = $props();

  // Rendered immediately with what we already know, so a slow, rate-limited or
  // unreachable GitHub api can't leave an empty hole in the projects section.
  // `undefined` means "not fetched yet" and falls back to override_desc.
  let description = $state<string | undefined>(undefined);
  let last_commit = $state<Date | undefined>(undefined);
  let homepage = $state<string | null>(null);

  onMount(() => {
    const controller = new AbortController();
    // Nothing is waiting on this, so don't let a slow api hold a card open.
    const timeout = setTimeout(() => controller.abort(), 8000);
    fetch("https://api.github.com/repos/" + github_repo, {
      signal: controller.signal,
      headers: { Accept: "application/vnd.github+json" },
    })
      .then((res) => (res.ok ? res.json() : null))
      .then((data) => {
        if (!data) return;
        description = data.description || undefined;
        last_commit = data.pushed_at ? new Date(data.pushed_at) : undefined;
        homepage = data.homepage || null;
      })
      .catch(() => {})
      .finally(() => clearTimeout(timeout));
  });
</script>

<div class="project-card">
  <img
    src={screenshot_url}
    alt={title + " screenshot"}
    class="project-screenshot"
    width={screenshot_size?.[0]}
    height={screenshot_size?.[1]}
    loading="lazy"
    decoding="async"
  />
  <div class="project-info">
    <h2 class="project-title">{title}</h2>
    <p class="project-description">{description ?? override_desc ?? ""}</p>
    {#if last_commit}
      <p class="project-last-commit">Last push: {last_commit.toLocaleDateString()}</p>
    {/if}
    <a href={"https://github.com/" + github_repo} target="_blank" rel="noopener noreferrer" class="card-button"
      >github</a
    >
    {#if homepage}
      <a href={homepage} target="_blank" rel="noopener noreferrer" class="card-button">demo</a>
    {/if}
  </div>
</div>

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
  .project-description {
    font-family: "Times New Roman", serif;
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