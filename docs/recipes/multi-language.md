# Recipe: Multi language sites

Multi language sites need alternate language canonical URLs.
You can extend the seoslug payload with hreflang tags and locale information.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=URLPolicy(lowercase_paths=True, trailing_slash="never"),
    title_template="{title} - My Site",
    site_name="My Site",
)
```

## Entity with language variants

```python
from seoslug import SEOEntity, SEOOverrides, build_seo_payload

# English version
en_entity = SEOEntity(
    entity_type="post",
    title="Hello World",
    excerpt="A brief introduction.",
    status="published",
)
en_payload = build_seo_payload(en_entity, "/en/hello-world", config)

# Spanish version
es_entity = SEOEntity(
    entity_type="post",
    title="Hola Mundo",
    excerpt="Una breve introduccion.",
    status="published",
)
es_payload = build_seo_payload(es_entity, "/es/hola-mundo", config)
```

## Extend the payload

```python
def add_hreflang(payload, lang, alternates):
    payload["og"]["locale"] = lang
    payload["hreflang"] = alternates
    return payload

payload = add_hreflang(en_payload, "en_US", {
    "en": "https://example.com/en/hello-world",
    "es": "https://example.com/es/hola-mundo",
    "x-default": "https://example.com/en/hello-world",
})
```

## Template rendering

```html
<head>
    <title>{{ payload.title }}</title>
    <link rel="canonical" href="{{ payload.canonical }}">

    {% for lang, url in payload.hreflang.items() %}
    <link rel="alternate" hreflang="{{ lang }}" href="{{ url }}">
    {% endfor %}

    <meta property="og:locale" content="{{ payload.og.locale }}">
    {% for lang, url in payload.hreflang.items() %}
    <meta property="og:locale:alternate" content="{{ lang }}">
    {% endfor %}
</head>
```

## Fallback behavior

For multi language sites, set up fallback preferences per language.
The default fallback chain already handles missing fields.
Override title or description per language as needed.

```python
overrides = SEOOverrides(
    meta_title="Hola Mundo",
    meta_description="Una breve introduccion.",
)
payload = build_seo_payload(entity, "/es/hola-mundo", config, overrides)
```
