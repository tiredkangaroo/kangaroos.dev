// The photo shown depends on ?id=, which a prerender can't know, so this route
// stays client-rendered. Everything else on the site is prerendered to HTML.
export const ssr = false;