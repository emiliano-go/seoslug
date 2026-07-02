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
| FastAPI / Starlette | [FastAPI integration](fastapi.md) | Async route handlers, dependency injection, ETag caching |
| Django | [Django integration](django.md) | Class-based views, template context, Django REST Framework |
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
