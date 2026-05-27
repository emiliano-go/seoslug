# seoslug

[![DeepWiki](https://img.shields.io/badge/DeepWiki-Documentation-blue)](https://deepwiki.com/emiliano-gandini-outeda/seoslug/)

Canonical URL normalization and deterministic SEO payload generation for content platforms.

## Installation

```bash
pip install seoslug
```

For local development:

```bash
pip install -e .
```

## Quick usage

```python
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="portal.example.com",
    public_base_url="https://portal.example.com",
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
        collapse_duplicate_slashes=True,
        strip_tracking_params=True,
        allowed_query_params=["page", "q"],
    ),
    default_og_image="https://cdn.example.com/default.jpg",
)

entity = SEOEntity(
    entity_type="post",
    slug="my-post",
    title="My Post",
    excerpt="Example excerpt",
    body_html="<p>Body content</p>",
    status="published",
    featured_image="https://cdn.example.com/post.jpg",
)

payload = build_seo_payload(entity, "/posts/my-post", config)
```

Full docs, API reference, and usage examples are in `docs/` and published with Zensical.

## License

MIT, see `LICENSE`.
