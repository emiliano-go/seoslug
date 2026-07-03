---
seo:
  title: Configuration overview - seoslug
  canonical: https://seoslug.emiliano-go.com/configuration/
  robots: index,follow
  og:
    type: website
    title: Configuration overview - seoslug
    description: seoslug uses four dataclasses to configure SEO output. Each one has
      a single responsibility. You compose them together at build time.
    url: https://seoslug.emiliano-go.com/configuration/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Configuration overview - seoslug
    description: seoslug uses four dataclasses to configure SEO output. Each one has
      a single responsibility. You compose them together at build time.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: seoslug uses four dataclasses to configure SEO output. Each one has
    a single responsibility. You compose them together at build time.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Configuration overview - seoslug
    url: https://seoslug.emiliano-go.com/configuration/
    description: seoslug uses four dataclasses to configure SEO output. Each one has
      a single responsibility. You compose them together at build time.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Configuration overview - seoslug</title>\n<meta name=\"description\"\
  \ content=\"seoslug uses four dataclasses to configure SEO output. Each one has\
  \ a single responsibility. You compose them together at build time.\">\n<link rel=\"\
  canonical\" href=\"https://seoslug.emiliano-go.com/configuration/\">\n<meta name=\"\
  robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"website\"\
  >\n<meta property=\"og:title\" content=\"Configuration overview - seoslug\">\n<meta\
  \ property=\"og:description\" content=\"seoslug uses four dataclasses to configure\
  \ SEO output. Each one has a single responsibility. You compose them together at\
  \ build time.\">\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/configuration/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Configuration overview - seoslug\">\n\
  <meta name=\"twitter:description\" content=\"seoslug uses four dataclasses to configure\
  \ SEO output. Each one has a single responsibility. You compose them together at\
  \ build time.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Configuration overview - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/configuration/\"\
  ,\n  \"description\": \"seoslug uses four dataclasses to configure SEO output. Each\
  \ one has a single responsibility. You compose them together at build time.\",\n\
  \  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n\
  \  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Configuration overview

seoslug uses four dataclasses to configure SEO output. Each one has a single responsibility. You compose them together at build time.

## SEOConfig

Global settings for your entire site. Controls canonical host, URL normalization, robots defaults, Open Graph, schema generation, and locale.

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

[Full reference](seo-config.md)

## URLPolicy

URL normalization rules. Enforces HTTPS, trailing slash policy, lowercase paths, and query parameter filtering. Every canonical URL flows through this pipeline.

```python
from seoslug import URLPolicy

policy = URLPolicy(
    enforce_https=True,
    lowercase_paths=True,
    trailing_slash="never",
    strip_tracking_params=True,
)
```

[Full reference](url-policy.md)

## SEOEntity

Your content. Holds the raw data seoslug uses to generate title, description, Open Graph, Twitter Cards, and JSON-LD schema. Entity type determines the schema output.

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    excerpt="A brief description",
    status="published",
)
```

[Full reference](seo-entity.md)

## SEOOverrides

Per-call overrides. Bypass generated values for a single page without touching global config. Useful for custom titles, per-page robots, or injecting custom JSON-LD.

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(
    meta_title="Custom Page Title",
    robots="noindex,follow",
)
payload = build_seo_payload(entity, "/path", config, overrides)
```

[Full reference](seo-overrides.md)
