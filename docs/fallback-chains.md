---
seo:
  title: Fallback Chains - seoslug
  canonical: https://seoslug.emiliano-go.com/fallback-chains/
  robots: index,follow
  og:
    type: website
    title: Fallback Chains - seoslug
    description: Every field in the SEO payload resolves through a fallback chain.
      The first non-empty value wins.
    url: https://seoslug.emiliano-go.com/fallback-chains/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Fallback Chains - seoslug
    description: Every field in the SEO payload resolves through a fallback chain.
      The first non-empty value wins.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Every field in the SEO payload resolves through a fallback chain. The
    first non-empty value wins.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Fallback Chains - seoslug
    url: https://seoslug.emiliano-go.com/fallback-chains/
    description: Every field in the SEO payload resolves through a fallback chain.
      The first non-empty value wins.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Fallback Chains - seoslug</title>\n<meta name=\"description\" content=\"\
  Every field in the SEO payload resolves through a fallback chain. The first non-empty\
  \ value wins.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/fallback-chains/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Fallback Chains - seoslug\">\n\
  <meta property=\"og:description\" content=\"Every field in the SEO payload resolves\
  \ through a fallback chain. The first non-empty value wins.\">\n<meta property=\"\
  og:url\" content=\"https://seoslug.emiliano-go.com/fallback-chains/\">\n<meta property=\"\
  og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"\
  og:image:width\" content=\"225\">\n<meta property=\"og:image:height\" content=\"\
  225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"\
  og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Fallback Chains - seoslug\">\n<meta name=\"\
  twitter:description\" content=\"Every field in the SEO payload resolves through\
  \ a fallback chain. The first non-empty value wins.\">\n<meta name=\"twitter:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Fallback Chains\
  \ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/fallback-chains/\"\
  ,\n  \"description\": \"Every field in the SEO payload resolves through a fallback\
  \ chain. The first non-empty value wins.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Fallback Chains

Every field in the SEO payload resolves through a fallback chain.
The first non-empty value wins.

This means you can set site-wide defaults in config, override per-entity in `SEOEntity`, and fine-tune per-page with `SEOOverrides`.

## Understanding precedence

The general precedence order is:

1. **`SEOOverrides`**: per-call overrides (highest priority)
2. **`SEOEntity`**: content entity fields
3. **`SEOConfig`**: configuration defaults
4. **Hardcoded defaults**: library fallbacks (lowest priority)

Overrides always win. Entity data is next. Config defaults come last.

## Title fallback chain

1. `SEOOverrides.meta_title`
2. `SEOEntity.title`
3. `"Untitled"` (hardcoded)

After resolution, the title template is applied unless `skip_title_template=True`.

```python
config = SEOConfig(title_template="{title} - My Site")
# title "My Post" becomes "My Post - My Site"
```

## Description fallback chain

1. `SEOOverrides.meta_description`
2. `SEOEntity.excerpt`
3. Auto-generated snippet from `SEOEntity.body_html` (max 160 chars)
4. `""` (empty string)

The body snippet is extracted via lxml (fallback to pure-Python regex).
Scripts and styles are stripped. Whitespace is normalized.
Result is truncated to 160 characters with an ellipsis.

```python
entity = SEOEntity(
    entity_type="post",
    body_html="<p>A long article about something interesting.</p>",
)
# description becomes "A long article about something interesting."
```

## Canonical fallback chain

1. `SEOOverrides.canonical_url`
2. Normalized route path (passed through full URL normalization pipeline)

```python
overrides = SEOOverrides(canonical_url="https://example.com/custom-about")
```

## Robots fallback chain

1. `SEOOverrides.robots` (string or `Robots` object)
2. Entity-derived default

The entity-derived default logic:

- `entity_type == "search"` uses `config.search_robots` (default: `"noindex,follow"`)
- `entity.status` is `"published"` uses `"index,follow"`
- Everything else uses `config.default_robots` (default: `"index,follow"`)

```python
config = SEOConfig(
    default_robots="noindex,nofollow",
    search_robots="noindex,follow",
)
```

## og:title fallback chain

1. `SEOOverrides.og_title`
2. Resolved title (after template)

## og:description fallback chain

1. `SEOOverrides.og_description`
2. Resolved description

## og:image fallback chain

1. `SEOOverrides.og_image` (string or `OGImage`)
2. `SEOEntity.featured_image` (string or `OGImage`)
3. `SEOConfig.default_og_image` (string or `OGImage`)

The resolved image cascades to twitter:image.

```python
config = SEOConfig(
    default_og_image="https://cdn.example.com/default.jpg",
)
```

## twitter:card fallback chain

1. `SEOOverrides.twitter_card`
2. `"summary_large_image"` (hardcoded default)

## twitter:title fallback chain

1. `SEOOverrides.twitter_title`
2. Resolved og:title

## twitter:description fallback chain

1. `SEOOverrides.twitter_description`
2. Resolved og:description

## twitter:image fallback chain

1. `SEOOverrides.twitter_image` (string or `OGImage`)
2. Resolved og:image

## Summary table

| Field               | Chain order                                  |
|---------------------|----------------------------------------------|
| title               | Override > Entity > `"Untitled"` + template  |
| description         | Override > Excerpt > Body snippet > `""`     |
| canonical           | Override > Normalized route                  |
| robots              | Override > Entity status default             |
| og:title            | Override > Resolved title                    |
| og:description      | Override > Resolved description              |
| og:image            | Override > Entity image > Config default     |
| twitter:card        | Override > `"summary_large_image"`           |
| twitter:title       | Override > og:title                          |
| twitter:description | Override > og:description                    |
| twitter:image       | Override > og:image                          |
