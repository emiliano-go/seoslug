---
seo:
  title: 'Recipe: Multi-Language Site - seoslug'
  canonical: https://seoslug.emiliano-go.com/recipes/multi-language/
  robots: index,follow
  og:
    type: website
    title: 'Recipe: Multi-Language Site - seoslug'
    description: A multi-language site using locale, locale:alternate, and per-language
      overrides.
    url: https://seoslug.emiliano-go.com/recipes/multi-language/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: 'Recipe: Multi-Language Site - seoslug'
    description: A multi-language site using locale, locale:alternate, and per-language
      overrides.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: A multi-language site using locale, locale:alternate, and per-language
    overrides.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: 'Recipe: Multi-Language Site - seoslug'
    url: https://seoslug.emiliano-go.com/recipes/multi-language/
    description: A multi-language site using locale, locale:alternate, and per-language
      overrides.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Recipe: Multi-Language Site - seoslug</title>\n<meta name=\"description\"\
  \ content=\"A multi-language site using locale, locale:alternate, and per-language\
  \ overrides.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/recipes/multi-language/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Recipe: Multi-Language Site -\
  \ seoslug\">\n<meta property=\"og:description\" content=\"A multi-language site\
  \ using locale, locale:alternate, and per-language overrides.\">\n<meta property=\"\
  og:url\" content=\"https://seoslug.emiliano-go.com/recipes/multi-language/\">\n\
  <meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Recipe: Multi-Language Site - seoslug\"\
  >\n<meta name=\"twitter:description\" content=\"A multi-language site using locale,\
  \ locale:alternate, and per-language overrides.\">\n<meta name=\"twitter:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Recipe: Multi-Language\
  \ Site - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/recipes/multi-language/\"\
  ,\n  \"description\": \"A multi-language site using locale, locale:alternate, and\
  \ per-language overrides.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
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
