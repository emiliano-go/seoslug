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
    # Exceptions
    SEOError,
    SEOConfigError,
    SEOEntityError,
    URLPolicyError,
    SEOPayloadError,
    # Hooks
    hook,
    register_hook,
    clear_hooks,
    get_registered_hooks,
    run_hooks,
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

Raises SEOPayloadError for empty input or malformed URLs.

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
Raises URLPolicyError for non-string input.

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

## Exceptions

All seoslug exceptions inherit from `SEOError`, which itself inherits from both `Exception` and `ValueError`. This means existing code catching `ValueError` will continue to work.

### SEOError

```python
seoslug.exceptions.SEOError
```

Base exception for all seoslug errors. Inherits from `Exception` and `ValueError`.

### SEOConfigError

```python
seoslug.exceptions.SEOConfigError
```

Raised when an `SEOConfig` or `URLPolicy` field fails validation.
For example: `canonical_host` contains a scheme or path, `title_template` is missing the `{title}` placeholder, or a required field is empty.

### SEOEntityError

```python
seoslug.exceptions.SEOEntityError
```

Raised when an `SEOEntity` or `SEOOverrides` field fails validation.
For example: `entity_type` is not a valid type, `schema_jsonld` is an invalid type, or a string field receives a non-string value.

### URLPolicyError

```python
seoslug.exceptions.URLPolicyError
```

Raised when a `URLPolicy` field fails validation or a path argument is not a string.
For example: `trailing_slash` is set to an invalid value, or `normalize_path` receives non-string input.

### SEOPayloadError

```python
seoslug.exceptions.SEOPayloadError
```

Raised during payload generation or text processing.
For example: `normalize_public_url` receives empty or malformed input, or `html_to_text` receives a non-string argument.

## Hooks

Hooks let you register callback functions that transform the SEO payload after it is built. See the [Hooks guide](hooks.md) for full documentation.

### hook

```python
hook(name: str) -> Callable
```

Decorator that registers a function to run when a named hook point is triggered.

```python
from seoslug import hook

@hook("post_process")
def add_breadcrumb(payload, entity, config):
    payload["breadcrumb"] = {"@type": "BreadcrumbList", ...}
    return payload
```

### register_hook

```python
register_hook(name: str, fn: Callable) -> None
```

Programmatic equivalent of the `@hook` decorator.

### clear_hooks

```python
clear_hooks(name: str | None = None) -> None
```

Remove all hooks registered under *name*, or all hooks if *name* is `None`.

### get_registered_hooks

```python
get_registered_hooks() -> dict[str, list[Callable]]
```

Return a copy of all registered hooks keyed by hook point name. Useful for inspection and testing.

### run_hooks

```python
run_hooks(name, payload, entity, config) -> dict
```

Run all hooks registered under *name* in registration order. Each hook receives the current payload and must return the (possibly modified) payload. Typically not called directly — `build_seo_payload` already calls `run_hooks("post_process", ...)` after building the payload.
