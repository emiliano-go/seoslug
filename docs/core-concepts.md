---
seo:
  title: Core concepts - seoslug
  canonical: https://seoslug.emiliano-go.com/core-concepts/
  robots: index,follow
  og:
    type: website
    title: Core concepts - seoslug
    description: seoslug is built on determinism, single responsibility, and pure
      functions. These principles make your SEO layer testable, cacheable, and predictable.
    url: https://seoslug.emiliano-go.com/core-concepts/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Core concepts - seoslug
    description: seoslug is built on determinism, single responsibility, and pure
      functions. These principles make your SEO layer testable, cacheable, and predictable.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: seoslug is built on determinism, single responsibility, and pure functions.
    These principles make your SEO layer testable, cacheable, and predictable.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Core concepts - seoslug
    url: https://seoslug.emiliano-go.com/core-concepts/
    description: seoslug is built on determinism, single responsibility, and pure
      functions. These principles make your SEO layer testable, cacheable, and predictable.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Core concepts - seoslug</title>\n<meta name=\"description\" content=\"\
  seoslug is built on determinism, single responsibility, and pure functions. These\
  \ principles make your SEO layer testable, cacheable, and predictable.\">\n<link\
  \ rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/core-concepts/\">\n<meta\
  \ name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Core concepts - seoslug\">\n<meta\
  \ property=\"og:description\" content=\"seoslug is built on determinism, single\
  \ responsibility, and pure functions. These principles make your SEO layer testable,\
  \ cacheable, and predictable.\">\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/core-concepts/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"Core concepts - seoslug\"\
  >\n<meta name=\"twitter:description\" content=\"seoslug is built on determinism,\
  \ single responsibility, and pure functions. These principles make your SEO layer\
  \ testable, cacheable, and predictable.\">\n<meta name=\"twitter:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Core concepts\
  \ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/core-concepts/\",\n\
  \  \"description\": \"seoslug is built on determinism, single responsibility, and\
  \ pure functions. These principles make your SEO layer testable, cacheable, and\
  \ predictable.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Core concepts

seoslug is built on determinism, single responsibility, and pure functions.
These principles make your SEO layer testable, cacheable, and predictable.

## Determinism

Identical inputs always produce identical outputs. Always.

```python
payload1 = build_seo_payload(entity, path, config)
payload2 = build_seo_payload(entity, path, config)
assert payload1 == payload2  # Always True
```

Most SEO libraries mix in timestamps, random cache busters, or environment
variables. seoslug does none of that. The same URL, entity, and config
always yield an identical `SEOPayload`.

This means:

- **Snapshot testing.** Commit expected output to Git. If SEO changes, your
  build fails.
- **Diffable deployments.** Compare staging vs production payloads to catch
  config drift.
- **Infinite caching.** `functools.lru_cache` on `build_seo_payload` gives
  you zero-cost repeat calls.

Concretely: if you generate SEO for a blog post on Monday and again on
Tuesday with the same inputs, every byte of the output is identical. No
surprises. No cache invalidation riddles.

## Single responsibility

seoslug generates SEO metadata. Nothing else.

- It does not rewrite your content.
- It does not make HTTP requests.
- It does not store state.
- It does not read environment variables.

You provide the data. seoslug formats it. That is the entire contract.

## Pure functions

Every public function in seoslug is a pure function:

- No system clock access
- No random number generation
- No environment variable reads
- No external API calls
- No mutable global state

What you see in the config is what you get in the output. This makes
seoslug trivially testable and safe to call from anywhere (web servers,
build pipelines, REPLs, tests).

## How it works

The builder accepts exactly three inputs and returns one structured output.

### Inputs

```python
payload = build_seo_payload(entity, route_path, config)
```

| Input | Type | What it provides |
|---|---|---|
| `config` | `SEOConfig` | Site-wide rules: canonical host, URL policy, templates, defaults |
| `entity` | `SEOEntity` | Per-content data: title, excerpt, images, schema fields |
| `route_path` | `str` | The URL path for this piece of content (e.g. `/blog/my-post`) |

### Output

```python
payload: SEOPayload
```

The `SEOPayload` dataclass contains seven keys:

| Key | Type | Source |
|---|---|---|
| `title` | `str` | Override > entity title > `"Untitled"`, with optional template |
| `description` | `str` | Override > entity excerpt > body snippet > `""` |
| `canonical` | `str` | Override > normalized public URL |
| `robots` | `str` | Override > entity default (based on type/status) > config default |
| `og` | `OGPayload` | Resolved from entity + config + overrides |
| `twitter` | `TwitterPayload` | Resolved from OG + config + overrides |
| `schema_jsonld` | `dict \| list[dict] \| None` | Override > auto-generated schema (if enabled) + breadcrumbs |

### Fallback chains

Each field resolves through a priority chain:

1. **SEOOverrides** (per-call, highest priority)
2. **SEOEntity** (per-content)
3. **SEOConfig** (site-wide defaults, lowest priority)

This means you can set sensible defaults globally, override per-entity for
most fields, and override per-call for edge cases.

```python
# Config-level default
config = SEOConfig(..., default_og_image="https://cdn.example.com/default.jpg")

# Entity-level override
entity = SEOEntity(..., featured_image=OGImage(url="https://cdn.example.com/hero.jpg", width=1200, height=630))

# Call-level override (wins everything)
overrides = SEOOverrides(og_image="https://cdn.example.com/urgent.jpg")

payload = build_seo_payload(entity, "/post", config, overrides)
# og:image is "https://cdn.example.com/urgent.jpg"
```

### Key resolution rules

- **title**: Override `meta_title` > entity `title` > `"Untitled"`.
  Config `title_template` is applied unless `skip_title_template` is set.
- **description**: Override `meta_description` > entity `excerpt` > body
  HTML text snippet > `""`.
- **canonical**: Override `canonical_url` > `normalize_public_url(route_path)`.
- **robots**: Override > entity-based default (`noindex,follow` for search
  type, `index,follow` for published, config `default_robots` otherwise).
- **og**:title/description/image cascade down from title/description/image
  unless explicitly overridden.
- **twitter**:title/description/image cascade down from OG equivalents.
- **schema_jsonld**: Override > auto-generated from entity fields +
  auto-generated `BreadcrumbList` when breadcrumbs are present.
