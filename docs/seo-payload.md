---
seo:
  title: SEO Payload - seoslug
  canonical: https://seoslug.emiliano-go.com/seo-payload/
  robots: index,follow
  og:
    type: website
    title: SEO Payload - seoslug
    description: buildseopayload returns a SEOPayload dataclass. It behaves like a
      dict for most use cases.
    url: https://seoslug.emiliano-go.com/seo-payload/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: SEO Payload - seoslug
    description: buildseopayload returns a SEOPayload dataclass. It behaves like a
      dict for most use cases.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: buildseopayload returns a SEOPayload dataclass. It behaves like a dict
    for most use cases.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: SEO Payload - seoslug
    url: https://seoslug.emiliano-go.com/seo-payload/
    description: buildseopayload returns a SEOPayload dataclass. It behaves like a
      dict for most use cases.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>SEO Payload - seoslug</title>\n<meta name=\"description\" content=\"\
  buildseopayload returns a SEOPayload dataclass. It behaves like a dict for most\
  \ use cases.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/seo-payload/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"SEO Payload - seoslug\">\n<meta\
  \ property=\"og:description\" content=\"buildseopayload returns a SEOPayload dataclass.\
  \ It behaves like a dict for most use cases.\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/seo-payload/\">\n<meta property=\"og:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"og:image:width\"\
  \ content=\"225\">\n<meta property=\"og:image:height\" content=\"225\">\n<meta property=\"\
  og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\" content=\"en_US\"\
  >\n<meta name=\"twitter:card\" content=\"summary_large_image\">\n<meta name=\"twitter:title\"\
  \ content=\"SEO Payload - seoslug\">\n<meta name=\"twitter:description\" content=\"\
  buildseopayload returns a SEOPayload dataclass. It behaves like a dict for most\
  \ use cases.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"SEO Payload - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/seo-payload/\"\
  ,\n  \"description\": \"buildseopayload returns a SEOPayload dataclass. It behaves\
  \ like a dict for most use cases.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# SEO Payload

`build_seo_payload()` returns a `SEOPayload` dataclass.
It behaves like a dict for most use cases.

The payload contains every tag your `<head>` needs.

## Full payload structure

```python
{
    "title": "My Post - My Blog",
    "description": "A brief description of the post.",
    "canonical": "https://blog.example.com/posts/my-post",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "My Post - My Blog",
        "description": "A brief description of the post.",
        "url": "https://blog.example.com/posts/my-post",
        "image": "https://cdn.example.com/hero.jpg",
        "image:width": 1200,
        "image:height": 630,
        "image:alt": "Hero image description",
        "site_name": "My Blog",
        "locale": "en_US",
        "locale:alternate": ["es_ES", "fr_FR"],
        "audio": "https://example.com/audio.mp3",
        "video": "https://example.com/video.mp4",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "My Post - My Blog",
        "description": "A brief description of the post.",
        "image": "https://cdn.example.com/hero.jpg",
        "image:alt": "Hero image description",
        "site": "@mysite",
        "creator": "@janedoe",
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "Article",
        "name": "My Post - My Blog",
        "url": "https://blog.example.com/posts/my-post",
        "description": "A brief description of the post.",
        "image": "https://cdn.example.com/hero.jpg",
    },
}
```

## Top-level keys

| Key           | Type                        | Description |
|---------------|-----------------------------|-------------|
| `title`       | `str`                       | Page title, with title template applied |
| `description` | `str`                       | Meta description from fallback chain |
| `canonical`   | `str`                       | Fully normalized canonical URL |
| `robots`      | `str`                       | Robots meta content string |
| `og`          | `OGPayload` (dict-like)     | Open Graph tags |
| `twitter`     | `TwitterPayload` (dict-like)| Twitter Card tags |
| `schema_jsonld` | `dict \| list[dict] \| None` | Schema.org JSON-LD |

## `title`

Fallback chain: `SEOOverrides.meta_title` > `SEOEntity.title` > `"Untitled"`.

After resolution the title template from config is applied.

```python
config = SEOConfig(
    ...,
    title_template="{title} - My Blog",
)
```

## `description`

Fallback chain: `SEOOverrides.meta_description` > `SEOEntity.excerpt` > body snippet > `""`.

