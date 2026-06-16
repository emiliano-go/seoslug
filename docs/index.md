# seoslug

seoslug turns your content entities into production ready SEO metadata.
It generates canonical URLs, Open Graph tags, Twitter Cards, and JSON-LD.
The library is deterministic. Same input always produces the same output.
This makes your SEO layer testable, cacheable, and predictable.

## Install

```bash
pip install seoslug
```

## Quick start

```python
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="portal.example.com",
    public_base_url="https://portal.example.com",
    url_policy=URLPolicy(allowed_query_params=["page", "q"]),
)

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    excerpt="Example excerpt",
    status="published",
)

payload = build_seo_payload(entity, "/posts/my-post", config)
```

The payload contains title, description, canonical, robots, og, twitter, and schema_jsonld.
Inject it directly into your HTML head section.

## Next steps

Read the [Getting Started](getting-started.md) guide for installation and setup.
Read [Core Concepts](core-concepts.md) to understand how seoslug works.
Read the [API Reference](api-reference.md) for the complete function reference.
Read the [Hooks Guide](hooks.md) to extend seoslug with custom post-processing.
