# Schema.org and JSON-LD

Schema.org is a shared vocabulary that search engines use to understand your content.
JSON-LD is the format for embedding it in your HTML.

## Auto generated schema

seoslug automatically generates JSON-LD based on entity_type.
The mapping is controlled by `schema_type_map` in SEOConfig.

Default mappings:

| Entity type | Schema.org type |
|-------------|-----------------|
| post | Article |
| page | WebPage |
| video | VideoObject |
| home | WebPage |
| taxonomy | CollectionPage |
| search | SearchResultsPage |

You can customize the mapping for your content types.

```python
config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    schema_type_map={
        "post": "BlogPosting",
        "page": "WebPage",
        "product": "Product",
        "event": "Event",
    },
)
```

## Schema structure

The auto generated schema includes these fields:

- `@context` -- always `"https://schema.org"`
- `@type` -- from the schema type map
- `name` -- the resolved title
- `url` -- the canonical URL
- `description` -- included when a description exists
- `image` -- included when an image exists
- `datePublished` -- included when `published_at` is set
- `dateModified` -- included when `updated_at` is set
- `mainEntityOfPage` -- included for Article type schemas
- `author` -- included when `author_name` is set (type Person)
- `publisher` -- included when `publisher_name` is set in config (type Organization)

## Example output

```python
{
    "@context": "https://schema.org",
    "@type": "Article",
    "name": "My Post",
    "url": "https://blog.example.com/posts/my-post",
    "description": "A brief description",
    "image": "https://cdn.example.com/image.jpg",
    "datePublished": "2025-01-15",
    "dateModified": "2025-02-01",
    "mainEntityOfPage": {
        "@id": "https://blog.example.com/posts/my-post"
    },
    "author": {
        "@type": "Person",
        "name": "Jane Doe"
    },
    "publisher": {
        "@type": "Organization",
        "name": "My Company",
        "logo": "https://cdn.example.com/logo.png"
    },
}
```

## Disabling auto generation

You can disable auto generation globally.

```python
config = SEOConfig(
    auto_generate_schema=False,
)
```

You can disable it for a single entity.

```python
overrides = SEOOverrides(omit_schema=True)
```

## Custom schema

You can provide a completely custom schema object.

```python
overrides = SEOOverrides(schema_jsonld={
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Custom Product",
    "offers": {
        "@type": "Offer",
        "price": "29.99",
        "priceCurrency": "USD",
    },
})
```

You can also pass a list of schema objects.

```python
overrides = SEOOverrides(schema_jsonld=[
    {"@context": "https://schema.org", "@type": "Article", "name": "Post"},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", ...},
])
```
