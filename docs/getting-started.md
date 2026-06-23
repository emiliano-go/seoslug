# Getting started

## Install

```bash
pip install seoslug
```

seoslug requires Python 3.10 or later.
Dependencies are lxml for HTML to text conversion and detrack for tracking parameter stripping.

## Configure

Create a configuration with your canonical host and URL policy.

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

`canonical_host` is the domain for all canonical URLs.
`public_base_url` is the full base URL used for URL normalization.
`url_policy` defines how URLs are cleaned before becoming canonical.

## Define an entity

An entity represents your content. It holds the data seoslug needs to generate metadata.

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    excerpt="Example excerpt",
    status="published",
)
```

## Generate the payload

Call `build_seo_payload` with the entity and route path.

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/posts/my-post", config)
```

The returned dictionary contains everything you need.

```python
print(payload["title"])       # "My Post"
print(payload["canonical"])   # "https://blog.example.com/posts/my-post"
print(payload["robots"])      # "index,follow"
print(payload["og"]["type"])  # "article"
```

## Inject into HTML

Use the payload in your template.

```html
<title>{{ payload.title }}</title>
<meta name="description" content="{{ payload.description }}">
<link rel="canonical" href="{{ payload.canonical }}">
<meta name="robots" content="{{ payload.robots }}">

<meta property="og:title" content="{{ payload.og.title }}">
<meta property="og:description" content="{{ payload.og.description }}">
<meta property="og:url" content="{{ payload.og.url }}">
<meta property="og:image" content="{{ payload.og.image }}">

<meta name="twitter:card" content="{{ payload.twitter.card }}">
<meta name="twitter:title" content="{{ payload.twitter.title }}">
<meta name="twitter:description" content="{{ payload.twitter.description }}">
<meta name="twitter:image" content="{{ payload.twitter.image }}">

<script type="application/ld+json">
{{ payload.schema_jsonld | tojson }}
</script>
```

## Next steps

Read [Core Concepts](core-concepts.md) to understand how seoslug works.
Read [Configuration Overview](configuration/index.md) for all configuration options.
