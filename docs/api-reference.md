# API reference

Complete reference for all public classes, functions, and dataclasses.

## Public imports

```python
from seoslug import (
    SEOConfig,
    URLPolicy,
    SEOEntity,
    SEOEntityBuilder,
    SEOOverrides,
    OGImage,
    Breadcrumb,
    FAQItem,
    Robots,
    SchemaRegistry,
    normalize_public_url,
    normalize_path,
    build_seo_payload,
    build_seo_payload_dict,
    build_seo_payload_async,
    from_blog_post,
    from_product,
    from_faq,
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

---

## build_seo_payload

```python
def build_seo_payload(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
) -> SEOPayload
```

The main entry point. Returns a `SEOPayload` dataclass with every SEO
field resolved through the fallback chain.

| Parameter | Description |
|---|---|
| `entity` | Content entity with title, excerpt, images, schema fields |
| `route_path` | URL path for this content (e.g. `/blog/my-post`) |
| `config` | Site-wide configuration (host, URL policy, defaults) |
| `overrides` | Optional per-call overrides for any field |

Raises `ValueError` if any input fails validation. Emits `warnings.warn`
for best-practice violations when `config.emit_warnings` is `True`.

---

## build_seo_payload_dict

```python
def build_seo_payload_dict(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
) -> dict
```

Same as `build_seo_payload` but returns a plain `dict` instead of a
`SEOPayload` dataclass. Convenient for template engines and JSON
serialization pipelines that expect a raw dictionary.

```python
payload_dict = build_seo_payload_dict(entity, "/post", config)
payload_dict["title"]   # "My Post"
payload_dict["og"]["type"]  # "article"
```

---

## build_seo_payload_async

```python
from seoslug.async_builder import build_seo_payload_async

async def build_seo_payload_async(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
    executor: ThreadPoolExecutor | None = None,
) -> SEOPayload
```

Async version of `build_seo_payload`. Offloads the synchronous builder
to a thread pool executor so it does not block the asyncio event loop.

| Parameter | Description |
|---|---|
| `executor` | Optional `ThreadPoolExecutor`. Defaults to a module-level executor with 4 workers |

```python
payload = await build_seo_payload_async(entity, "/post", config)
```

Use `set_executor(None)` to reset to the default 4-worker executor.

---

## normalize_public_url

```python
def normalize_public_url(
    url_or_path: str,
    config: SEOConfig,
) -> str
```

Normalizes a URL or path to a canonical absolute URL. Enforces the
canonical host, HTTPS scheme, trailing slash policy, and query filtering.

| Parameter | Description |
|---|---|
| `url_or_path` | Absolute URL or relative path (e.g. `/blog/post` or `https://...`) |
| `config` | `SEOConfig` with canonical host, URL policy, and public base URL |

Accepts both absolute URLs and relative paths. Relative paths are resolved
against `config.public_base_url`. If `public_base_url` has a sub-path
(e.g. `/blog/`), it is prepended to the route path.

Raises `SEOPayloadError` for empty input, malformed URLs, or invalid schemes.

---

## normalize_path

```python
def normalize_path(
    path: str,
    policy: URLPolicy,
) -> str
```

Normalizes a URL path without host or scheme. Applies lowercase,
trailing slash, and duplicate-slash rules. Always returns a path
starting with `/`.

| Parameter | Description |
|---|---|
| `path` | URL path string (e.g. `"/Blog//Post"`) |
| `policy` | `URLPolicy` controlling normalization behavior |

```python
normalize_path("/Blog//Post", URLPolicy())
# "/blog/post"
```

Raises `URLPolicyError` for non-string input.

---

## SEOConfig

```python
@dataclass(slots=True)
class SEOConfig:
    canonical_host: str
    public_base_url: str
    url_policy: URLPolicy
    default_robots: str | Robots = "index,follow"
    default_og_image: str | OGImage | None = None
    site_name: str | None = None
    title_template: str | None = "{title}"
    search_robots: str | Robots = "noindex,follow"
    schema_type_map: dict[str, str | None]
    auto_generate_schema: bool = True
    publisher_name: str | None = None
    publisher_logo: str | None = None
    locale: str | None = None
    locale_alternate: list[str] | None = None
    twitter_site: str | None = None
    schema_registry: SchemaRegistry | None = None
    emit_warnings: bool = False
```

