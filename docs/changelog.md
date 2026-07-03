---
seo:
  title: Changelog - seoslug
  canonical: https://seoslug.emiliano-go.com/changelog/
  robots: index,follow
  og:
    type: website
    title: Changelog - seoslug
    description: All notable changes to seoslug are documented here. The format is
      based on Keep a Changelog. The project follows semantic versioning.
    url: https://seoslug.emiliano-go.com/changelog/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Changelog - seoslug
    description: All notable changes to seoslug are documented here. The format is
      based on Keep a Changelog. The project follows semantic versioning.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: All notable changes to seoslug are documented here. The format is based
    on Keep a Changelog. The project follows semantic versioning.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Changelog - seoslug
    url: https://seoslug.emiliano-go.com/changelog/
    description: All notable changes to seoslug are documented here. The format is
      based on Keep a Changelog. The project follows semantic versioning.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Changelog - seoslug</title>\n<meta name=\"description\" content=\"\
  All notable changes to seoslug are documented here. The format is based on Keep\
  \ a Changelog. The project follows semantic versioning.\">\n<link rel=\"canonical\"\
  \ href=\"https://seoslug.emiliano-go.com/changelog/\">\n<meta name=\"robots\" content=\"\
  index,follow\">\n<meta property=\"og:type\" content=\"website\">\n<meta property=\"\
  og:title\" content=\"Changelog - seoslug\">\n<meta property=\"og:description\" content=\"\
  All notable changes to seoslug are documented here. The format is based on Keep\
  \ a Changelog. The project follows semantic versioning.\">\n<meta property=\"og:url\"\
  \ content=\"https://seoslug.emiliano-go.com/changelog/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Changelog - seoslug\">\n<meta name=\"\
  twitter:description\" content=\"All notable changes to seoslug are documented here.\
  \ The format is based on Keep a Changelog. The project follows semantic versioning.\"\
  >\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Changelog - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/changelog/\"\
  ,\n  \"description\": \"All notable changes to seoslug are documented here. The\
  \ format is based on Keep a Changelog. The project follows semantic versioning.\"\
  ,\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n\
  \  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Changelog

All notable changes to seoslug are documented here. The format is based on Keep a Changelog. The project follows semantic versioning.

## 2.2.0 (2026-07-03)

### Fixed

- Python 3.10 compatibility: lazy import tomllib, fall back to tomli.
- Lazy import pyyaml in HugoBuilder and QuartzBuilder; add pyyaml to test deps.
- Correct twitter_site handle from @emiliano_gando to @emiliano_go_.

### Docs

- Replace OG image with 1408x768 Discord-friendly version.
- Add PyPI badge to README.
- Add favicon to docs site.
- Replace em dashes and prose dashes with colons in llms.txt and llms-full.txt.
- Replace em dashes with colons in doc source files.

### Chore

- Update .gitignore.

## 2.1.0 (2026-07-03)

### Added

- HugoBuilder and QuartzBuilder for static site generator SEO file generation.
- Zensical Markdown extension for inline SEO generation within Markdown docs.
- Favicon for documentation site.

### Docs

- New integration guides: Next.js, Gatsby, Astro, Nuxt, SvelteKit, Strapi.
- Add Flask and Starlette integration guides, split Starlette into dedicated page.
- Add PyPI badge to README.

## 2.0.1 (2026-07-03)

### Fixed

- Python 3.10 compatibility: lazy import `tomllib`, fall back to `tomli`.
- Lazy import `pyyaml` in HugoBuilder and QuartzBuilder; add `pyyaml` to test dependencies.

### Docs

- Replace OG image with 1408x768 Discord-friendly version.
- Add robots.txt, llms.txt, llms-full.txt.
- Add icon, centered heading, and catchphrase to landing page.

## 2.0.0 (2026-07-02)

### Added

#### New entity types

- `product` - Schema.org Product with sku, price, price_currency, and availability fields. Auto-generates Product JSON-LD with Offer.
- `organization` - Schema.org Organization with sameAs and logo support.
- `local_business` - Schema.org LocalBusiness extends Organization with address field.
- `faq` - Schema.org FAQPage with faq_items (list of FAQItem). Auto-generates Question/Answer JSON-LD.

#### New dataclasses

- `OGImage` - Structured image type with url, width, height, and alt. Accepted by SEOEntity.featured_image, SEOConfig.default_og_image, SEOOverrides.og_image, and SEOOverrides.twitter_image.
- `Breadcrumb` - Single breadcrumb entry with name and url. Used in SEOEntity.breadcrumbs.
- `FAQItem` - Single FAQ pair with question and answer. Used in SEOEntity.faq_items.
- `Robots` - Structured robots directive. Supports index, follow, max-snippet, max-image-preview, and max-video-preview. Serializes to standard robots meta content string.

