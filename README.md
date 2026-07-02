<p align="center">
  <img src="https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/main/assets/icon.png" alt="seoslug" width="128"/>
</p>
<p align="center">
  <h1 align="center">seoslug</h1>
</p>

<p align="center">
  <strong>Deterministic SEO payload generation for content platforms.</strong>
</p>

<p align="center">
  <a href="https://www.python.org/downloads/">
    <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white&style=for-the-badge" alt="Python">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-10AC84?style=for-the-badge" alt="License">
  </a>
  <a href="https://deepwiki.com/emiliano-go/seoslug/">
    <img src="https://img.shields.io/badge/DeepWiki-8A2BE2?logo=readthedocs&logoColor=white&style=for-the-badge" alt="DeepWiki">
  </a>
</p>

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
    title="Introducing v2",
    excerpt="A fully deterministic SEO payload library.",
)

payload = build_seo_payload(entity, "/blog/introducing-v2", config)
```

That is it. `payload` is a `SEOPayload` dataclass with title, description, canonical,
robots, og, twitter, and schema_jsonld -- ready to inject into your HTML.

Render the full `<head>` in one call:

```python
payload.render_html()
# '<title>Introducing v2</title>\n<meta name="description" ...'
```

Or access individual fields:

```python
payload.title           # "Introducing v2"
payload.canonical       # "https://blog.example.com/blog/introducing-v2"
payload.og.image        # None (set default_og_image in config)
payload.to_dict()       # plain dict for JSON serialization
```

```json
{
  "title": "Introducing v2",
  "canonical": "https://blog.example.com/blog/introducing-v2",
  "robots": "index,follow",
  "og": {
    "type": "article",
    "title": "Introducing v2",
    "url": "https://blog.example.com/blog/introducing-v2"
  },
  "twitter": {
    "card": "summary_large_image",
    "title": "Introducing v2"
  },
  "schema_jsonld": {
    "@context": "https://schema.org",
    "@type": "Article",
    "name": "Introducing v2",
    "url": "https://blog.example.com/blog/introducing-v2"
  }
}
```

Render the same payload twice -- identical HTML, identical hash. That is the
foundation of everything that follows.

---

## Benchmarks

```
10,000 payloads in 276 ms  (28 µs/payload)
```

Every payload includes: canonical URL, Open Graph (10+ fields), Twitter Cards
(6+ fields), robots directive, and JSON-LD structured data. That is 10,000
complete SEO metadata objects in under 300 ms.

---
## Comparison: manual vs seoslug

| Task | Manual | seoslug |
|---|---|---|
| Canonical URL | Construct by hand | `build_seo_payload(entity, path, config)` |
| Open Graph tags | 10+ `<meta>` tags | `payload.og` or `payload.render_html()` |
| Twitter Cards | 6+ `<meta>` tags | `payload.twitter` or `payload.render_html()` |
| JSON-LD schema | Write and maintain schema.org JSON | Auto-generated |
| BreadcrumbList | Manual `BreadcrumbList` JSON-LD | `Breadcrumb(name, url)` auto-generates |
| URL normalization | HTTPS, trailing slash, lowercase logic | `URLPolicy` handles it |
| HTML excerpt | Strip tags, decode entities, truncate | Built-in `html_to_text()` |
| Validation | Manual audit of title/description length | `emit_warnings=True` in config |
| HTML rendering | Jinja2 template for every tag | `payload.render_html()` |
| Content-based ETag | Manual hash | `payload.etag()` |
| Testing | Manual snapshot fixtures | Deterministic: `assert payload == dict` |

[Full comparison →](docs/comparison.md)

---

## Why determinism matters

```python
p1 = build_seo_payload(entity, path, config)
p2 = build_seo_payload(entity, path, config)
assert p1 == p2  # Always True
```

Most SEO tools produce different output for identical input: random cache
busters, timestamps, dictionary key order instability. seoslug does none of
that. Every call is a pure function with zero side effects.

- **Commit SEO output to Git** and validate it in CI. If SEO changes, your build fails.
- **Cache forever.** Identical inputs always produce identical metadata. No invalidation logic needed.
- **Diff staging vs production** to instantly reveal configuration drift.
- **Track SEO evolution** right alongside your code.

SEO becomes another deterministic build artifact -- testable, cacheable, and CI-verifiable.

---

## Features

| Category | What seoslug handles |
|---|---|
| **URL normalization** | HTTPS enforcement, trailing slash policy, lowercase paths, duplicate-slash collapse, tracking-parameter stripping (detrack or built-in regex) |
| **Open Graph** | `og:title`, `og:description`, `og:image` (+ width/height/alt), `og:type`, `og:url`, `og:site_name`, `og:locale`/`locale:alternate`, `og:audio`, `og:video` |
| **Twitter Cards** | `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image` (+ alt), `twitter:site`, `twitter:creator` |
| **JSON-LD schemas** | Article, WebPage, VideoObject, CollectionPage, SearchResultsPage, Product, Organization, LocalBusiness, FAQPage, BreadcrumbList |
| **Schema registry** | Register custom schema generators for any schema.org type |
| **Robots directives** | `index`/`noindex`, `follow`/`nofollow`, `max-snippet`, `max-image-preview` - via string or structured `Robots` dataclass |
| **Breadcrumbs** | `Breadcrumb(name, url)` auto-generates `BreadcrumbList` JSON-LD |
| **Validation warnings** | Title length, description length, canonical URL scheme, OG image URL, robots format |
| **Dependency model** | Default: **`seoslug[fast]`** (lxml + detrack). Minimal: **`seoslug[light]`** (pure Python). |

---

## Framework support

| Framework | Integration |
|---|---|
| **FastAPI** / **Starlette** / **Litestar** | Call `build_seo_payload` in your route handler. Or use `build_seo_payload_async` to offload to a thread pool. |
| **Django** / **Flask** / **Quart** | Call in your view function. Pass the dataclass to your template context. |
| **Static site generators** (Pelican, MkDocs, Astro) | Run at build time. Commit the JSON output to Git. |
| **Custom CMS** | Use `build_seo_payload_dict` for a plain dict if you prefer. |

---

## Installation

```bash
pip install "seoslug[fast]"
```

This is the recommended install. It includes **lxml** (C-optimized HTML
extraction) and **detrack** (tracking-parameter stripping).

For a minimal footprint with pure-Python fallbacks:

```bash
pip install "seoslug[light]"
```

Identical output. Only performance differs for very large HTML bodies.

---

## At a glance

```python
# Structured OG images
entity = SEOEntity(
    entity_type="post",
    featured_image=OGImage(url="https://ex.com/img.jpg", width=1200, height=630, alt="Hero"),
)

