# Recipe: Search Results

A search results page with SearchResultsPage schema and noindex directive.
Tracking params are stripped from the canonical URL.

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
        allowed_query_params=["q", "page"],
    ),
    title_template="{title}",
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

payload = build_seo_payload(
    entity,
    "/search?q=python&utm_source=twitter&page=1",
    config,
)
```

## Result

```python
{
    "title": "Search results for: python",
    "description": "Showing results for python tutorials.",
    "canonical": "https://blog.example.com/search?q=python&page=1",
    "robots": "noindex,follow",
    "og": {
        "type": "website",
        "title": "Search results for: python",
        "description": "Showing results for python tutorials.",
        "url": "https://blog.example.com/search?q=python&page=1",
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
        "url": "https://blog.example.com/search?q=python&page=1",
        "description": "Showing results for python tutorials.",
    },
}
```

## Key behaviors

- `search_robots` is set to `"noindex,follow"` so search result pages are not indexed
- `allowed_query_params` keeps only `q` and `page` in the canonical URL
- `strip_tracking_params=True` removes `utm_source` and other tracking params
- The schema type is `SearchResultsPage` per the default mapping
