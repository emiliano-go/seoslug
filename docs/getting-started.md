# Getting started

Install seoslug, configure your site, define your first entity, generate a
payload, and inject it into an HTML template.

## 1. Install

```bash
pip install "seoslug[fast]"
```

Requires Python 3.10 or later. The `[fast]` extras include **lxml**
(C-optimized HTML parsing) and **detrack** (tracking-parameter stripping).

For a minimal footprint with pure-Python fallbacks:

```bash
pip install "seoslug[light]"
```

Output is identical. Performance may differ for very large HTML bodies.

## 2. Configure

Create a `SEOConfig` with your canonical host, public base URL, and URL
policy. This defines the site-wide SEO rules.

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
    ),
)
```

| Field | Purpose |
|---|---|
| `canonical_host` | Hostname for all output canonical URLs (host-only, no scheme/path/port) |
| `public_base_url` | Full absolute URL of the deployment; its path becomes the base path |
| `url_policy` | Controls how URLs are normalized (HTTPS, slash policy, query filtering) |

## 3. Define an entity

An `SEOEntity` represents a single piece of content. It holds the data
seoslug needs to generate all meta tags and JSON-LD.

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    slug="hello-world",
    title="Hello World",
    excerpt="My first post.",
    body_html="<p>Welcome to my blog.</p>",
    status="published",
)
```

`entity_type` determines the Open Graph type (`article` for "post" and
"video"; `website` for everything else) and the JSON-LD schema type (mapped
via `schema_type_map`).

## 4. Generate the payload

Call `build_seo_payload` with your entity, route path, and config.

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/posts/hello-world", config)
```

The return value is a `SEOPayload` dataclass with seven top-level attributes:

| Attribute | Type | Description |
|---|---|---|
| `title` | `str` | Page title (with optional template applied) |
| `description` | `str` | Meta description |
| `canonical` | `str` | Fully normalized canonical URL |
| `robots` | `str` | Robots meta content string |
| `og` | `OGPayload` | Nested Open Graph payload |
| `twitter` | `TwitterPayload` | Nested Twitter Card payload |
| `schema_jsonld` | `dict \| list[dict] \| None` | JSON-LD structured data |

Access values directly or convert to a dict:

```python
payload.title              # "Hello World"
payload.canonical          # "https://blog.example.com/posts/hello-world"
payload.to_dict()          # plain dict for JSON serialization

# Dict-style access also works
payload["title"]           # "Hello World"
payload["og"]["type"]      # "article"
```

If you need a plain dict instead of a dataclass:

```python
from seoslug import build_seo_payload_dict

payload_dict = build_seo_payload_dict(entity, "/posts/hello-world", config)
# payload_dict is a plain dict
```

## 5. Inject into HTML template

Pass the `SEOPayload` into your template context and render every tag:

```html
<title>{{ payload.title }}</title>
<meta name="description" content="{{ payload.description }}">
<link rel="canonical" href="{{ payload.canonical }}">
<meta name="robots" content="{{ payload.robots }}">

<!-- Open Graph -->
<meta property="og:type" content="{{ payload.og.type }}">
<meta property="og:title" content="{{ payload.og.title }}">
<meta property="og:description" content="{{ payload.og.description }}">
<meta property="og:url" content="{{ payload.og.url }}">
<meta property="og:image" content="{{ payload.og.image }}">
<meta property="og:site_name" content="{{ payload.og.site_name }}">
<meta property="og:locale" content="{{ payload.og.locale }}">

<!-- Twitter Cards -->
<meta name="twitter:card" content="{{ payload.twitter.card }}">
<meta name="twitter:title" content="{{ payload.twitter.title }}">
<meta name="twitter:description" content="{{ payload.twitter.description }}">
<meta name="twitter:image" content="{{ payload.twitter.image }}">
<meta name="twitter:site" content="{{ payload.twitter.site }}">
<meta name="twitter:creator" content="{{ payload.twitter.creator }}">

<!-- JSON-LD structured data -->
<script type="application/ld+json">
{{ payload.schema_jsonld | tojson }}
</script>
```

For templates that expect a plain dict (e.g. Jinja2 with `tojson` filter),
use `build_seo_payload_dict` or call `payload.to_dict()` before rendering.

## Next steps

- [Core Concepts](core-concepts.md) - understand determinism, pure functions,
  and the builder architecture
- [API Reference](api-reference.md) - complete function and dataclass
  reference