Site-wide configuration for SEO metadata generation. Validates all input
in `__post_init__`.

| Field | Type | Default | Description |
|---|---|---|---|
| `canonical_host` | `str` | required | Hostname for all canonical URLs (host-only, no scheme/path/port) |
| `public_base_url` | `str` | required | Full absolute URL of deployment (used as base for URL resolution) |
| `url_policy` | `URLPolicy` | required | URL normalization rules |
| `default_robots` | `str \| Robots` | `"index,follow"` | Fallback robots directive |
| `default_og_image` | `str \| OGImage \| None` | `None` | Fallback OG image |
| `site_name` | `str \| None` | `None` | `og:site_name` value |
| `title_template` | `str \| None` | `"{title}"` | Template string; must contain `{title}` |
| `search_robots` | `str \| Robots` | `"noindex,follow"` | Robots for `entity_type="search"` |
| `schema_type_map` | `dict[str, str \| None]` | built-in map | Maps entity_type to schema.org type |
| `auto_generate_schema` | `bool` | `True` | Auto-generate JSON-LD schema |
| `publisher_name` | `str \| None` | `None` | Publisher name for JSON-LD |
| `publisher_logo` | `str \| None` | `None` | Publisher logo URL for JSON-LD |
| `locale` | `str \| None` | `None` | `og:locale` value |
| `locale_alternate` | `list[str] \| None` | `None` | `og:locale:alternate` values |
| `twitter_site` | `str \| None` | `None` | `twitter:site` value |
| `schema_registry` | `SchemaRegistry \| None` | `None` | Custom schema generators |
| `emit_warnings` | `bool` | `False` | Emit `warnings.warn` for validation issues |

Default `schema_type_map`:

```python
{
    "post": "Article",
    "page": "WebPage",
    "video": "VideoObject",
    "home": "WebPage",
    "taxonomy": "CollectionPage",
    "search": "SearchResultsPage",
    "product": "Product",
    "organization": "Organization",
    "local_business": "LocalBusiness",
    "faq": "FAQPage",
}
```

Validation rules:

- `canonical_host` must be host-only (no scheme, path, port, query, or
  trailing dot). IPv6 not supported.
- `public_base_url` must be an absolute `http` or `https` URL.
- `title_template` must include the `{title}` placeholder.
- `locale_alternate` items are deduplicated and stripped.
- `url_policy` must be a `URLPolicy` instance.

---

## URLPolicy

```python
@dataclass(slots=True)
class URLPolicy:
    enforce_https: bool = True
    lowercase_paths: bool = True
    trailing_slash: Literal["always", "never", "preserve"] = "never"
    collapse_duplicate_slashes: bool = True
    strip_tracking_params: bool = True
    allowed_query_params: list[str] = field(default_factory=list)
```

Controls URL normalization behavior.

| Field | Type | Default | Description |
|---|---|---|---|
| `enforce_https` | `bool` | `True` | Upgrade all canonical URLs to HTTPS |
| `lowercase_paths` | `bool` | `True` | Lowercase URL paths |
| `trailing_slash` | `Literal` | `"never"` | Trailing slash policy: `"always"`, `"never"`, or `"preserve"` |
| `collapse_duplicate_slashes` | `bool` | `True` | Collapse `//` to `/` in paths |
| `strip_tracking_params` | `bool` | `True` | Remove tracking parameters (uses detrack if available, built-in regex otherwise) |
| `allowed_query_params` | `list[str]` | `[]` | Query params to preserve (all others stripped when non-empty) |

Validation:

- `trailing_slash` must be one of `"always"`, `"never"`, `"preserve"`.
- `allowed_query_params` is deduplicated; empty strings are removed.

---

## SEOEntity

