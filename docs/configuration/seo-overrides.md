# SEOOverrides reference

`SEOOverrides` lets you override any field that seoslug would otherwise generate.
Pass it as the fourth argument to `build_seo_payload()`.

## Fields

### meta_title (optional)

Overrides the title tag.
Takes highest precedence in the title fallback chain.

```python
SEOOverrides(meta_title="Custom Page Title")
```

### meta_description (optional)

Overrides the meta description.
Takes highest precedence in the description fallback chain.

```python
SEOOverrides(meta_description="Custom description for this page")
```

### canonical_url (optional)

Overrides the canonical URL.
Takes highest precedence in the canonical fallback chain.

```python
SEOOverrides(canonical_url="https://example.com/custom-canonical")
```

### robots (optional)

Overrides the robots directive.
Takes highest precedence in the robots fallback chain.

```python
SEOOverrides(robots="noindex,nofollow")
```

### og_title (optional)

Overrides the Open Graph title.
When set, it also becomes the fallback for the Twitter title.

```python
SEOOverrides(og_title="Custom OG Title")
```

### og_description (optional)

Overrides the Open Graph description.
When set, it also becomes the fallback for the Twitter description.

```python
SEOOverrides(og_description="Custom OG description")
```

### og_image (optional)

Overrides the Open Graph image.
When set, it also becomes the fallback for the Twitter image.

```python
SEOOverrides(og_image="https://cdn.example.com/custom-og.jpg")
```

### twitter_card (optional)

Overrides the Twitter card type.
Defaults to "summary_large_image".

```python
SEOOverrides(twitter_card="summary")
```

### twitter_title (optional)

Overrides the Twitter title.
Takes highest precedence over the OG title fallback.

```python
SEOOverrides(twitter_title="Custom Twitter Title")
```

### twitter_description (optional)

Overrides the Twitter description.
Takes highest precedence over the OG description fallback.

```python
SEOOverrides(twitter_description="Custom Twitter description")
```

### twitter_image (optional)

Overrides the Twitter image.
Takes highest precedence over the OG image fallback.

```python
SEOOverrides(twitter_image="https://cdn.example.com/custom-twitter.jpg")
```

### schema_jsonld (optional)

Provides a custom JSON-LD schema object.
Accepts a dict or a list of dicts.
When set, seoslug uses this value instead of auto generating schema.

```python
SEOOverrides(schema_jsonld={
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Custom Product",
})
```

### omit_schema (optional)

Disables schema generation for a single entity.
When True, no schema_jsonld key is added to the payload.
Defaults to False.

```python
SEOOverrides(omit_schema=True)
```

## Example

Force a custom image and disable indexing for a specific page.

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(
    og_image="https://cdn.example.com/promo.jpg",
    robots="noindex,follow",
)
payload = build_seo_payload(entity, "/path", config, overrides)
```
