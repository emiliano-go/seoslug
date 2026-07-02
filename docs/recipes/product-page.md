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