#### BreadcrumbList auto-generation

Pass a list of `Breadcrumb` objects to `SEOEntity.breadcrumbs`. seoslug automatically generates a `BreadcrumbList` JSON-LD schema and appends it to the payload.

#### Social metadata fields

- `SEOOverrides.og_audio` and `SEOOverrides.og_video` for multimedia Open Graph tags.
- `SEOOverrides.twitter_creator` for Twitter `creator` attribution.
- `SEOConfig.locale_alternate` for alternate locale Open Graph tags.
- `SEOConfig.twitter_site` for Twitter `site` attribution.

#### SchemaRegistry

Register custom JSON-LD generators for any schema type. When `build_schema` encounters a registered type, it calls your generator instead of the built-in builder.

```python
from seoslug import SchemaRegistry

registry = SchemaRegistry()
registry.register("Podcast", lambda entity, config, canonical, title, description, og_image: {
    "@context": "https://schema.org",
    "@type": "Podcast",
    "name": title,
    "url": canonical,
})

config = SEOConfig(
    ...,
    schema_registry=registry,
)
```

#### Validation warnings

Set `emit_warnings=True` in `SEOConfig` to receive non-fatal Python warnings for common SEO issues (title too long, description too long, missing absolute URLs, malformed robots directives).

#### SEOPayload dataclass return type

`build_seo_payload` now returns an `SEOPayload` dataclass instead of a plain dict. The dataclass supports dict-style access (`payload["title"]`), attribute access (`payload.title`), and `.to_dict()`.

#### build_seo_payload_dict

New function that calls `build_seo_payload` and returns `payload.to_dict()`. Convenience wrapper for template engines and JSON serialization that expect a raw dictionary.

#### build_seo_payload_async

Async version of `build_seo_payload`. Runs the synchronous builder in a thread pool executor. Import from `seoslug.async_builder`. Accepts an optional `executor` parameter.

```python
from seoslug.async_builder import build_seo_payload_async

payload = await build_seo_payload_async(entity, route, config)
```

#### Factory functions

- `from_blog_post(title, body_html, ...)` - Creates an SEOEntity pre-configured as a blog post.
- `from_product(name, sku, price, ...)` - Creates an SEOEntity pre-configured as a product.
- `from_faq(questions, ...)` - Creates an SEOEntity pre-configured as an FAQ page.

#### SEOEntityBuilder

Fluent builder for `SEOEntity`. Use chained method calls instead of keyword arguments.

```python
from seoslug import SEOEntityBuilder

entity = (
    SEOEntityBuilder()
    .entity_type("product")
    .title("Widget")
    .price(29.99)
    .availability("InStock")
    .build()
)
```

### Changed

- lxml and detrack moved from core dependencies to optional extras.
  - `[fast]` extras include lxml + detrack (recommended).
  - `[light]` extras is a no-op marker for minimal installs.
- Pure-Python HTML extractor replaces lxml for `html_to_text` when lxml is not available.
- HTML entity decoding (nbsp, amp, lt, gt, quot, #39) added to pure-Python extractor.

## 1.1.0 (2026-06-17)

### Added

- Plugin/hook system for payload post-processing via `hook`, `register_hook`, `clear_hooks`, `get_registered_hooks`, and `run_hooks`.
- Custom exception hierarchy: `SEOError`, `SEOConfigError`, `SEOEntityError`, `URLPolicyError`, `SEOPayloadError`.
- `author_name` field on `SEOEntity` for JSON-LD author injection.
- `omit_schema` field on `SEOOverrides` for per-call schema suppression.
- `publisher_name` and `publisher_logo` fields on `SEOConfig` for JSON-LD publisher injection.

### Changed

- `build_seo_payload` now runs `post_process` hooks before returning.
- HTML body description extraction is now lazy: only parsed when no higher-precedence source is available.

## 1.0.2 (2026-06-??)

### Changed

- Minor internal improvements and documentation updates.

## 1.0.1 (2026-05-28)

### Changed

- Replaced inline tracking parameter logic with the detrack library.
- Tracking coverage expanded from 3 patterns to 60+ patterns.
- Added detrack as a dependency.

## 1.0.0 (2026-04-15)

### Added

- First stable release.
- SEOConfig, URLPolicy, SEOEntity, SEOOverrides dataclasses.
- build_seo_payload function for complete SEO payload generation.
- normalize_public_url and normalize_path for URL normalization.
- Automatic JSON-LD schema generation.
- Open Graph and Twitter Card generation.
- Deterministic, pure function design.