```python
@dataclass(slots=True)
class SEOEntity:
    entity_type: Literal["home", "post", "page", "video", "taxonomy", "search", "other",
                         "product", "organization", "local_business", "faq"]
    slug: str | None = None
    title: str | None = None
    excerpt: str | None = None
    body_html: str | None = None
    status: str | None = None
    featured_image: str | OGImage | None = None
    published_at: str | None = None
    updated_at: str | None = None
    author_name: str | None = None
    breadcrumbs: list[Breadcrumb] | None = None
    sku: str | None = None
    price: str | None = None
    price_currency: str | None = None
    availability: str | None = None
    same_as: list[str] | None = None
    address: str | None = None
    faq_items: list[FAQItem] | None = None
```

Input data for a content entity.

| Field | Type | Used in | Description |
|---|---|---|---|
| `entity_type` | `Literal` | meta + schema | Content type; determines OG type and schema mapping |
| `slug` | `str \| None` | metadata only | URL slug (informational, not used in output) |
| `title` | `str \| None` | meta + schema | Page title |
| `excerpt` | `str \| None` | meta | Meta description source |
| `body_html` | `str \| None` | meta | Body HTML for auto-generated description snippet |
| `status` | `str \| None` | meta | Content status; `"published"` sets robots to `index,follow` |
| `featured_image` | `str \| OGImage \| None` | meta + schema | Featured image (string URL or structured OGImage) |
| `published_at` | `str \| None` | schema only | ISO date for `datePublished` |
| `updated_at` | `str \| None` | schema only | ISO date for `dateModified` |
| `author_name` | `str \| None` | schema only | Author name for JSON-LD |
| `breadcrumbs` | `list[Breadcrumb] \| None` | schema only | Breadcrumb trail; generates BreadcrumbList |
| `sku` | `str \| None` | schema only | SKU for Product schema |
| `price` | `str \| None` | schema only | Price for Product schema |
| `price_currency` | `str \| None` | schema only | ISO 4217 currency code |
| `availability` | `str \| None` | schema only | Schema.org availability (e.g. `"InStock"`) |
| `same_as` | `list[str] \| None` | schema only | SameAs URLs for Organization |
| `address` | `str \| None` | schema only | Street address for LocalBusiness |
| `faq_items` | `list[FAQItem] \| None` | schema only | Q&A pairs for FAQPage schema |

Validation:

- `entity_type` must be one of the 11 accepted values.
- All optional string fields are normalized (stripped; empty strings
  become `None`).
- `featured_image` accepts a string URL or `OGImage` instance.
- `same_as` is deduplicated; empty strings removed.

---

## SEOOverrides

```python
@dataclass(slots=True)
class SEOOverrides:
    meta_title: str | None = None
    meta_description: str | None = None
    canonical_url: str | None = None
    robots: str | Robots | None = None
    og_title: str | None = None
    og_description: str | None = None
    og_image: str | OGImage | None = None
    twitter_card: str | None = None
    twitter_title: str | None = None
    twitter_description: str | None = None
    twitter_image: str | OGImage | None = None
    schema_jsonld: dict | list[dict] | None = None
    omit_schema: bool = False
    skip_title_template: bool = False
    twitter_creator: str | None = None
    og_audio: str | None = None
    og_video: str | None = None
```

Per-entity overrides for SEO metadata. Takes highest priority in each
fallback chain.

| Field | Type | Default | Description |
|---|---|---|---|
| `meta_title` | `str \| None` | `None` | Override page title |
| `meta_description` | `str \| None` | `None` | Override meta description |
| `canonical_url` | `str \| None` | `None` | Override canonical URL (absolute) |
| `robots` | `str \| Robots \| None` | `None` | Override robots directive |
| `og_title` | `str \| None` | `None` | Override `og:title` |
| `og_description` | `str \| None` | `None` | Override `og:description` |
| `og_image` | `str \| OGImage \| None` | `None` | Override `og:image` (string URL or structured) |
| `twitter_card` | `str \| None` | `None` | Override `twitter:card` type |
| `twitter_title` | `str \| None` | `None` | Override `twitter:title` |
| `twitter_description` | `str \| None` | `None` | Override `twitter:description` |
| `twitter_image` | `str \| OGImage \| None` | `None` | Override `twitter:image` |
| `schema_jsonld` | `dict \| list[dict] \| None` | `None` | Override entire JSON-LD schema |
| `omit_schema` | `bool` | `False` | Remove `schema_jsonld` from output |
| `skip_title_template` | `bool` | `False` | Bypass `title_template` for this entity |
| `twitter_creator` | `str \| None` | `None` | Set `twitter:creator` |
| `og_audio` | `str \| None` | `None` | Set `og:audio` URL |
| `og_video` | `str \| None` | `None` | Set `og:video` URL |

