<p align="center">
  <h1 align="center">seoslug</h1>
</p>

<p align="center">
  <strong>Canonical URL normalization + deterministic SEO payload generation for content platforms.</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-10AC84?style=for-the-badge" alt="License">
  </a>
  <a href="https://deepwiki.com/emiliano-gandini-outeda/seoslug/">
    <img src="https://img.shields.io/badge/DeepWiki-8A2BE2?logo=readthedocs&logoColor=white&style=for-the-badge" alt="DeepWiki">
  </a>
</p>

---

## What is seoslug?

seoslug turns your content entities into production-ready SEO metadata, canonical URLs, Open Graph, Twitter Cards, and JSON-LD, **deterministically**. Same input always produces the same output, making your SEO layer testable, cacheable, and predictable.

**One function call. Complete SEO coverage. No surprises.**

---

## Quick start

```python
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
    ),
)

entity = SEOEntity(
    entity_type="post",
    slug="my-post",
    title="My Post",
    excerpt="Example excerpt",
)

payload = build_seo_payload(entity, "/posts/my-post", config)
```

That's it. payload contains everything you need: title, description, canonical, og, twitter, and schema_jsonld, ready to inject into your HTML.

### Why deterministic?

Most SEO tools produce different output for the same input: random cache busters, timestamps, or dictionary key order changes. **seoslug** does none of that.

```python
payload1 = build_seo_payload(entity, path, config)
payload2 = build_seo_payload(entity, path, config)
assert payload1 == payload2  # Always True
```

This seemingly small property unlocks powerful workflows. You can commit expected SEO output to Git and validate it in CI: if SEO changes, your build fails. The same URL always generates an identical payload, so you can cache forever without invalidation logic. Diffing staging against production instantly reveals configuration drift, and you can track how your SEO evolves right alongside your code.

### What seoslug handles

**URL normalization**: HTTPS enforcement, trailing slash policy, lowercase paths, query parameter sorting. Optionally strips tracking parameters using [detrack](https://github.com/emiliano-gandini-outeda/detrack).

**Open Graph and Twitter Cards**: `og:title`, `og:image`, `twitter:card`, and everything else search engines and social platforms expect.

**JSON-LD**: Auto-generates schema.org schemas (Article, WebPage, VideoObject, CollectionPage, SearchResultsPage) based on your entity type. Map any entity type to any schema type via config. Override with custom JSON-LD when needed.

**Robots directives**: index/noindex and follow/nofollow based on entity status.

**Configurable fallbacks**: Define what happens when a field is missing. `Title` can fall back to `meta_title`, then `entity.title`, then `"Untitled"`. Description falls back from `meta_description` to `entity.excerpt` to an auto-generated HTML body snippet. The HTML body is only parsed when no higher-precedence source is available.

**Plugin hooks**: Extend the payload with custom JSON-LD, inject organization schemas, or transform descriptions via the `post_process` hook system.

And everything is pure: no environment variables, no system clock, no random numbers, no external API calls.

### Documentation
- [Docs](https://emiliano-gandini-outeda.me/seoslug)
- [Deepwiki](https://deepwiki.com/emiliano-gandini-outeda/seoslug/)
- [Hooks & Plugins](https://emiliano-gandini-outeda.me/seoslug/hooks/)
- [API Reference](https://emiliano-gandini-outeda.me/seoslug/api-reference/)