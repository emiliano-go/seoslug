---
seo:
  title: Getting started - seoslug
  canonical: https://seoslug.emiliano-go.com/getting-started/
  robots: index,follow
  og:
    type: website
    title: Getting started - seoslug
    description: Install seoslug, configure your site, define your first entity, generate
      a payload, and inject it into an HTML template.
    url: https://seoslug.emiliano-go.com/getting-started/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Getting started - seoslug
    description: Install seoslug, configure your site, define your first entity, generate
      a payload, and inject it into an HTML template.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: Install seoslug, configure your site, define your first entity, generate
    a payload, and inject it into an HTML template.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Getting started - seoslug
    url: https://seoslug.emiliano-go.com/getting-started/
    description: Install seoslug, configure your site, define your first entity, generate
      a payload, and inject it into an HTML template.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Getting started - seoslug</title>\n<meta name=\"description\" content=\"\
  Install seoslug, configure your site, define your first entity, generate a payload,\
  \ and inject it into an HTML template.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/getting-started/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Getting started - seoslug\">\n\
  <meta property=\"og:description\" content=\"Install seoslug, configure your site,\
  \ define your first entity, generate a payload, and inject it into an HTML template.\"\
  >\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/getting-started/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Getting started - seoslug\">\n<meta name=\"\
  twitter:description\" content=\"Install seoslug, configure your site, define your\
  \ first entity, generate a payload, and inject it into an HTML template.\">\n<meta\
  \ name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Getting started - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/getting-started/\"\
  ,\n  \"description\": \"Install seoslug, configure your site, define your first\
  \ entity, generate a payload, and inject it into an HTML template.\",\n  \"image\"\
  : \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n  \"publisher\"\
  : {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano Gandini Outeda\"\
  ,\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\n\
  \  }\n}\n</script>\n"
---

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
