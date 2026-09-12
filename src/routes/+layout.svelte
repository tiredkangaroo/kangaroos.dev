<script lang="ts">
  import favicon from "$lib/assets/favicon.svg";

  let { children } = $props();
</script>

<svelte:head>
  <link rel="icon" href={favicon} />
  <style>
    :root {
      --card-bg: #ace8bc;
      --card-border: #346140;
    }
    html,
    body {
      margin: 0;
      padding: 0;
      font-family: monospace;
    }
  </style>
</svelte:head>

{@render children()}
