# Integrations overview

seoslug works with many Python web frameworks.
You can use it with FastAPI, Django, Flask, or any static site generator.
The integrations section covers each of these with working code examples.

Each example shows how to call `build_seo_payload` in your specific framework.
It also shows how to render the payload in templates and cache the results.

## Available guides

- [FastAPI](fastapi.md). Async route handlers with ETag caching.
- [Django](django.md). Views, templates, and framework caching.
- [Static Site Generators](ssg.md). Hugo, Pelican, MkDocs, and build time generation.

## General pattern

The pattern is the same across all frameworks.

1. Create your SEOConfig once at application startup.
2. Build an SEOEntity for each content item.
3. Call `build_seo_payload` in your route handler or build step.
4. Pass the payload to your template.
5. Render the meta tags in the HTML head section.

```python
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

# Do this once
config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)

# Do this per request
entity = SEOEntity(entity_type="post", title="My Post")
payload = build_seo_payload(entity, "/posts/my-post", config)
```
