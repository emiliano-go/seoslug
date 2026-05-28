# Recipe: Blog post

A blog post needs an Article schema, Open Graph tags for social sharing, and a canonical URL that strips tracking parameters.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(
        strip_tracking_params=True,
        lowercase_paths=True,
        trailing_slash="never",
    ),
    default_og_image="https://cdn.example.com/default.jpg",
    title_template="{title} - My Blog",
    site_name="My Blog",
    schema_type_map={"post": "BlogPosting"},
    publisher_name="My Company",
)
```

## Entity

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    title="Hello World",
    excerpt="A brief introduction to the blog.",
    body_html="<p>Full article content here.</p>",
    status="published",
    featured_image="https://cdn.example.com/hello.jpg",
    published_at="2025-01-15",
    author_name="Jane Doe",
)
```

## Generate

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/blog/hello-world", config)
```

## Result

```python
{
    "title": "Hello World - My Blog",
    "description": "A brief introduction to the blog.",
    "canonical": "https://blog.example.com/blog/hello-world",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "Hello World - My Blog",
        "description": "A brief introduction to the blog.",
        "url": "https://blog.example.com/blog/hello-world",
        "image": "https://cdn.example.com/hello.jpg",
        "site_name": "My Blog",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Hello World - My Blog",
        "description": "A brief introduction to the blog.",
        "image": "https://cdn.example.com/hello.jpg",
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "name": "Hello World - My Blog",
        "url": "https://blog.example.com/blog/hello-world",
        "description": "A brief introduction to the blog.",
        "image": "https://cdn.example.com/hello.jpg",
        "datePublished": "2025-01-15",
        "mainEntityOfPage": {
            "@id": "https://blog.example.com/blog/hello-world"
        },
        "author": {
            "@type": "Person",
            "name": "Jane Doe"
        },
        "publisher": {
            "@type": "Organization",
            "name": "My Company"
        },
    },
}
```
