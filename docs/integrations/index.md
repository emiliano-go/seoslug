---
seo:
  title: Integrations - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/
  robots: index,follow
  og:
    type: website
    title: Integrations - seoslug
    description: seoslug is framework-agnostic. You can use it with any Python web
      framework, static site generator, or build pipeline.
    url: https://seoslug.emiliano-go.com/integrations/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Integrations - seoslug
    description: seoslug is framework-agnostic. You can use it with any Python web
      framework, static site generator, or build pipeline.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: seoslug is framework-agnostic. You can use it with any Python web framework,
    static site generator, or build pipeline.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Integrations - seoslug
    url: https://seoslug.emiliano-go.com/integrations/
    description: seoslug is framework-agnostic. You can use it with any Python web
      framework, static site generator, or build pipeline.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Integrations - seoslug</title>\n<meta name=\"description\" content=\"\
  seoslug is framework-agnostic. You can use it with any Python web framework, static\
  \ site generator, or build pipeline.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Integrations - seoslug\">\n<meta\
  \ property=\"og:description\" content=\"seoslug is framework-agnostic. You can use\
  \ it with any Python web framework, static site generator, or build pipeline.\"\
  >\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/integrations/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"Integrations - seoslug\"\
  >\n<meta name=\"twitter:description\" content=\"seoslug is framework-agnostic. You\
  \ can use it with any Python web framework, static site generator, or build pipeline.\"\
  >\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Integrations - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/\"\
  ,\n  \"description\": \"seoslug is framework-agnostic. You can use it with any Python\
  \ web framework, static site generator, or build pipeline.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
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
| Zensical | [Zensical integration](zensical.md) | Pre-build script + template override, works with any MkDocs theme |
| Hugo | [Hugo integration](hugo.md) | Pre-build frontmatter injection + head partial, works with any theme |
| Quartz | [Quartz integration](quartz.md) | Pre-build frontmatter injection + Head component mod |
| Static site generators | [SSG integration](ssg.md) | Build-time generation, JSON manifest, Pelican, MkDocs |

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
