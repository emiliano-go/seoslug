# SEOConfig reference

`SEOConfig` is the main configuration object.
It controls every aspect of SEO metadata generation.

## Fields

### canonical_host (required)

The domain for all canonical URLs.
Must be a hostname only, no scheme or path.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

### public_base_url (required)

The full base URL for your site.
Used during URL normalization to extract the scheme and host.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)
```

### url_policy (required)

A `URLPolicy` instance that defines URL normalization rules.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(trailing_slash="always"),
)
```

### default_robots (optional)

Default robots directive for content that is not published and not search results.
Defaults to `"index,follow"`.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    default_robots="noindex,nofollow",
)
```

### default_og_image (optional)

Fallback image URL for Open Graph and Twitter cards.
Used when the entity has no featured image.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    default_og_image="https://cdn.example.com/default.jpg",
)
```

### site_name (optional)

The site name for Open Graph.
Adds `og:site_name` to the payload.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    site_name="My Blog",
)
```

### title_template (optional)

Template string for the title tag.
Must include the `{title}` placeholder.
Defaults to `"{title}"`.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    title_template="{title} - My Blog",
)
```

### search_robots (optional)

Robots directive for search result pages.
Defaults to `"noindex,follow"`.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    search_robots="noindex,nofollow",
)
```

### schema_type_map (optional)

Maps entity types to schema.org types.
Defaults map post to Article, page to WebPage, video to VideoObject, home to WebPage, taxonomy to CollectionPage, and search to SearchResultsPage.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    schema_type_map={
        "post": "BlogPosting",
        "page": "WebPage",
        "product": "Product",
    },
)
```

### auto_generate_schema (optional)

Controls automatic JSON-LD generation.
Defaults to True. Set to False to disable.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    auto_generate_schema=False,
)
```

### publisher_name (optional)

The publisher name for schema.org JSON-LD.
Adds a publisher field to Article type schemas.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    publisher_name="My Company",
)
```

### publisher_logo (optional)

The publisher logo URL for schema.org JSON-LD.
Only used when publisher_name is set.

```python
SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    publisher_name="My Company",
    publisher_logo="https://cdn.example.com/logo.png",
)
```
