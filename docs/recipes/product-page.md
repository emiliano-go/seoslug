---
seo:
  title: 'Recipe: Product Page - seoslug'
  canonical: https://seoslug.emiliano-go.com/recipes/product-page/
  robots: index,follow
  og:
    type: website
    title: 'Recipe: Product Page - seoslug'
    description: A product page with Product schema, SKU, price, availability, structured
      OGImage, and breadcrumbs.
    url: https://seoslug.emiliano-go.com/recipes/product-page/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: 'Recipe: Product Page - seoslug'
    description: A product page with Product schema, SKU, price, availability, structured
      OGImage, and breadcrumbs.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: A product page with Product schema, SKU, price, availability, structured
    OGImage, and breadcrumbs.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: 'Recipe: Product Page - seoslug'
    url: https://seoslug.emiliano-go.com/recipes/product-page/
    description: A product page with Product schema, SKU, price, availability, structured
      OGImage, and breadcrumbs.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Recipe: Product Page - seoslug</title>\n<meta name=\"description\"\
  \ content=\"A product page with Product schema, SKU, price, availability, structured\
  \ OGImage, and breadcrumbs.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/recipes/product-page/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Recipe: Product Page - seoslug\"\
  >\n<meta property=\"og:description\" content=\"A product page with Product schema,\
  \ SKU, price, availability, structured OGImage, and breadcrumbs.\">\n<meta property=\"\
  og:url\" content=\"https://seoslug.emiliano-go.com/recipes/product-page/\">\n<meta\
  \ property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"Recipe: Product Page\
  \ - seoslug\">\n<meta name=\"twitter:description\" content=\"A product page with\
  \ Product schema, SKU, price, availability, structured OGImage, and breadcrumbs.\"\
  >\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Recipe: Product Page - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/recipes/product-page/\"\
  ,\n  \"description\": \"A product page with Product schema, SKU, price, availability,\
  \ structured OGImage, and breadcrumbs.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Recipe: Product Page

A product page with Product schema, SKU, price, availability, structured OGImage, and breadcrumbs.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="shop.example.com",
    public_base_url="https://shop.example.com",
    url_policy=URLPolicy(
        lowercase_paths=True,
        trailing_slash="never",
        strip_tracking_params=True,
    ),
    title_template="{title} - My Shop",
    site_name="My Shop",
    default_og_image="https://cdn.example.com/default-product.jpg",
    schema_type_map={"product": "Product"},
)
```

## Entity

```python
from seoslug import SEOEntity, OGImage, Breadcrumb

entity = SEOEntity(
    entity_type="product",
    title="Wireless Headphones Pro",
    excerpt="Premium wireless headphones with active noise cancellation.",
    status="published",
    featured_image=OGImage(
        url="https://cdn.example.com/headphones.jpg",
        width=1200,
        height=1200,
        alt="Wireless Headphones Pro",
    ),
    sku="WH-PRO-001",
    price="79.99",
    price_currency="USD",
    availability="InStock",
    breadcrumbs=[
        Breadcrumb(name="Home", url="/"),
        Breadcrumb(name="Audio", url="/audio"),
        Breadcrumb(name="Headphones", url="/audio/headphones"),
    ],
)
```

## Generate

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/products/headphones-pro", config)
```

## Result

```python
{
    "title": "Wireless Headphones Pro - My Shop",
    "description": "Premium wireless headphones with active noise cancellation.",
    "canonical": "https://shop.example.com/products/headphones-pro",
    "robots": "index,follow",
    "og": {
        "type": "website",
        "title": "Wireless Headphones Pro - My Shop",
        "description": "Premium wireless headphones with active noise cancellation.",
        "url": "https://shop.example.com/products/headphones-pro",
        "image": "https://cdn.example.com/headphones.jpg",
        "image:width": 1200,
        "image:height": 1200,
        "image:alt": "Wireless Headphones Pro",
        "site_name": "My Shop",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Wireless Headphones Pro - My Shop",
        "description": "Premium wireless headphones with active noise cancellation.",
        "image": "https://cdn.example.com/headphones.jpg",
        "image:alt": "Wireless Headphones Pro",
    },
    "schema_jsonld": [
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": "Wireless Headphones Pro - My Shop",
            "url": "https://shop.example.com/products/headphones-pro",
            "description": "Premium wireless headphones with active noise cancellation.",
            "image": "https://cdn.example.com/headphones.jpg",
            "sku": "WH-PRO-001",
            "offers": {
                "@type": "Offer",
                "price": "79.99",
                "priceCurrency": "USD",
                "availability": "https://schema.org/InStock",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://shop.example.com/"},
                {"@type": "ListItem", "position": 2, "name": "Audio", "item": "https://shop.example.com/audio"},
                {"@type": "ListItem", "position": 3, "name": "Headphones", "item": "https://shop.example.com/audio/headphones"},
            ],
        },
    ],
}
```

## Custom schema override

For extra fields like `aggregateRating` or `brand`, use `SEOOverrides`:

```python
from seoslug import SEOOverrides

overrides = SEOOverrides(schema_jsonld={
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Wireless Headphones Pro",
    "description": "Premium wireless headphones with active noise cancellation.",
    "sku": "WH-PRO-001",
    "offers": {
        "@type": "Offer",
        "price": "79.99",
        "priceCurrency": "USD",
        "availability": "https://schema.org/InStock",
    },
    "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "4.5",
        "reviewCount": "128",
    },
    "brand": {
        "@type": "Brand",
        "name": "Acme Audio",
    },
})

payload = build_seo_payload(entity, "/products/headphones-pro", config, overrides)
```
