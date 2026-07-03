---
seo:
  title: FAQ - seoslug
  canonical: https://seoslug.emiliano-go.com/faq/
  robots: index,follow
  og:
    type: website
    title: FAQ - seoslug
    description: Why deterministic?
    url: https://seoslug.emiliano-go.com/faq/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: FAQ - seoslug
    description: Why deterministic?
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Why deterministic?
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: FAQ - seoslug
    url: https://seoslug.emiliano-go.com/faq/
    description: Why deterministic?
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>FAQ - seoslug</title>\n<meta name=\"description\" content=\"Why\
  \ deterministic?\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/faq/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"FAQ - seoslug\">\n<meta property=\"\
  og:description\" content=\"Why deterministic?\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/faq/\">\n<meta property=\"og:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"og:image:width\"\
  \ content=\"225\">\n<meta property=\"og:image:height\" content=\"225\">\n<meta property=\"\
  og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\" content=\"en_US\"\
  >\n<meta name=\"twitter:card\" content=\"summary_large_image\">\n<meta name=\"twitter:title\"\
  \ content=\"FAQ - seoslug\">\n<meta name=\"twitter:description\" content=\"Why deterministic?\"\
  >\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"FAQ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/faq/\",\n  \"\
  description\": \"Why deterministic?\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# FAQ

## Why deterministic?

Determinism enables testing, caching, and confidence. You can snapshot test your SEO layer. You can cache payloads without invalidation logic. You can diff staging against production to find configuration drift.

## Can I add custom meta tags?

Not directly through seoslug. But you can extend the payload after generation. The returned `SEOPayload` is a dataclass. Convert it to a dict, add your custom tags, then pass it to your template.

```python
payload = build_seo_payload(entity, "/path", config)
data = payload.to_dict()
data["custom_tags"] = '<meta name="foo" content="bar">'
```

## How do I disable auto-generated schema?

Set `auto_generate_schema` to `False` in `SEOConfig`.

```python
config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=...,
    auto_generate_schema=False,
)
```

Or set `omit_schema` to `True` in `SEOOverrides` for a single entity.

```python
overrides = SEOOverrides(omit_schema=True)
```

## Does seoslug work with Django?

Yes. See the [Django integration guide](integrations/django.md).

## Does seoslug work with FastAPI?

Yes. See the [FastAPI integration guide](integrations/fastapi.md).

## Does seoslug work with static site generators?

Yes. See the [SSG integration guide](integrations/ssg.md).

## Is seoslug thread safe?

Yes. All functions are pure and stateless. There is no mutable shared state. The async builder uses a thread pool executor, which is safe by design.

## Are there zero core dependencies?

The recommended install (`pip install "seoslug[fast]"`) includes lxml and
detrack. For a minimal pure-Python install with no extra dependencies:

```bash
pip install "seoslug[light]"
```

The `[light]` extras marker makes your intent explicit. Output is identical
either way. Only performance differs for very large HTML bodies.

## Why no backlink features?

Backlink management is off-page SEO. seoslug focuses on on-page SEO metadata generation. These two concerns are separate.

## Do I need lxml?

No. The `[light]` extras install seoslug without lxml. The pure-Python HTML
extractor strips tags and normalises whitespace with identical results.
Performance may differ for very large HTML bodies.

## Do I need detrack?

No. The `[light]` extras install seoslug without detrack. Tracking-parameter
stripping falls back to a built-in set of common tracking parameters (utm_*,
fbclid, gclid, etc.).

## Why am I seeing validation warnings?

Enable validation warnings by setting `emit_warnings=True` in `SEOConfig`. Warnings fire through Python's `warnings` module when the payload has issues (title too long, missing OG image, etc).

```python
import warnings
warnings.filterwarnings("always")

config = SEOConfig(
    ...,
    emit_warnings=True,
)
```

These are non-fatal. They help you catch SEO problems during development.

## What is the Robots dataclass?

`Robots` is a structured dataclass for fine-grained robots directives. Use it instead of a raw string when you need `max-snippet`, `max-image-preview`, or `max-video-preview`.

```python
from seoslug import Robots

robots = Robots(index=True, follow=True, max_snippet=150)
```

## What is the OGImage dataclass?

`OGImage` is a structured dataclass for Open Graph images with optional width, height, and alt text.

```python
from seoslug import OGImage

image = OGImage(
    url="https://example.com/image.jpg",
    width=1200,
    height=630,
    alt="Preview image",
)
```

Use it anywhere seoslug accepts an image value: `featured_image`, `default_og_image`, `SEOOverrides.og_image`, and `SEOOverrides.twitter_image`.

## What Python versions are supported?

Python 3.10 and later.

## How do I report a bug?

Open an issue on GitHub. Include the version, input, expected output, and actual output.
