# SEOConfig reference

`SEOConfig` is the global configuration object. You create one per site and pass it to every `build_seo_payload` call.

## Fields

| Option | Type | Default | Description |
|---|---|---|---|
| `canonical_host` | `str` | required | Hostname for all canonical URLs. Host only, no scheme or path. |
| `public_base_url` | `str` | required | Full absolute URL of the deployment. Path is used as base for sub-path deployments. |
| `url_policy` | `URLPolicy` | required | URL normalization rules. |
| `default_robots` | `str` or `Robots` | `"index,follow"` | Robots directive for non-published, non-search content. |
| `default_og_image` | `str` or `OGImage` or `None` | `None` | Fallback OG image when the entity has none. |
| `site_name` | `str` or `None` | `None` | Site name for `og:site_name`. |
| `title_template` | `str` or `None` | `"{title}"` | Template string. Must include the `{title}` placeholder. |
| `search_robots` | `str` or `Robots` | `"noindex,follow"` | Robots directive for search result pages. |
| `schema_type_map` | `dict[str, str\|None]` | see below | Maps entity types to schema.org types. Set `None` to disable schema for a type. |
| `auto_generate_schema` | `bool` | `True` | Enable automatic JSON-LD generation. |
| `publisher_name` | `str` or `None` | `None` | Publisher name for Article schema (adds `publisher` field). |
| `publisher_logo` | `str` or `None` | `None` | Publisher logo URL. Only used when `publisher_name` is set. |
| `locale` | `str` or `None` | `None` | Locale for `og:locale` (e.g. `"en_US"`). |
| `locale_alternate` | `list[str]` or `None` | `None` | Alternate locales for `og:locale:alternate`. |
| `twitter_site` | `str` or `None` | `None` | Twitter username for `twitter:site` (include the `@`). |
| `schema_registry` | `SchemaRegistry` or `None` | `None` | Registry for custom schema generators. |
| `emit_warnings` | `bool` | `False` | Emit Python warnings for SEO validation issues. |

### canonical_host (required)

The domain for all canonical URLs. Must be a bare hostname with no scheme, path, port, or query string.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

Valid: `"blog.example.com"`, `"example.com"`  
Invalid: `"https://blog.example.com"`, `"blog.example.com/blog"`, `"blog.example.com:8080"`

### public_base_url (required)

The full absolute URL of your deployment, including scheme and optional path. Used by the URL pipeline to build canonical URLs.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

Must be an absolute `http://` or `https://` URL. The path component becomes the base path for sub-path deployments.

### url_policy (required)

A `URLPolicy` instance that controls URL normalization. See the [URLPolicy reference](url-policy.md) for all options.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(trailing_slash="always"),
)
```

### default_robots

Default robots directive for content that is not published and not search results. Accepts a plain string or a structured `Robots` dataclass.

```python
# String form
SEOConfig(
    ...,
    default_robots="noindex,nofollow",
)

# Structured form
from seoslug import Robots

SEOConfig(
    ...,
    default_robots=Robots(index=False, follow=False, max_snippet=100),
)
```

### default_og_image

Fallback Open Graph image. Used when the entity has no `featured_image` and no override is provided. Accepts a plain URL string or a structured `OGImage` dataclass with dimensions and alt text.

```python
# String form
SEOConfig(
    ...,
    default_og_image="https://cdn.example.com/default.jpg",
)

# Structured form
from seoslug import OGImage

SEOConfig(
    ...,
    default_og_image=OGImage(
        url="https://cdn.example.com/default.jpg",
        width=1200,
        height=630,
        alt="Default site image",
    ),
)
```

When structured, the width, height, and alt are emitted as `og:image:width`, `og:image:height`, and `og:image:alt`.

### site_name

Displayed as `og:site_name` in the Open Graph payload.

```python
SEOConfig(
    ...,
    site_name="My Blog",
)
```

### title_template

Template for the `<title>` tag. Must contain the `{title}` placeholder, which is replaced with the resolved entity title. Defaults to `"{title}"` (passthrough).

```python
SEOConfig(
    ...,
    title_template="{title} - My Blog",
)

# Result: "My Post - My Blog"
```

### search_robots

Robots directive for pages with `entity_type="search"`. Same type flexibility as `default_robots`; accepts `str` or `Robots`.

```python
SEOConfig(
    ...,
    search_robots="noindex,nofollow",
)
```

### schema_type_map

Maps each entity type to a schema.org `@type`. Set a value to `None` to skip schema generation for that type. The default map:

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

Override any type to customize:

```python
SEOConfig(
    ...,
    schema_type_map={
        "post": "BlogPosting",
        "product": None,  # disable schema for products
    },
)
```

### auto_generate_schema

Set to `False` to disable automatic JSON-LD generation globally. You can still inject schema via `SEOOverrides.schema_jsonld` per call.

```python
SEOConfig(
    ...,
    auto_generate_schema=False,
)
```

### publisher_name

Adds a `publisher` field to Article-type JSON-LD schemas. The publisher is rendered as an `Organization` with the given name.

```python
SEOConfig(
    ...,
    publisher_name="My Company",
)
```

### publisher_logo

Logo URL for the publisher. Only included when `publisher_name` is also set.

```python
SEOConfig(
    ...,
    publisher_name="My Company",
    publisher_logo="https://cdn.example.com/logo.png",
)
```

### locale

Sets `og:locale` on every page. Use standard locale codes like `"en_US"` or `"fr_FR"`.

```python
SEOConfig(
    ...,
    locale="en_US",
)
```

### locale_alternate

List of alternate locales for `og:locale:alternate`. Only emitted when `locale` is also set.

```python
SEOConfig(
    ...,
    locale="en_US",
    locale_alternate=["es_ES", "fr_FR"],
)
```

Output:

```html
<meta property="og:locale" content="en_US">
<meta property="og:locale:alternate" content="es_ES">
<meta property="og:locale:alternate" content="fr_FR">
```

### twitter_site

Twitter username for `twitter:site`. Include the `@` symbol.

```python
SEOConfig(
    ...,
    twitter_site="@myblog",
)
```

### schema_registry

A `SchemaRegistry` instance that lets you register custom JSON-LD generators. When a schema type appears in the registry, seoslug calls your generator instead of the built-in builder.

```python
from seoslug import SchemaRegistry

registry = SchemaRegistry()
registry.register("Podcast", lambda entity, config, canonical, title, description, og_image: {
    "@context": "https://schema.org",
    "@type": "Podcast",
    "name": title,
    "url": canonical,
})

SEOConfig(
    ...,
    schema_type_map={"other": "Podcast"},
    schema_registry=registry,
)
```

### emit_warnings

When `True`, seoslug calls `warnings.warn()` for non-fatal SEO issues after every payload build. Useful during development and CI. Warnings include:

- Title exceeds 60 characters
- Description exceeds 160 characters  
- Canonical URL is not absolute
- OG image URL is not absolute
- Robots directive may be malformed

```python
import warnings
warnings.filterwarnings("always")

SEOConfig(
    ...,
    emit_warnings=True,
)
```

## Sub-path deployments

When your site runs under a path prefix (e.g. `https://example.com/blog/`), set `public_base_url` with the full path. The URL pipeline prepends the path to every canonical URL.

```python
SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com/blog/",
    url_policy=URLPolicy(),
)
```

A route path of `/my-post` produces the canonical URL `https://example.com/blog/my-post`.

The path from `public_base_url` is also used as the base for breadcrumb item URLs and any relative path normalization.

```python
# /my-post → https://example.com/blog/my-post
# /category/seo → https://example.com/blog/category/seo
```

## Default schema_type_map

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
