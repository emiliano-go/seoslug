# API Reference

## Public imports

```python
from seoslug import (
    SEOConfig,
    URLPolicy,
    SEOEntity,
    SEOOverrides,
    normalize_public_url,
    normalize_path,
    build_seo_payload,
)
```

## URLPolicy

- `enforce_https: bool = True`
- `lowercase_paths: bool = True`
- `trailing_slash: "always" | "never" | "preserve" = "never"`
- `collapse_duplicate_slashes: bool = True`
- `strip_tracking_params: bool = True`
- `allowed_query_params: list[str] = []`

## SEOConfig

- `canonical_host: str`
- `public_base_url: str`
- `url_policy: URLPolicy`
- `default_robots: str = "index,follow"`
- `default_og_image: str | None = None`
- `site_name: str | None = None`
- `title_template: str | None = "{title}"`
- `search_robots: str = "noindex,follow"`

## SEOEntity

- `entity_type: "home" | "post" | "page" | "video" | "taxonomy" | "search" | "other"`
- `slug: str | None`
- `title: str | None`
- `excerpt: str | None`
- `body_html: str | None`
- `status: str | None`
- `featured_image: str | None`
- `published_at: str | None`
- `updated_at: str | None`

## SEOOverrides

- `meta_title: str | None`
- `meta_description: str | None`
- `canonical_url: str | None`
- `robots: str | None`
- `og_title: str | None`
- `og_description: str | None`
- `og_image: str | None`
- `twitter_card: str | None`
- `twitter_title: str | None`
- `twitter_description: str | None`
- `twitter_image: str | None`
- `schema_jsonld: dict | list[dict] | None`

## Functions

- `normalize_path(path: str, policy: URLPolicy) -> str`
- `normalize_public_url(url_or_path: str, config: SEOConfig) -> str`
- `build_seo_payload(entity: SEOEntity, route_path: str, config: SEOConfig, overrides: SEOOverrides | None = None) -> dict`