Usage:

```python
overrides = SEOOverrides(
    meta_title="Custom Title",
    skip_title_template=True,
    twitter_creator="@author",
    omit_schema=True,
)
```

---

## OGImage

```python
@dataclass(slots=True)
class OGImage:
    url: str
    width: int | None = None
    height: int | None = None
    alt: str | None = None
```

Structured Open Graph image with optional dimensions and alt text.

| Field | Type | Description |
|---|---|---|
| `url` | `str` | Image URL (required, non-empty) |
| `width` | `int \| None` | `og:image:width` |
| `height` | `int \| None` | `og:image:height` |
| `alt` | `str \| None` | `og:image:alt` |

---

## Breadcrumb

```python
@dataclass(slots=True)
class Breadcrumb:
    name: str
    url: str
```

A single breadcrumb trail entry.

| Field | Type | Description |
|---|---|---|
| `name` | `str` | Display name (required, non-empty) |
| `url` | `str` | URL or path (required, non-empty; normalized when generating BreadcrumbList) |

---

## FAQItem

```python
@dataclass(slots=True)
class FAQItem:
    question: str
    answer: str
```

A single FAQ question-and-answer pair.

| Field | Type | Description |
|---|---|---|
| `question` | `str` | Question text (required, non-empty) |
| `answer` | `str` | Answer text (required, non-empty) |

---

## Robots

```python
@dataclass(slots=True)
class Robots:
    index: bool = True
    follow: bool = True
    max_snippet: int | None = None
    max_image_preview: str | None = None
    max_video_preview: int | None = None
```

Structured robots directive. Serializes to the standard robots meta content
string via `.serialize()`.

| Field | Type | Default | Description |
|---|---|---|---|
| `index` | `bool` | `True` | `index` or `noindex` |
| `follow` | `bool` | `True` | `follow` or `nofollow` |
| `max_snippet` | `int \| None` | `None` | `max-snippet:N` |
| `max_image_preview` | `str \| None` | `None` | `max-image-preview:VALUE` |
| `max_video_preview` | `int \| None` | `None` | `max-video-preview:N` |

```python
robots = Robots(index=True, follow=False, max_snippet=160)
robots.serialize()  # "index,nofollow,max-snippet:160"
```

---

## SchemaRegistry

```python
class SchemaRegistry:
    def __init__(self) -> None: ...
    def register(self, schema_type: str, generator: SchemaGenerator) -> None: ...
    def unregister(self, schema_type: str) -> None: ...
    def get(self, schema_type: str) -> SchemaGenerator | None: ...
```

Registry for user-registered schema generators.

```python
from seoslug import SchemaRegistry

registry = SchemaRegistry()
registry.register("Podcast", lambda entity, config, canonical, title, description, og_image: {
    "@context": "https://schema.org",
    "@type": "Podcast",
    "name": title,
    "url": canonical,
})
```

Register a generator for any schema type name. When `build_schema`
encounters a type registered here, it calls the generator instead of the
built-in builder.

| Method | Parameters | Description |
|---|---|---|
| `register` | `schema_type: str`, `generator: SchemaGenerator` | Register a generator for a schema type |
| `unregister` | `schema_type: str` | Remove a registered generator |
| `get` | `schema_type: str` | Look up a generator by type (returns `None` if not found) |

`SchemaGenerator` protocol:

```python
class SchemaGenerator(Protocol):
    def __call__(
        self,
        entity: SEOEntity,
        config: SEOConfig,
        canonical: str,
        title: str,
        description: str | None,
        og_image: str | None,
    ) -> dict | None: ...
```

---

## SEOEntityBuilder

