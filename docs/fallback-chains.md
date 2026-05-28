# Fallback chains

When a field is missing from your entity, seoslug consults a fallback chain.
Each field has a predefined chain of sources.
The first non empty value in the chain is used.

## Title fallback chain

The title is resolved in this order:

1. `SEOOverrides.meta_title`
2. `SEOEntity.title`
3. `"Untitled"` (hardcoded default)

After resolution, the title template is applied if set in SEOConfig.

```python
config = SEOConfig(title_template="{title} - My Site")
# title "My Post" becomes "My Post - My Site"
```

## Description fallback chain

The description is resolved in this order:

1. `SEOOverrides.meta_description`
2. `SEOEntity.excerpt`
3. Auto generated snippet from `SEOEntity.body_html` (max 160 characters)
4. `""` (empty string)

The HTML body is converted to plain text using lxml.
Script and style elements are removed before text extraction.
Whitespace is normalized.
The result is truncated to 160 characters with an ellipsis.

```python
entity = SEOEntity(
    entity_type="post",
    title="My Post",
    body_html="<p>This is a long article about something interesting.</p>",
)
# description becomes "This is a long article about something interesting."
```

## Canonical fallback chain

The canonical URL is resolved in this order:

1. `SEOOverrides.canonical_url`
2. Normalized route path

The route path is passed through the full URL normalization pipeline.
This ensures consistent canonical URLs.

## Robots fallback chain

The robots directive is resolved in this order:

1. `SEOOverrides.robots`
2. Entity derived default based on type and status

The entity derived default works like this:

- Search entity types use `SEOConfig.search_robots` (default: "noindex,follow")
- Published entities get "index,follow"
- All other entities use `SEOConfig.default_robots` (default: "index,follow")

```python
config = SEOConfig(
    default_robots="noindex,nofollow",
    search_robots="noindex,follow",
)
```

## Open Graph fallback chains

### og:title

1. `SEOOverrides.og_title`
2. Resolved title

### og:description

1. `SEOOverrides.og_description`
2. Resolved description

### og:image

1. `SEOOverrides.og_image`
2. `SEOEntity.featured_image`
3. `SEOConfig.default_og_image`

## Twitter fallback chains

### twitter:card

1. `SEOOverrides.twitter_card`
2. `"summary_large_image"` (hardcoded default)

### twitter:title

1. `SEOOverrides.twitter_title`
2. Resolved og:title

### twitter:description

1. `SEOOverrides.twitter_description`
2. Resolved og:description

### twitter:image

1. `SEOOverrides.twitter_image`
2. Resolved og:image

## Understanding precedence

Overrides always take the highest precedence.
Entity fields come next.
Configuration defaults come last.
Hardcoded defaults are the final fallback.
