import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";

// Options are not passed to sveltekit() on purpose: doing so makes sveltekit
// ignore svelte.config.js entirely, which is where the adapter and the runes
// compiler option live.
export default defineConfig({
  plugins: [sveltekit()],
});
