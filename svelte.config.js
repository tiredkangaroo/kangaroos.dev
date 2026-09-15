import adapter from "@sveltejs/adapter-static";

/** @type {import('@sveltejs/kit').Config} */
const config = {
  kit: {
    adapter: adapter({
      pages: "build",
      assets: "build",
      fallback: null,
      precompress: false,
      strict: true,
    }),
    paths: {
      // Set to your repository name if hosting at https://<username>.github.io/<repo-name>/
      // base: process.env.NODE_ENV === 'production' ? '/my-repo-name' : ''
    },
  },
};

export default config;