```python
class SEOEntityBuilder:
    def __init__(self) -> None: ...
    def entity_type(self, value: str) -> SEOEntityBuilder: ...
    def slug(self, value: str) -> SEOEntityBuilder: ...
    def title(self, value: str) -> SEOEntityBuilder: ...
    def excerpt(self, value: str) -> SEOEntityBuilder: ...
    def body_html(self, value: str) -> SEOEntityBuilder: ...
    def status(self, value: str) -> SEOEntityBuilder: ...
    def featured_image(self, value: str | OGImage) -> SEOEntityBuilder: ...
    def published_at(self, value: str) -> SEOEntityBuilder: ...
    def updated_at(self, value: str) -> SEOEntityBuilder: ...
    def author_name(self, value: str) -> SEOEntityBuilder: ...
    def breadcrumbs(self, value: list[Breadcrumb]) -> SEOEntityBuilder: ...
    def sku(self, value: str) -> SEOEntityBuilder: ...
    def price(self, value: str | float) -> SEOEntityBuilder: ...
    def price_currency(self, value: str) -> SEOEntityBuilder: ...
    def availability(self, value: str) -> SEOEntityBuilder: ...
    def same_as(self, value: list[str]) -> SEOEntityBuilder: ...
    def address(self, value: str) -> SEOEntityBuilder: ...
    def faq_items(self, value: list[FAQItem]) -> SEOEntityBuilder: ...
    def build(self) -> SEOEntity: ...
```

Fluent builder for `SEOEntity`. Every setter returns `self` for chaining.

```python
entity = (
    SEOEntityBuilder()
    .entity_type("product")
    .title("Widget")
    .sku("W-001")
    .price(29.99)
    .availability("InStock")
    .build()
)
```

All methods accept the same types as the corresponding `SEOEntity` field.
`price()` accepts `str` or `float` (converted to `str`). `.build()` raises
`ValueError` if `entity_type` was not set.

---

## Factory functions

```python
from seoslug import from_blog_post, from_product, from_faq
```

Convenience factories that create `SEOEntity` instances for common content
types.

### from_blog_post

```python
def from_blog_post(
    title: str,
    body_html: str,
    slug: str | None = None,
    author: str = "",
    excerpt: str | None = None,
    breadcrumbs: list[dict] | None = None,
) -> SEOEntity
```

Creates a blog post entity. Sets `entity_type="post"` and `status="published"`.

| Parameter | Type | Description |
|---|---|---|
| `title` | `str` | Post title |
| `body_html` | `str` | Full HTML body (used for auto-generated description) |
| `slug` | `str \| None` | URL slug (optional) |
| `author` | `str` | Author name (optional, empty string becomes `None`) |
| `excerpt` | `str \| None` | Explicit excerpt; falls back to body snippet when `None` |
| `breadcrumbs` | `list[dict] \| None` | List of `{"name": ..., "url": ...}` dicts |

```python
entity = from_blog_post(
    title="Hello World",
    body_html="<p>Content</p>",
    author="Jane",
    breadcrumbs=[{"name": "Blog", "url": "/blog"}],
)
```

### from_product

```python
def from_product(
    name: str,
    sku: str,
    price: str | float,
    currency: str = "USD",
    availability: str = "InStock",
    description: str | None = None,
    breadcrumbs: list[dict] | None = None,
) -> SEOEntity
```

Creates a product entity. Sets `entity_type="product"` and
`status="published"`.

| Parameter | Type | Description |
|---|---|---|
| `name` | `str` | Product name |
| `sku` | `str` | Stock-keeping unit |
| `price` | `str \| float` | Price as string (`"29.99"`) or numeric |
| `currency` | `str` | ISO 4217 currency code (default `"USD"`) |
| `availability` | `str` | Schema.org availability (default `"InStock"`) |
| `description` | `str \| None` | Optional product description (excerpt) |
| `breadcrumbs` | `list[dict] \| None` | List of `{"name": ..., "url": ...}` dicts |

### from_faq

```python
def from_faq(
    questions: list[dict[str, str]],
    title: str = "FAQ",
    description: str | None = None,
    breadcrumbs: list[dict] | None = None,
) -> SEOEntity
```

Creates an FAQ page entity. Sets `entity_type="faq"` and
`status="published"`.

| Parameter | Type | Description |
|---|---|---|
| `questions` | `list[dict[str, str]]` | List of `{"question": "...", "answer": "..."}` dicts |
| `title` | `str` | Page title (default `"FAQ"`) |
| `description` | `str \| None` | Optional meta description |
| `breadcrumbs` | `list[dict] \| None` | List of `{"name": ..., "url": ...}` dicts |

