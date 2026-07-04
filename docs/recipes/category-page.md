---
{}
---

# Recipe: Category / Taxonomy Page

A category page with CollectionPage schema, title template, and default OG image.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(
        lowercase_paths=True,
        trailing_slash="never",
        strip_tracking_params=True,
    ),
    title_template="{title} - Category - My Blog",
    site_name="My Blog",
    default_og_image="https://cdn.example.com/category-default.jpg",
    schema_type_map={"taxonomy": "CollectionPage"},
)
```

## Entity

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="taxonomy",
    title="Python Tutorials",
    excerpt="A collection of Python tutorials for beginners and advanced users.",
    status="published",
)
```

## Generate

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/topics/python", config)
```

## Result

```python
{
    "title": "Python Tutorials - Category - My Blog",
    "description": "A collection of Python tutorials for beginners and advanced users.",
    "canonical": "https://blog.example.com/topics/python",
    "robots": "index,follow",
    "og": {
        "type": "website",
        "title": "Python Tutorials - Category - My Blog",
        "description": "A collection of Python tutorials for beginners and advanced users.",
        "url": "https://blog.example.com/topics/python",
        "image": "https://cdn.example.com/category-default.jpg",
        "site_name": "My Blog",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Python Tutorials - Category - My Blog",
        "description": "A collection of Python tutorials for beginners and advanced users.",
        "image": "https://cdn.example.com/category-default.jpg",
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Python Tutorials - Category - My Blog",
        "url": "https://blog.example.com/topics/python",
        "description": "A collection of Python tutorials for beginners and advanced users.",
        "image": "https://cdn.example.com/category-default.jpg",
    },
}
```

## With breadcrumbs

```python
from seoslug import Breadcrumb

entity = SEOEntity(
    entity_type="taxonomy",
    title="Python Tutorials",
    excerpt="A collection of Python tutorials.",
    status="published",
    breadcrumbs=[
        Breadcrumb(name="Home", url="/"),
        Breadcrumb(name="Tutorials", url="/tutorials"),
        Breadcrumb(name="Python", url="/tutorials/python"),
    ],
)
```

The `schema_jsonld` becomes a list with both CollectionPage and BreadcrumbList.
