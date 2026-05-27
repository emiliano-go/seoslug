# seoslug

Canonical URL normalization and deterministic SEO payload generation for content platforms.

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

## What you get

- One URL normalization engine, host and scheme enforcement included.
- One SEO payload builder with strict fallback order.
- Deterministic output for tests and snapshots.