---

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

---

## SEOPayload

```python
@dataclass(eq=False)
class SEOPayload:
    title: str
    description: str
    canonical: str
    robots: str
    og: OGPayload
    twitter: TwitterPayload
    schema_jsonld: dict | list[dict] | None = None
```

Return type of `build_seo_payload`. Supports attribute access and
dict-style access (`payload["title"]`, `payload["og"]["type"]`).

| Field | Type | Description |
|---|---|---|
| `title` | `str` | Resolved page title (with template applied) |
| `description` | `str` | Resolved meta description |
| `canonical` | `str` | Fully normalized canonical URL |
| `robots` | `str` | Robots meta content string |
| `og` | `OGPayload` | Nested Open Graph payload |
| `twitter` | `TwitterPayload` | Nested Twitter Card payload |
| `schema_jsonld` | `dict \| list[dict] \| None` | JSON-LD structured data (single dict or array of dicts) |

Methods:

| Method | Returns | Description |
|---|---|---|
| `to_dict()` | `dict` | Converts to a plain dict; drops `None` values from nested payloads |
| `render_html()` | `str` | Render full `<head>` HTML snippet with all meta tags, OG, Twitter, and JSON-LD |
| `hash()` | `str` | Deterministic SHA-256 hex digest of the serialized payload |
| `etag()` | `str` | Quoted hex string suitable for the HTTP `ETag` header |

Dict-style methods: `get(key)`, `keys()`, `__contains__` (checks value is
not `None`).

---

## OGPayload

```python
@dataclass(eq=False)
class OGPayload:
    type: str
    title: str | None
    description: str | None
    url: str | None
    image: str | None
    image_width: int | None = None
    image_height: int | None = None
    image_alt: str | None = None
    site_name: str | None = None
    locale: str | None = None
    locale_alternate: list[str] | None = None
    audio: str | None = None
    video: str | None = None
```

Nested Open Graph payload. Supports dict-style access with colon-separated
keys: `payload["og"]["image:width"]`.

| Field | Dict key | Description |
|---|---|---|
| `type` | `type` | OG type (`article` or `website`) |
| `title` | `title` | `og:title` |
| `description` | `description` | `og:description` |
| `url` | `url` | `og:url` (same as canonical) |
| `image` | `image` | `og:image` URL |
| `image_width` | `image:width` | `og:image:width` |
| `image_height` | `image:height` | `og:image:height` |
| `image_alt` | `image:alt` | `og:image:alt` |
| `site_name` | `site_name` | `og:site_name` |
| `locale` | `locale` | `og:locale` |
| `locale_alternate` | `locale:alternate` | `og:locale:alternate` |
| `audio` | `audio` | `og:audio` URL |
| `video` | `video` | `og:video` URL |

Methods: `to_dict()`, `get(key)`, `keys()`, `__contains__`.

---

## TwitterPayload

```python
@dataclass(eq=False)
class TwitterPayload:
    card: str
    title: str | None
    description: str | None
    image: str | None
    image_alt: str | None = None
    site: str | None = None
    creator: str | None = None
```

Nested Twitter Card payload. Supports dict-style access with colon-separated
keys: `payload["twitter"]["image:alt"]`.

| Field | Dict key | Description |
|---|---|---|
| `card` | `card` | `twitter:card` type |
| `title` | `title` | `twitter:title` |
| `description` | `description` | `twitter:description` |
| `image` | `image` | `twitter:image` URL |
| `image_alt` | `image:alt` | `twitter:image:alt` |
| `site` | `site` | `twitter:site` |
| `creator` | `creator` | `twitter:creator` |

Methods: `to_dict()`, `get(key)`, `keys()`, `__contains__`.

---

## TypedDict variants

For type-checking compatibility with code that expects plain dicts:

```python
from seoslug.payload import SEOPayloadTypedDict, OGPayloadTypedDict, TwitterPayloadTypedDict
```

These are `TypedDict` versions of the payload dataclasses. Use them for
type annotations when working with `build_seo_payload_dict` or
`payload.to_dict()`.
