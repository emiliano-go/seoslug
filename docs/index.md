---
seo:
  title: seoslug - seoslug
  canonical: https://seoslug.emiliano-go.com/
  robots: index,follow
  og:
    type: website
    title: seoslug - seoslug
    description: <p align="center" <img src="https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png"
      alt="seoslug" width="225"/ </p <p...
    url: https://seoslug.emiliano-go.com/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: seoslug - seoslug
    description: <p align="center" <img src="https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png"
      alt="seoslug" width="225"/ </p <p...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: <p align="center" <img src="https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png"
    alt="seoslug" width="225"/ </p <p...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: seoslug - seoslug
    url: https://seoslug.emiliano-go.com/
    description: <p align="center" <img src="https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png"
      alt="seoslug" width="225"/ </p <p...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>seoslug - seoslug</title>\n<meta name=\"description\" content=\"\
  &lt;p align=&quot;center&quot; &lt;img src=&quot;https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png&quot;\
  \ alt=&quot;seoslug&quot; width=&quot;225&quot;/ &lt;/p &lt;p...\">\n<link rel=\"\
  canonical\" href=\"https://seoslug.emiliano-go.com/\">\n<meta name=\"robots\" content=\"\
  index,follow\">\n<meta property=\"og:type\" content=\"website\">\n<meta property=\"\
  og:title\" content=\"seoslug - seoslug\">\n<meta property=\"og:description\" content=\"\
  &lt;p align=&quot;center&quot; &lt;img src=&quot;https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png&quot;\
  \ alt=&quot;seoslug&quot; width=&quot;225&quot;/ &lt;/p &lt;p...\">\n<meta property=\"\
  og:url\" content=\"https://seoslug.emiliano-go.com/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"seoslug - seoslug\">\n<meta name=\"twitter:description\"\
  \ content=\"&lt;p align=&quot;center&quot; &lt;img src=&quot;https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png&quot;\
  \ alt=&quot;seoslug&quot; width=&quot;225&quot;/ &lt;/p &lt;p...\">\n<meta name=\"\
  twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"seoslug - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/\",\n  \"\
  description\": \"<p align=\\\"center\\\" <img src=\\\"https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png\\\
  \" alt=\\\"seoslug\\\" width=\\\"225\\\"/ </p <p...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

<p align="center">
  <img src="https://raw.githubusercontent.com/emiliano-go/seoslug/refs/heads/master/assets/icon.png" alt="seoslug" width="225"/>
</p>
<p align="center">
  <em>Fast on the draw, faster on the crawl.</em>
</p>
<p align="center">
  <h1 align="center">seoslug</h1>
</p>

Deterministic SEO payload generation for content platforms.

Stop hand-rolling meta tags. Stop debugging inconsistent Open Graph output.
seoslug turns your content entities into production-ready SEO metadata in one
pure function call. Same input. Same output. Every time.

## What it does

seoslug takes three inputs (config, entity, route path) and returns a complete
`SEOPayload` dataclass with canonical URL, Open Graph tags, Twitter Cards,
robots directives, and JSON-LD structured data. Everything you need for a
`<head>` section, in one object.

## Why determinism matters

```python
p1 = build_seo_payload(entity, path, config)
p2 = build_seo_payload(entity, path, config)
assert p1 == p2  # Always True
```

Most SEO tools produce different output for identical input: random cache
busters, timestamps, dictionary key order instability. seoslug does none of
that. Every call is a pure function with zero side effects.

- **Commit SEO output to Git** and validate it in CI. If SEO changes, your
  build fails.
- **Cache forever.** Identical inputs always produce identical metadata. No
  invalidation logic needed.
- **Diff staging vs production** to instantly reveal configuration drift.
- **Track SEO evolution** right alongside your code.

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
    slug="introducing-v2",
    title="Introducing v2",
    excerpt="A fully deterministic SEO payload library.",
)

payload = build_seo_payload(entity, "/blog/introducing-v2", config)
```

`payload` is a `SEOPayload` dataclass. Attribute access, dict-style access,
render to HTML, or hash for caching:

```python
payload.title             # "Introducing v2"
payload.canonical         # "https://blog.example.com/blog/introducing-v2"
payload.og.image          # None (unless you set default_og_image)
payload.to_dict()         # plain dict ready for JSON serialization
payload.render_html()     # full <head> HTML snippet
payload.hash()            # deterministic SHA-256 hex digest
payload.etag()            # HTTP ETag header value
```

The equivalent JSON output:

```json
{
  "title": "Introducing v2",
  "description": "A fully deterministic SEO payload library.",
  "canonical": "https://blog.example.com/blog/introducing-v2",
  "robots": "index,follow",
  "og": {
    "type": "article",
    "title": "Introducing v2",
    "description": "A fully deterministic SEO payload library.",
    "url": "https://blog.example.com/blog/introducing-v2"
  },
  "twitter": {
    "card": "summary_large_image",
    "title": "Introducing v2",
    "description": "A fully deterministic SEO payload library."
  },
  "schema_jsonld": {
    "@context": "https://schema.org",
    "@type": "Article",
    "name": "Introducing v2",
    "url": "https://blog.example.com/blog/introducing-v2",
    "description": "A fully deterministic SEO payload library.",
    "mainEntityOfPage": {
      "@id": "https://blog.example.com/blog/introducing-v2"
    }
  }
}
```

## Performance

**10,000 payloads in 276 ms (28 µs/payload).** Every payload includes
canonical URL, Open Graph, Twitter Cards, robots, and JSON-LD. That is a
complete `head` section for 10,000 pages in under 300 ms.

Since every call is deterministic, wrap with `functools.lru_cache` for
zero-cost repeated lookups on the same input.

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

[Full comparison →](comparison.md)

## Next steps

- [Comparison: manual vs seoslug](comparison.md): see exactly what seoslug
  removes from your to-do list
- [Getting Started](getting-started.md): install, configure, generate your
  first payload
- [Core Concepts](core-concepts.md): determinism, pure functions, how the
  builder works
- [API Reference](api-reference.md): complete function and dataclass
  reference
- [Hooks](hooks.md): extend seoslug with custom post-processing
