---

# Integrations

seoslug is framework-agnostic. You can use it with any Python web framework, static site generator, or build pipeline.

The general pattern is always the same:

1. Build an `SEOEntity` from your content data.
2. Create an `SEOConfig` that matches your deployment.
3. Call `build_seo_payload` (or `build_seo_payload_async` for async frameworks).
4. Inject the returned `SEOPayload` into your template or JSON response.

## Framework guides

| Framework | Guide | Notes |
|-----------|-------|-------|
| FastAPI | [FastAPI integration](fastapi.md) | Async route handlers, dependency injection, ETag caching |
| Starlette | [Starlette integration](starlette.md) | Async endpoints, path params, middleware, Jinja2Templates |
| Django | [Django integration](django.md) | Class-based views, template context, Django REST Framework |
| Flask | [Flask integration](flask.md) | Route handlers, Jinja2 templates, JSON APIs, extension pattern |
| Nuxt | [Nuxt integration](nuxt.md) | `useHead` composable + `asyncData` in Nuxt 3, static or SSR |
| SvelteKit | [SvelteKit integration](sveltekit.md) | `load` function in `+page.js` + `<svelte:head>`, static or SSR |

## SSG guides

| SSG | Guide | Notes |
|-----|-------|-------|
| Hugo | [Hugo integration](hugo.md) | Pre-build frontmatter injection + head partial, works with any theme |
| Quartz | [Quartz integration](quartz.md) | Pre-build frontmatter injection + Head component mod |
| Next.js | [Next.js integration](nextjs.md) | `getStaticProps` + `next/head`, or `generateMetadata` in App Router |
| Gatsby | [Gatsby integration](gatsby.md) | `onCreatePage` in `gatsby-node.js` + Gatsby Head API |
| Astro | [Astro integration](astro.md) | `<Seo />` component via `Astro.glob` or JSON manifest |
| Zensical | [Zensical integration](zensical.md) | Inline Markdown extension + template override, or pre-build script |
| Static site generators | [SSG integration](ssg.md) | Build-time generation, JSON manifest, Pelican, MkDocs |

## CMS guides

| CMS | Guide | Notes |
|-----|-------|-------|
| Strapi | [Strapi integration](strapi.md) | Custom middleware to enrich API responses with SEO payloads |

## Other frameworks

seoslug works anywhere Python runs. The integration pattern is the same:

```python
from seoslug import SEOConfig, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="yoursite.com",
    public_base_url="https://yoursite.com",
    url_policy=...,
)

entity = SEOEntity(
    entity_type="page",
    title="Hello",
    status="published",
)

payload = build_seo_payload(entity, "/hello", config)
```

Use `payload.to_dict()` when you need a plain dict for template engines or JSON serialization. Use `build_seo_payload_dict()` as a shorthand.

For async frameworks, import from `seoslug.async_builder`:
