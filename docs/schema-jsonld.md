---
{}
---

# Schema.org JSON-LD

seoslug auto-generates Schema.org JSON-LD based on `entity_type`.
The mapping from entity type to schema.org type lives in `schema_type_map`.

You get deterministic, structured data for every page.
No manual schema stitching required.

## Auto-generated schema

Default `schema_type_map` mappings:

| Entity type     | Schema.org type      |
|-----------------|----------------------|
| `post`          | Article              |
| `page`          | WebPage              |
| `video`         | VideoObject          |
| `home`          | WebPage              |
| `taxonomy`      | CollectionPage       |
| `search`        | SearchResultsPage    |
| `product`       | Product              |
| `organization`  | Organization         |
| `local_business`| LocalBusiness        |
| `faq`           | FAQPage              |

Override any mapping:

```python
from seoslug import SEOConfig

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=...,
    schema_type_map={
        "post": "BlogPosting",
        "event": "Event",
    },
)
```

Set a mapping to `None` to disable schema for that type.

## Generic builder fields

Every auto-generated schema includes these fields:

| Field              | Condition              |
|--------------------|------------------------|
| `@context`         | Always `"https://schema.org"` |
| `@type`            | From `schema_type_map` |
| `name`             | Resolved title         |
| `url`              | Canonical URL          |
| `description`      | When description exists |
| `image`            | When OG image exists   |
| `datePublished`    | When `published_at` is set |
| `dateModified`     | When `updated_at` is set |
| `author`           | When `author_name` is set (Person type) |
| `publisher`        | When `publisher_name` is set in config (Organization type) |
| `mainEntityOfPage` | For Article/BlogPosting/NewsArticle types |

```python
# Generated output shape
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

## Type-specific builders

Four entity types have dedicated builders with extra fields.
All others use the generic builder which produces the fields above.

### Product (`entity_type="product"`)

| Field      | Source           |
|------------|------------------|
| `sku`      | `entity.sku`     |
| `offers.price` | `entity.price` |
| `offers.priceCurrency` | `entity.price_currency` |
| `offers.availability` | `entity.availability` (prefixed with `https://schema.org/`) |

```python
entity = SEOEntity(
    entity_type="product",
    title="Wireless Headphones",
    sku="WH-1000",
    price="79.99",
    price_currency="USD",
    availability="InStock",
)
```

### Organization (`entity_type="organization"`)

| Field    | Source               |
|----------|----------------------|
| `sameAs` | `entity.same_as`     |
| `logo`   | `config.publisher_logo` |

```python
entity = SEOEntity(
    entity_type="organization",
    title="Acme Inc",
    same_as=[
        "https://twitter.com/acme",
        "https://facebook.com/acme",
    ],
)
```

### LocalBusiness (`entity_type="local_business"`)

Extends Organization builder. Adds:

| Field                     | Source             |
|---------------------------|--------------------|
| `address.@type`           | `"PostalAddress"`  |
| `address.streetAddress`   | `entity.address`   |

```python
entity = SEOEntity(
    entity_type="local_business",
    title="My Shop",
    address="123 Main St",
    same_as=["https://fb.me/shop"],
)
```

### FAQPage (`entity_type="faq"`)

| Field                           | Source                               |
|---------------------------------|--------------------------------------|
| `mainEntity[].@type`            | `"Question"`                         |
| `mainEntity[].name`             | `faq_item.question`                  |
| `mainEntity[].acceptedAnswer.@type` | `"Answer"`                       |
| `mainEntity[].acceptedAnswer.text`  | `faq_item.answer`                |

```python
from seoslug import FAQItem

entity = SEOEntity(
    entity_type="faq",
    title="FAQ",
    faq_items=[
        FAQItem(question="Q1?", answer="A1."),
        FAQItem(question="Q2?", answer="A2."),
    ],
)
```

## BreadcrumbList auto-generation

When `SEOEntity.breadcrumbs` is set, seoslug appends a BreadcrumbList schema to the output.

Breadcrumbs merge with the main schema. If 1 schema total, it stays a dict. If 2+, it becomes a list.

```python
from seoslug import Breadcrumb

entity = SEOEntity(
    entity_type="post",
    title="My Post",
    breadcrumbs=[
        Breadcrumb(name="Home", url="/"),
        Breadcrumb(name="Blog", url="/blog"),
        Breadcrumb(name="My Post", url="/blog/my-post"),
    ],
)
```

Generated BreadcrumbList:

```python
{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "Home",
            "item": "https://blog.example.com/"
        },
        {
            "@type": "ListItem",
            "position": 2,
            "name": "Blog",
            "item": "https://blog.example.com/blog"
        },
    ],
}
```

## SchemaRegistry for custom generators

Register custom schema generators for any schema.org type.
When registered, the custom generator takes priority over built-in builders.

```python
from seoslug import SchemaRegistry

registry = SchemaRegistry()

def my_podcast_gen(entity, config, canonical, title, description, og_image):
    return {
        "@context": "https://schema.org",
        "@type": "Podcast",
        "name": title,
        "url": canonical,
        "description": description,
    }

registry.register("Podcast", my_podcast_gen)

config = SEOConfig(
    ...,
    schema_type_map={"other": "Podcast"},
    schema_registry=registry,
)
```

See the [Registry](registry.md) doc for full details.

## Generic fallback for unmapped types

If a schema type is mapped in `schema_type_map` but has no built-in builder and no registry entry, seoslug uses a generic fallback.

The fallback produces the standard fields: name, url, description, image, dates, author, publisher.

This means you can map any entity type to any schema.org type string and get valid output.

```python
config = SEOConfig(
    ...,
    schema_type_map={
        "post": "TechArticle",       # uses generic fallback
        "event": "Event",            # uses generic fallback
    },
)
```

## Disable, override, omit

Three levels of control over schema output.

**Disable globally**: turn off auto-generation for all entities:

```python
config = SEOConfig(
    ...,
    auto_generate_schema=False,
)
```

**Override per entity**: provide a custom schema dict or list:

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

overrides = SEOOverrides(schema_jsonld=[
    {"@context": "https://schema.org", "@type": "Article", "name": "Post"},
    {"@context": "https://schema.org", "@type": "BreadcrumbList", ...},
])
```

**Omit per entity**: remove schema entirely (even breadcrumbs are suppressed):

```python
overrides = SEOOverrides(omit_schema=True)
```

Precedence:

1. `omit_schema=True` wins over everything
2. `schema_jsonld` override (dict or list)
3. Auto-generated schema (if `auto_generate_schema` is True)
4. BreadcrumbList (appended to whatever is above)
