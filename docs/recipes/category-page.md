# Recipe: Category page

Category pages use CollectionPage schema and should inherit SEO fields from parent categories.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(lowercase_paths=True, trailing_slash="never"),
    title_template="{title} - Category - My Blog",
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
        "image": None,
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Python Tutorials - Category - My Blog",
        "description": "A collection of Python tutorials for beginners and advanced users.",
        "image": None,
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Python Tutorials - Category - My Blog",
        "url": "https://blog.example.com/topics/python",
        "description": "A collection of Python tutorials for beginners and advanced users.",
    },
}
```
