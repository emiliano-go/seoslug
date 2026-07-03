---
seo:
  title: 'Recipe: Category / Taxonomy Page - seoslug'
  canonical: https://seoslug.emiliano-go.com/recipes/category-page/
  robots: index,follow
  og:
    type: website
    title: 'Recipe: Category / Taxonomy Page - seoslug'
    description: A category page with CollectionPage schema, title template, and default
      OG image.
    url: https://seoslug.emiliano-go.com/recipes/category-page/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: 'Recipe: Category / Taxonomy Page - seoslug'
    description: A category page with CollectionPage schema, title template, and default
      OG image.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: A category page with CollectionPage schema, title template, and default
    OG image.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: 'Recipe: Category / Taxonomy Page - seoslug'
    url: https://seoslug.emiliano-go.com/recipes/category-page/
    description: A category page with CollectionPage schema, title template, and default
      OG image.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Recipe: Category / Taxonomy Page - seoslug</title>\n<meta name=\"\
  description\" content=\"A category page with CollectionPage schema, title template,\
  \ and default OG image.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/recipes/category-page/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Recipe: Category / Taxonomy Page\
  \ - seoslug\">\n<meta property=\"og:description\" content=\"A category page with\
  \ CollectionPage schema, title template, and default OG image.\">\n<meta property=\"\
  og:url\" content=\"https://seoslug.emiliano-go.com/recipes/category-page/\">\n<meta\
  \ property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"Recipe: Category\
  \ / Taxonomy Page - seoslug\">\n<meta name=\"twitter:description\" content=\"A category\
  \ page with CollectionPage schema, title template, and default OG image.\">\n<meta\
  \ name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Recipe: Category / Taxonomy Page - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/recipes/category-page/\"\
  ,\n  \"description\": \"A category page with CollectionPage schema, title template,\
  \ and default OG image.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
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
