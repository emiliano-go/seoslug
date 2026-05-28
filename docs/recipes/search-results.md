# Recipe: Search results

Search result pages use SearchResultsPage schema and should signal noindex to avoid duplicate content issues.

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
    search_robots="noindex,follow",
    schema_type_map={"search": "SearchResultsPage"},
)
```

## Entity

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="search",
    title="Search results for: python",
    excerpt="Showing results for python tutorials.",
    status="published",
)
```

## Generate

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/search?q=python", config)
```

## Result

```python
{
    "title": "Search results for: python",
    "description": "Showing results for python tutorials.",
    "canonical": "https://blog.example.com/search?q=python",
    "robots": "noindex,follow",
    "og": {
        "type": "website",
        "title": "Search results for: python",
        "description": "Showing results for python tutorials.",
        "url": "https://blog.example.com/search?q=python",
        "image": None,
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Search results for: python",
        "description": "Showing results for python tutorials.",
        "image": None,
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "SearchResultsPage",
        "name": "Search results for: python",
        "url": "https://blog.example.com/search?q=python",
        "description": "Showing results for python tutorials.",
    },
}
```
