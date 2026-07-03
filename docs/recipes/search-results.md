---
seo:
  title: 'Recipe: Search Results - seoslug'
  canonical: https://seoslug.emiliano-go.com/recipes/search-results/
  robots: index,follow
  og:
    type: website
    title: 'Recipe: Search Results - seoslug'
    description: A search results page with SearchResultsPage schema and noindex directive.
      Tracking params are stripped from the canonical URL.
    url: https://seoslug.emiliano-go.com/recipes/search-results/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: 'Recipe: Search Results - seoslug'
    description: A search results page with SearchResultsPage schema and noindex directive.
      Tracking params are stripped from the canonical URL.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: A search results page with SearchResultsPage schema and noindex directive.
    Tracking params are stripped from the canonical URL.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: 'Recipe: Search Results - seoslug'
    url: https://seoslug.emiliano-go.com/recipes/search-results/
    description: A search results page with SearchResultsPage schema and noindex directive.
      Tracking params are stripped from the canonical URL.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Recipe: Search Results - seoslug</title>\n<meta name=\"description\"\
  \ content=\"A search results page with SearchResultsPage schema and noindex directive.\
  \ Tracking params are stripped from the canonical URL.\">\n<link rel=\"canonical\"\
  \ href=\"https://seoslug.emiliano-go.com/recipes/search-results/\">\n<meta name=\"\
  robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"website\"\
  >\n<meta property=\"og:title\" content=\"Recipe: Search Results - seoslug\">\n<meta\
  \ property=\"og:description\" content=\"A search results page with SearchResultsPage\
  \ schema and noindex directive. Tracking params are stripped from the canonical\
  \ URL.\">\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/recipes/search-results/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Recipe: Search Results - seoslug\">\n\
  <meta name=\"twitter:description\" content=\"A search results page with SearchResultsPage\
  \ schema and noindex directive. Tracking params are stripped from the canonical\
  \ URL.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Recipe: Search Results - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/recipes/search-results/\"\
  ,\n  \"description\": \"A search results page with SearchResultsPage schema and\
  \ noindex directive. Tracking params are stripped from the canonical URL.\",\n \
  \ \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n \
  \ \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano Gandini\
  \ Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

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
