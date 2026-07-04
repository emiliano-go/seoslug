---
{}
---

# Configuration overview

seoslug uses four dataclasses to configure SEO output. Each one has a single responsibility. You compose them together at build time.

## SEOConfig

Global settings for your entire site. Controls canonical host, URL normalization, robots defaults, Open Graph, schema generation, and locale.

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

[Full reference](seo-config.md)

## URLPolicy

URL normalization rules. Enforces HTTPS, trailing slash policy, lowercase paths, and query parameter filtering. Every canonical URL flows through this pipeline.

```python
from seoslug import URLPolicy

policy = URLPolicy(
    enforce_https=True,
    lowercase_paths=True,
    trailing_slash="never",
    strip_tracking_params=True,
)
```

[Full reference](url-policy.md)

## SEOEntity

Your content. Holds the raw data seoslug uses to generate title, description, Open Graph, Twitter Cards, and JSON-LD schema. Entity type determines the schema output.

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    excerpt="A brief description",
    status="published",
)
```

[Full reference](seo-entity.md)

## SEOOverrides

Per-call overrides. Bypass generated values for a single page without touching global config. Useful for custom titles, per-page robots, or injecting custom JSON-LD.

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(
    meta_title="Custom Page Title",
    robots="noindex,follow",
)
payload = build_seo_payload(entity, "/path", config, overrides)
```

[Full reference](seo-overrides.md)
