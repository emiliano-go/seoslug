---
seo:
  title: Validation Warnings - seoslug
  canonical: https://seoslug.emiliano-go.com/validation/
  robots: index,follow
  og:
    type: website
    title: Validation Warnings - seoslug
    description: seoslug produces non-fatal validation warnings when emitwarnings
      is enabled. Warnings alert you to common SEO issues without breaking your build.
    url: https://seoslug.emiliano-go.com/validation/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Validation Warnings - seoslug
    description: seoslug produces non-fatal validation warnings when emitwarnings
      is enabled. Warnings alert you to common SEO issues without breaking your build.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: seoslug produces non-fatal validation warnings when emitwarnings is
    enabled. Warnings alert you to common SEO issues without breaking your build.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Validation Warnings - seoslug
    url: https://seoslug.emiliano-go.com/validation/
    description: seoslug produces non-fatal validation warnings when emitwarnings
      is enabled. Warnings alert you to common SEO issues without breaking your build.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Validation Warnings - seoslug</title>\n<meta name=\"description\"\
  \ content=\"seoslug produces non-fatal validation warnings when emitwarnings is\
  \ enabled. Warnings alert you to common SEO issues without breaking your build.\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/validation/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Validation Warnings - seoslug\"\
  >\n<meta property=\"og:description\" content=\"seoslug produces non-fatal validation\
  \ warnings when emitwarnings is enabled. Warnings alert you to common SEO issues\
  \ without breaking your build.\">\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/validation/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Validation Warnings - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"seoslug produces non-fatal validation warnings\
  \ when emitwarnings is enabled. Warnings alert you to common SEO issues without\
  \ breaking your build.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Validation Warnings - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/validation/\"\
  ,\n  \"description\": \"seoslug produces non-fatal validation warnings when emitwarnings\
  \ is enabled. Warnings alert you to common SEO issues without breaking your build.\"\
  ,\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n\
  \  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Validation Warnings

seoslug produces non-fatal validation warnings when `emit_warnings` is enabled.
Warnings alert you to common SEO issues without breaking your build.

## Enabling warnings

Set `emit_warnings=True` in `SEOConfig`.

```python
from seoslug import SEOConfig

config = SEOConfig(
    ...,
    emit_warnings=True,
)
```

When enabled, `build_seo_payload` calls `validate_payload()` and emits each warning via `warnings.warn()`.

## The validate_payload function

```python
from seoslug.validation import validate_payload

warnings: list[str] = validate_payload(payload_dict, config)
```

Parameters:

| Parameter | Type        | Description               |
|-----------|-------------|---------------------------|
| `payload` | `dict`      | The built SEO payload     |
| `config`  | `SEOConfig` | Your SEO configuration    |

Returns a list of warning strings. Each string describes one issue.

## Warning types

| Warning | Condition | Example |
|---------|-----------|---------|
| Title exceeds 60 chars | `len(title) > 60` | `"Title exceeds 60 characters (72 chars)"` |
| Description exceeds 160 chars | `len(description) > 160` | `"Description exceeds 160 characters (245 chars)"` |
| Canonical URL not absolute | canonical does not start with `http://` or `https://` | `"Canonical URL is not absolute: /relative-path"` |
| OG image URL not absolute | og:image does not start with `http://` or `https://` | `"OG image URL is not absolute: /images/photo.jpg"` |
| Robots directive malformed | robots string has invalid format | `"Robots directive may be malformed: jibberish"` |

## Example with catch_warnings

```python
import warnings
from seoslug import SEOConfig, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=...,
    emit_warnings=True,
)

entity = SEOEntity(
    entity_type="page",
    title="A" * 70,           # triggers title warning
    excerpt="B" * 300,         # triggers description warning
)

with warnings.catch_warnings(record=True) as w:
    warnings.simplefilter("always")
    payload = build_seo_payload(entity, "/page", config)

for warning in w:
    print(warning.message)
    # Title exceeds 60 characters (70 chars)
    # Description exceeds 160 characters (300 chars)
```

## Disabling warnings

Set `emit_warnings=False` (default) to skip validation entirely.

```python
config = SEOConfig(
    ...,
    emit_warnings=False,  # default
)
```

No performance cost when disabled. The validation function is never called.

## Best practices

- Enable warnings in development and CI
- Keep the warnings list in CI output for review
- Fix absolute URL issues in canonical and OG image fields
- Tighten title generation if it consistently exceeds 60 chars
- Disable warnings in production for zero overhead
