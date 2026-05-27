# Usage Examples

## Basic payload generation

```python
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="portal.example.com",
    public_base_url="https://portal.example.com",
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
        allowed_query_params=["page", "q"],
    ),
    default_og_image="https://cdn.example.com/default.jpg",
)

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    excerpt="Example excerpt",
    body_html="<p>Body content</p>",
    status="published",
)

payload = build_seo_payload(entity, "/posts/my-post", config)
```

## Normalize URL only

```python
from seoslug import normalize_public_url

url = normalize_public_url(
    "http://old.example.com//Blog/Post?utm_source=x&page=2&bad=1",
    config,
)
# https://portal.example.com/blog/post?page=2
```

## Override selected metadata

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(
    meta_title="Custom title",
    canonical_url="https://portal.example.com/custom-path",
    twitter_card="summary",
)

payload = build_seo_payload(entity, "/posts/my-post", config, overrides)
```

## Search page robots

```python
search_entity = SEOEntity(entity_type="search", title="Search", status="published")
payload = build_seo_payload(search_entity, "/search?q=python", config)
# payload["robots"] == "noindex,follow"
```