# Structured robots
config = SEOConfig(..., default_robots=Robots(index=True, follow=False, max_snippet=-1))

# Breadcrumbs
entity = SEOEntity(
    entity_type="page",
    breadcrumbs=[Breadcrumb(name="Home", url="/"), Breadcrumb(name="Blog", url="/blog")],
)

# Schema registry
registry = SchemaRegistry()
registry.register("Podcast", lambda e, c, can, t, d, og: {"@type": "Podcast", "name": t})

# Factory shortcuts
entity = from_blog_post(title="Hello", body_html="<p>World</p>", author="Jane")

# Fluent builder
entity = SEOEntityBuilder().entity_type("product").title("Widget").sku("W-001").build()

# Async support
payload = await build_seo_payload_async(entity, "/post", config)

# Dict wrapper
d = build_seo_payload_dict(entity, "/post", config)

# Render HTML
head_html = payload.render_html()

# Content hash / ETag
fingerprint = payload.hash()
etag_value = payload.etag()
```

---

## Documentation

- [Comparison: manual vs seoslug](docs/comparison.md)
- [Getting started](docs/getting-started.md)
- [Core concepts](docs/core-concepts.md)
- [Configuration](docs/configuration/index.md)
- [API reference](docs/api-reference.md)
- [DeepWiki](https://deepwiki.com/emiliano-go/seoslug/)
