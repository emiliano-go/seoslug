# Recipe: Product page

Product pages need Product schema with price, availability, and ratings.
Use SEOOverrides to supply the custom schema fields that seoslug does not generate automatically.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="shop.example.com",
    public_base_url="https://shop.example.com",
    url_policy=URLPolicy(lowercase_paths=True, trailing_slash="never"),
    title_template="{title} - My Shop",
    schema_type_map={"product": "Product"},
)
```

## Entity

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="product",
    title="Wireless Headphones",
    excerpt="Premium wireless headphones with noise cancellation.",
    status="published",
    featured_image="https://cdn.example.com/headphones.jpg",
)
```

## Generate with custom schema

```python
from seoslug import SEOOverrides, build_seo_payload

overrides = SEOOverrides(schema_jsonld={
    "@context": "https://schema.org",
    "@type": "Product",
    "name": "Wireless Headphones",
    "description": "Premium wireless headphones with noise cancellation.",
    "image": "https://cdn.example.com/headphones.jpg",
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
})

payload = build_seo_payload(entity, "/products/headphones", config, overrides)
```

## Result

```python
{
    "title": "Wireless Headphones - My Shop",
    "description": "Premium wireless headphones with noise cancellation.",
    "canonical": "https://shop.example.com/products/headphones",
    "robots": "index,follow",
    "og": {
        "type": "website",
        "title": "Wireless Headphones - My Shop",
        "description": "Premium wireless headphones with noise cancellation.",
        "url": "https://shop.example.com/products/headphones",
        "image": "https://cdn.example.com/headphones.jpg",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Wireless Headphones - My Shop",
        "description": "Premium wireless headphones with noise cancellation.",
        "image": "https://cdn.example.com/headphones.jpg",
    },
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": "Wireless Headphones",
        "description": "Premium wireless headphones with noise cancellation.",
        "image": "https://cdn.example.com/headphones.jpg",
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
    },
}
```
