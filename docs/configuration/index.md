# Configuration overview

seoslug uses three dataclasses for configuration.

`SEOConfig` controls global behavior like canonical host and schema generation.
`URLPolicy` defines how URLs are normalized.
`SEOEntity` represents your content.
`SEOOverrides` lets you override any generated field on a per call basis.

## SEOConfig

`SEOConfig` is the main configuration object.
It holds your site wide settings.

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

## URLPolicy

`URLPolicy` controls URL normalization rules.

```python
from seoslug import URLPolicy

policy = URLPolicy(
    enforce_https=True,
    lowercase_paths=True,
    trailing_slash="never",
    strip_tracking_params=True,
)
```

## SEOEntity

`SEOEntity` represents a single content item.

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    excerpt="Example excerpt",
    status="published",
)
```

## SEOOverrides

`SEOOverrides` lets you override generated values for a single call.

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(
    meta_title="Custom title for this page",
    robots="noindex,follow",
)
payload = build_seo_payload(entity, "/path", config, overrides)
```

## Next steps

Read the detailed pages for each configuration class.
[SEOConfig Reference](seo-config.md). All SEOConfig fields explained.
[URLPolicy Reference](url-policy.md). URL normalization rules in detail.
[SEOEntity Reference](seo-entity.md). Input schema for content.
[SEOOverrides Reference](seo-overrides.md). Per call override options.
