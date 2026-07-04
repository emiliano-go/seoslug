---
{}
---

# SEOOverrides reference

`SEOOverrides` lets you override any generated SEO field for a single call. Pass it as the fourth argument to `build_seo_payload`. Every field is optional.

## Fields

| Option | Type | Default | Description |
|---|---|---|---|
| `meta_title` | `str` or `None` | `None` | Override the `<title>` tag. Highest precedence. |
| `meta_description` | `str` or `None` | `None` | Override the meta description. Highest precedence. |
| `canonical_url` | `str` or `None` | `None` | Override the canonical URL. Highest precedence. |
| `robots` | `str` or `Robots` or `None` | `None` | Override the robots directive. Highest precedence. |
| `og_title` | `str` or `None` | `None` | Override `og:title`. Also becomes fallback for `twitter:title`. |
| `og_description` | `str` or `None` | `None` | Override `og:description`. Also becomes fallback for `twitter:description`. |
| `og_image` | `str` or `OGImage` or `None` | `None` | Override `og:image`. Also becomes fallback for `twitter:image`. |
| `twitter_card` | `str` or `None` | `None` | Override the Twitter card type. Defaults to `"summary_large_image"`. |
| `twitter_title` | `str` or `None` | `None` | Override `twitter:title`. Highest precedence. |
| `twitter_description` | `str` or `None` | `None` | Override `twitter:description`. Highest precedence. |
| `twitter_image` | `str` or `OGImage` or `None` | `None` | Override `twitter:image`. Highest precedence. |
| `twitter_creator` | `str` or `None` | `None` | Twitter handle for `twitter:creator`. |
| `og_audio` | `str` or `None` | `None` | URL for `og:audio`. |
| `og_video` | `str` or `None` | `None` | URL for `og:video`. |
| `schema_jsonld` | `dict` or `list[dict]` or `None` | `None` | Custom JSON-LD schema. Replaces auto-generated schema. |
| `omit_schema` | `bool` | `False` | Suppress all JSON-LD schema output for this entity. |
| `skip_title_template` | `bool` | `False` | Bypass `config.title_template` for this entity. |

### meta_title

Overrides the entire title tag. Bypasses `config.title_template` unless `skip_title_template` is `False`.

```python
SEOOverrides(meta_title="Exact Page Title")
```

### meta_description

Overrides the meta description tag. Falls back through excerpt, body_html when not set.

```python
SEOOverrides(meta_description="Custom description for this page only")
```

### canonical_url

Overrides the canonical URL. Provide a full absolute URL.

```python
SEOOverrides(canonical_url="https://example.com/custom-canonical")
```

### robots

Overrides the robots directive. Accepts a plain string or a structured `Robots` dataclass.

```python
# String form
SEOOverrides(robots="noindex,nofollow")

# Structured form
from seoslug import Robots

SEOOverrides(robots=Robots(index=False, follow=False))
```

### og_title

Overrides the Open Graph title. When set, it becomes the fallback for `twitter:title` (unless `twitter_title` is also set).

```python
SEOOverrides(og_title="Custom OG Title")
```

### og_description

Overrides the Open Graph description. When set, it becomes the fallback for `twitter:description` (unless `twitter_description` is also set).

```python
SEOOverrides(og_description="Custom OG description for social sharing")
```

### og_image

Overrides the Open Graph image. Accepts a URL string or a structured `OGImage` with dimensions and alt text. When set, it becomes the fallback for `twitter:image`.

```python
# String form
SEOOverrides(og_image="https://cdn.example.com/promo.jpg")

# Structured form
from seoslug import OGImage

SEOOverrides(
    og_image=OGImage(
        url="https://cdn.example.com/promo.jpg",
        width=1200,
        height=630,
        alt="Promo image",
    ),
)
```

### twitter_card

Overrides the Twitter card type. Defaults to `"summary_large_image"`. Common values are `"summary"` and `"summary_large_image"`.