The HTML body is only parsed when neither the override nor the excerpt is available.
If you provide an explicit `excerpt` or `meta_description`, the `body_html` is never touched.
This avoids expensive HTML parsing when the description is already determined.

The body snippet converts HTML to plain text and truncates at 160 characters.

## `canonical`

Fallback chain: `SEOOverrides.canonical_url` > normalized route path.

The route path runs through the full URL normalization pipeline.

## `robots`

| `Robots` dataclass field   | Type      | Default |
|----------------------------|-----------|---------|
| `index`                    | `bool`    | `True`  |
| `follow`                   | `bool`    | `True`  |
| `max_snippet`              | `int \| None` | `None` |
| `max_image_preview`        | `str \| None` | `None` |
| `max_video_preview`        | `int \| None` | `None` |

```python
from seoslug import Robots

# Structured
config = SEOConfig(
    ...,
    default_robots=Robots(index=False, follow=False),
    search_robots=Robots(index=False, follow=True, max_snippet=-1),
)

# Or string
overrides = SEOOverrides(robots="noindex,nofollow")
```

The output is always a serialized string like `"index,follow"` or `"noindex,follow,max-snippet:-1"`.

## `og` (Open Graph)

| Key                | Type                 | Source |
|--------------------|----------------------|--------|
| `type`             | `str`                | `"article"` for post/video, `"website"` otherwise |
| `title`            | `str \| None`        | Override > resolved title |
| `description`      | `str \| None`        | Override > resolved description |
| `url`              | `str \| None`        | Canonical URL |
| `image`            | `str \| None`        | Override > entity.featured_image > config.default_og_image |
| `image:width`      | `int \| None`        | From OGImage.width |
| `image:height`     | `int \| None`        | From OGImage.height |
| `image:alt`        | `str \| None`        | From OGImage.alt |
| `site_name`        | `str \| None`        | From config.site_name |
| `locale`           | `str \| None`        | From config.locale |
| `locale:alternate` | `list[str] \| None`  | From config.locale_alternate |
| `audio`            | `str \| None`        | Override og_audio |
| `video`            | `str \| None`        | Override og_video |

### OGImage dataclass

```python
from seoslug import OGImage

img = OGImage(
    url="https://cdn.example.com/hero.jpg",
    width=1200,
    height=630,
    alt="Hero image",
)
```

Accepted anywhere an image is: `entity.featured_image`, `overrides.og_image`, `overrides.twitter_image`, `config.default_og_image`.

## `twitter` (Twitter Card)

| Key           | Type                 | Source |
|---------------|----------------------|--------|
| `card`        | `str`                | Override > `"summary_large_image"` |
| `title`       | `str \| None`        | Override > resolved og:title |
| `description` | `str \| None`        | Override > resolved og:description |
| `image`       | `str \| None`        | Override > resolved og:image |
| `image:alt`   | `str \| None`        | From OGImage.alt |
| `site`        | `str \| None`        | From config.twitter_site |
| `creator`     | `str \| None`        | From override.twitter_creator |

## `schema_jsonld`

Auto-generated from entity type. See [Schema JSON-LD](schema-jsonld.md).

Single schema is a dict. Multiple schemas (e.g. with breadcrumbs) is a list. `None` when omitted.

## Social metadata fields

`locale` and `locale:alternate` are set at config level and flow into the OG payload:

```python
config = SEOConfig(
    ...,
    locale="en_US",
    locale_alternate=["es_ES", "fr_FR"],
)
```

Accessible in the payload as:

```python
payload["og"]["locale"]           # "en_US"
payload["og"]["locale:alternate"] # ["es_ES", "fr_FR"]
```

`og:audio` and `og:video` come from overrides:

```python
overrides = SEOOverrides(
    og_audio="https://example.com/audio.mp3",
    og_video="https://example.com/video.mp4",
)
```

`twitter:site` is a config-level field:

```python
config = SEOConfig(..., twitter_site="@mysite")

payload["twitter"]["site"]  # "@mysite"
```

`twitter:creator` is a per-entity override:

```python
overrides = SEOOverrides(twitter_creator="@janedoe")

payload["twitter"]["creator"]  # "@janedoe"
```
