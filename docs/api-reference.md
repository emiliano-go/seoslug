# API reference

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

## build_seo_payload

```python
build_seo_payload(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
) -> dict
```

The main entry point for SEO payload generation.
Returns a dictionary with title, description, canonical, robots, og, twitter, and schema_jsonld.

The route path is normalized through the URL pipeline before becoming the canonical URL.
Overrides are applied per field, taking highest precedence in each fallback chain.

## normalize_public_url

```python
normalize_public_url(
    url_or_path: str,
    config: SEOConfig,
) -> str
```

Normalizes a URL or path to a canonical absolute URL.
Enforces the canonical host, scheme, trailing slash policy, and query filtering.
Accepts both absolute URLs and relative paths.
Relative paths are resolved against the public_base_url.

Raises ValueError for empty input or malformed URLs.

## normalize_path

```python
normalize_path(
    path: str,
    policy: URLPolicy,
) -> str
```

Normalizes a URL path without host or scheme.
Applies lowercase, trailing slash, and duplicate slash rules.
Always returns a path starting with "/".
Raises ValueError for non string input.

## SEOConfig

```python
@dataclass
class SEOConfig:
    canonical_host: str
    public_base_url: str
    url_policy: URLPolicy
    default_robots: str = "index,follow"
    default_og_image: str | None = None
    site_name: str | None = None
    title_template: str | None = "{title}"
    search_robots: str = "noindex,follow"
    schema_type_map: dict[str, str | None] = field(default_factory=...)
    auto_generate_schema: bool = True
    publisher_name: str | None = None
    publisher_logo: str | None = None
```

The main configuration object.
Validates input in `__post_init__`.
`canonical_host` must be host only with no scheme or path.
`public_base_url` must be an absolute HTTP or HTTPS URL.
`title_template` must include the `{title}` placeholder.

## URLPolicy

```python
@dataclass
class URLPolicy:
    enforce_https: bool = True
    lowercase_paths: bool = True
    trailing_slash: Literal["always", "never", "preserve"] = "never"
    collapse_duplicate_slashes: bool = True
    strip_tracking_params: bool = True
    allowed_query_params: list[str] = field(default_factory=list)
```

Controls URL normalization behavior.
`trailing_slash` must be one of "always", "never", or "preserve".
`allowed_query_params` is deduplicated and empty strings are removed.
`strip_tracking_params` requires the detrack library.

## SEOEntity

```python
@dataclass
class SEOEntity:
    entity_type: Literal["home", "post", "page", "video", "taxonomy", "search", "other"]
    slug: str | None = None
    title: str | None = None
    excerpt: str | None = None
    body_html: str | None = None
    status: str | None = None
    featured_image: str | None = None
    published_at: str | None = None
    updated_at: str | None = None
    author_name: str | None = None
```

Input schema for content entities.
`entity_type` must be one of the seven accepted values.
Optional string fields are normalized: stripped whitespace, empty strings become None.

## SEOOverrides

```python
@dataclass
class SEOOverrides:
    meta_title: str | None = None
    meta_description: str | None = None
    canonical_url: str | None = None
    robots: str | None = None
    og_title: str | None = None
    og_description: str | None = None
    og_image: str | None = None
    twitter_card: str | None = None
    twitter_title: str | None = None
    twitter_description: str | None = None
    twitter_image: str | None = None
    schema_jsonld: dict | list[dict] | None = None
    omit_schema: bool = False
```

Per call overrides for SEO metadata.
`schema_jsonld` accepts a dict, list of dicts, or None.
`omit_schema` removes the schema_jsonld key from the payload.
