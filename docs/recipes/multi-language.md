---
{}
---

# Recipe: Multi-Language Site

A multi-language site using locale, locale:alternate, and per-language overrides.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=URLPolicy(
        lowercase_paths=True,
        trailing_slash="never",
    ),
    title_template="{title} - My Site",
    site_name="My Site",
    publisher_name="My Company",
    schema_type_map={"post": "Article"},
)
```

## English page

```python
from seoslug import SEOEntity, SEOOverrides, build_seo_payload

en_entity = SEOEntity(
    entity_type="post",
    title="Hello World",
    excerpt="A brief introduction.",
    status="published",
    published_at="2025-01-15",
    author_name="Jane Doe",
)

en_payload = build_seo_payload(
    en_entity,
    "/en/hello-world",
    config,
    SEOOverrides(
        twitter_creator="@janedoe",
    ),
)
```

## Spanish page

```python
es_entity = SEOEntity(
    entity_type="post",
    title="Hola Mundo",
    excerpt="Una breve introduccion.",
    status="published",
    published_at="2025-01-15",
    author_name="Jane Doe",
)

es_payload = build_seo_payload(
    es_entity,
    "/es/hola-mundo",
    config,
    SEOOverrides(
        meta_title="Hola Mundo",
        meta_description="Una breve introduccion.",
        twitter_creator="@janedoe",
    ),
)
```

## Setting locale and locale:alternate

Configure locale per-language in your view layer:

```python
from seoslug import SEOConfig

en_config = SEOConfig(
    ...,
    locale="en_US",
    locale_alternate=["es_ES", "fr_FR"],
)

es_config = SEOConfig(
    ...,
    locale="es_ES",
    locale_alternate=["en_US", "fr_FR"],
)
```

Or set locale on the payload after generation:

```python
en_payload.og.locale = "en_US"
en_payload.og.locale_alternate = ["es_ES", "fr_FR"]

es_payload.og.locale = "es_ES"
es_payload.og.locale_alternate = ["en_US", "fr_FR"]
```

## Template rendering

```html
<!-- English page -->
<head>
    <title>{{ en_payload.title }}</title>
    <link rel="canonical" href="{{ en_payload.canonical }}">

    <link rel="alternate" hreflang="en" href="https://example.com/en/hello-world">
    <link rel="alternate" hreflang="es" href="https://example.com/es/hola-mundo">
    <link rel="alternate" hreflang="x-default" href="https://example.com/en/hello-world">

    <meta property="og:locale" content="en_US">
    <meta property="og:locale:alternate" content="es_ES">
    <meta property="og:locale:alternate" content="fr_FR">
</head>
```

## English payload result

```python
{
    "title": "Hello World - My Site",
    "description": "A brief introduction.",
    "canonical": "https://example.com/en/hello-world",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "Hello World - My Site",
        "description": "A brief introduction.",
        "url": "https://example.com/en/hello-world",
        "site_name": "My Site",
        "locale": "en_US",
        "locale:alternate": ["es_ES", "fr_FR"],
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Hello World - My Site",
        "description": "A brief introduction.",
        "creator": "@janedoe",
        "site": None,
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "Article",
        "name": "Hello World - My Site",
        "url": "https://example.com/en/hello-world",
        "description": "A brief introduction.",
        "datePublished": "2025-01-15",
        "mainEntityOfPage": {"@id": "https://example.com/en/hello-world"},
        "author": {"@type": "Person", "name": "Jane Doe"},
        "publisher": {"@type": "Organization", "name": "My Company"},
    },
}
```
