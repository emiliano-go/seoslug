# SEO payload generation

The payload returned by `build_seo_payload()` is a dictionary with seven top level keys.

## Payload structure

```python
{
    "title": "My Post",
    "description": "A short description",
    "canonical": "https://blog.example.com/posts/my-post",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "My Post",
        "description": "A short description",
        "url": "https://blog.example.com/posts/my-post",
        "image": "https://cdn.example.com/default.jpg",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "My Post",
        "description": "A short description",
        "image": "https://cdn.example.com/default.jpg",
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "Article",
        "name": "My Post",
        "url": "https://blog.example.com/posts/my-post",
        "description": "A short description",
        "image": "https://cdn.example.com/default.jpg",
    },
}
```

## How each field is generated

### title

Resolved through the fallback chain.
Override meta_title is checked first.
Then entity title is checked.
If both are missing, the default is "Untitled".

The title template from SEOConfig is applied if set.

```python
config = SEOConfig(
    title_template="{title} - My Blog",
)
# Result: "My Post - My Blog"
```

### description

Resolved through the fallback chain.
Override meta_description is checked first.
Then entity excerpt is checked.
Then the HTML body is converted to plain text and truncated to 160 characters.
If all are missing, the result is an empty string.

### canonical

Resolved through the fallback chain.
Override canonical_url is checked first.
Then the normalized route path is used.

The route path is passed through the full URL normalization pipeline.

### robots

Resolved through the fallback chain.
Override robots is checked first.
Then the entity status determines the value.
Published content gets "index,follow".
Search entity types get the search_robots value from config.
Other statuses use the default_robots value from config.

### og

The Open Graph dictionary has five keys: type, title, description, url, and image.
The og:type depends on entity type. Posts and videos use "article". Others use "website".
The og:title falls back from override to the resolved title.
The og:description falls back from override to the resolved description.
The og:image falls back from override to entity featured_image to config default_og_image.
If site_name is set in config, og:site_name is added.

### twitter

The Twitter dictionary has four keys: card, title, description, and image.
The twitter:card defaults to "summary_large_image" and can be overridden.
The twitter:title has its own override, then falls back to og:title.
The twitter:description has its own override, then falls back to og:description.
The twitter:image has its own override, then falls back to og:image.

### schema_jsonld

The schema is auto generated based on entity type.
The entity type is mapped to a schema.org type via `schema_type_map`.
The schema includes name, url, description, and image.
Timestamps are added for published_at and updated_at.
Author and publisher information is added when available.
Article types include a mainEntityOfPage field.

Schema generation can be disabled globally via `auto_generate_schema`.
Schema can be overridden per call via `SEOOverrides.schema_jsonld`.
Schema can be omitted per call via `SEOOverrides.omit_schema`.