```python
SEOOverrides(twitter_card="summary")
```

### twitter_title

Overrides the Twitter title independently from OG title. Highest precedence in the Twitter title fallback chain.

```python
SEOOverrides(twitter_title="Custom Twitter Card Title")
```

### twitter_description

Overrides the Twitter description independently. Highest precedence.

```python
SEOOverrides(twitter_description="Custom Twitter card description")
```

### twitter_image

Overrides the Twitter image independently. Highest precedence. Accepts a URL string or a structured `OGImage`.

```python
SEOOverrides(twitter_image="https://cdn.example.com/twitter-card.jpg")
```

### twitter_creator

Sets the `twitter:creator` meta tag. Use the Twitter handle with or without `@`.

```python
SEOOverrides(twitter_creator="@janedoe")
```

### og_audio

Sets the `og:audio` meta tag. Provide a URL to an audio file.

```python
SEOOverrides(og_audio="https://cdn.example.com/episode.mp3")
```

### og_video

Sets the `og:video` meta tag. Provide a URL to a video file.

```python
SEOOverrides(og_video="https://cdn.example.com/trailer.mp4")
```

### schema_jsonld

Provides a custom JSON-LD schema object. Accepts a single dict or a list of dicts. When set, seoslug uses this value instead of auto-generating schema for the entity. Breadcrumbs are still appended separately.

```python
SEOOverrides(schema_jsonld={
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Custom Product",
    "offers": {
        "@type": "Offer",
        "price": "29.99",
    },
})
```

### omit_schema

When `True`, removes the `schema_jsonld` key entirely from the payload. Breadcrumbs are also suppressed.

```python
SEOOverrides(omit_schema=True)
```

### skip_title_template

When `True`, bypasses `config.title_template` and uses the raw title directly. Useful when `meta_title` already contains a fully formatted title.

```python
config = SEOConfig(
    ...,
    title_template="{title} - My Blog",
)

# With skip_title_template, the title stays as-is
SEOOverrides(
    meta_title="Exact Title - No Template Applied",
    skip_title_template=True,
)
```

## Use cases

### Custom title without template

Use `skip_title_template` to provide a fully formatted title that bypasses the global template.

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(
    meta_title="My Exact Page Title - Site Name",
    skip_title_template=True,
)
payload = build_seo_payload(entity, "/page", config, overrides)
```

### Per-page noindex

Prevent a specific page from being indexed without changing global settings.

```python
overrides = SEOOverrides(robots="noindex,nofollow")
payload = build_seo_payload(entity, "/draft-page", config, overrides)
```

### Custom social card

Provide a unique image and description just for social sharing on one page.

```python
from seoslug import OGImage

overrides = SEOOverrides(
    og_title="Special Promo",
    og_description="Limited time offer - click to learn more",
    og_image=OGImage(
        url="https://cdn.example.com/promo-social.jpg",
        width=1200,
        height=630,
        alt="Special promo banner",
    ),
    twitter_creator="@marketing",
)
payload = build_seo_payload(entity, "/promo", config, overrides)
```

### Audio and video content

Add `og:audio` or `og:video` tags for media-rich pages.

```python
overrides = SEOOverrides(
    og_audio="https://cdn.example.com/episode-42.mp3",
    og_video="https://cdn.example.com/trailer.mp4",
)
payload = build_seo_payload(entity, "/media", config, overrides)
```

### Custom JSON-LD injection

Replace the auto-generated schema with your own, or provide multiple schemas.

```python
overrides = SEOOverrides(schema_jsonld=[
    {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Widget",
    },
    {
        "@context": "https://schema.org",
        "@type": "Review",
        "itemReviewed": {"@type": "Product", "name": "Widget"},
    },
])
payload = build_seo_payload(entity, "/product", config, overrides)
```

### Complete schema suppression

Remove all JSON-LD output for a single page.

```python
overrides = SEOOverrides(omit_schema=True)
payload = build_seo_payload(entity, "/page", config, overrides)
```
