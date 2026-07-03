---
seo:
  title: SEOEntityBuilder - seoslug
  canonical: https://seoslug.emiliano-go.com/builder-pattern/
  robots: index,follow
  og:
    type: website
    title: SEOEntityBuilder - seoslug
    description: SEOEntityBuilder is a fluent builder for SEOEntity. Use it when you
      prefer method chaining over constructor arguments.
    url: https://seoslug.emiliano-go.com/builder-pattern/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: SEOEntityBuilder - seoslug
    description: SEOEntityBuilder is a fluent builder for SEOEntity. Use it when you
      prefer method chaining over constructor arguments.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: SEOEntityBuilder is a fluent builder for SEOEntity. Use it when you
    prefer method chaining over constructor arguments.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: SEOEntityBuilder - seoslug
    url: https://seoslug.emiliano-go.com/builder-pattern/
    description: SEOEntityBuilder is a fluent builder for SEOEntity. Use it when you
      prefer method chaining over constructor arguments.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>SEOEntityBuilder - seoslug</title>\n<meta name=\"description\" content=\"\
  SEOEntityBuilder is a fluent builder for SEOEntity. Use it when you prefer method\
  \ chaining over constructor arguments.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/builder-pattern/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"SEOEntityBuilder - seoslug\">\n\
  <meta property=\"og:description\" content=\"SEOEntityBuilder is a fluent builder\
  \ for SEOEntity. Use it when you prefer method chaining over constructor arguments.\"\
  >\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/builder-pattern/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"SEOEntityBuilder\
  \ - seoslug\">\n<meta name=\"twitter:description\" content=\"SEOEntityBuilder is\
  \ a fluent builder for SEOEntity. Use it when you prefer method chaining over constructor\
  \ arguments.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"SEOEntityBuilder - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/builder-pattern/\"\
  ,\n  \"description\": \"SEOEntityBuilder is a fluent builder for SEOEntity. Use\
  \ it when you prefer method chaining over constructor arguments.\",\n  \"image\"\
  : \"https://seoslug.emiliano-go.com/assets/icon.png\",\n  \"publisher\": {\n   \
  \ \"@type\": \"Organization\",\n    \"name\": \"Emiliano Gandini Outeda\"\n  }\n\
  }\n</script>\n"
---

# SEOEntityBuilder

`SEOEntityBuilder` is a fluent builder for `SEOEntity`.
Use it when you prefer method chaining over constructor arguments.

```python
from seoslug import SEOEntityBuilder

entity = (
    SEOEntityBuilder()
    .entity_type("product")
    .title("Wireless Headphones")
    .sku("WH-1000")
    .price(79.99)
    .price_currency("USD")
    .availability("InStock")
    .build()
)
```

## entity_type requirement

`entity_type` is required. The builder raises `ValueError` if you call `build()` without it.

```python
from seoslug import SEOEntityBuilder

try:
    SEOEntityBuilder().build()
except ValueError as e:
    print(e)  # "entity_type is required"
```

## All builder methods

Every method returns `self` for chaining.

| Method              | Parameter Type        | Maps to             |
|---------------------|-----------------------|---------------------|
| `.entity_type()`    | `str`                 | `entity_type` (required) |
| `.slug()`           | `str`                 | `slug`              |
| `.title()`          | `str`                 | `title`             |
| `.excerpt()`        | `str`                 | `excerpt`           |
| `.body_html()`      | `str`                 | `body_html`         |
| `.status()`         | `str`                 | `status`            |
| `.featured_image()` | `str \| OGImage`      | `featured_image`    |
| `.published_at()`   | `str`                 | `published_at`      |
| `.updated_at()`     | `str`                 | `updated_at`        |
| `.author_name()`    | `str`                 | `author_name`       |
| `.breadcrumbs()`    | `list[Breadcrumb]`    | `breadcrumbs`       |
| `.sku()`            | `str`                 | `sku`               |
| `.price()`          | `str \| float`        | `price` (converted to str) |
| `.price_currency()` | `str`                 | `price_currency`    |
| `.availability()`   | `str`                 | `availability`      |
| `.same_as()`        | `list[str]`           | `same_as`           |
| `.address()`        | `str`                 | `address`           |
| `.faq_items()`      | `list[FAQItem]`       | `faq_items`         |
| `.build()`          | -                     | Returns `SEOEntity` |

## Full example

```python
from seoslug import SEOEntityBuilder, Breadcrumb, FAQItem, OGImage

entity = (
    SEOEntityBuilder()
    .entity_type("product")
    .title("Widget Pro")
    .slug("widget-pro")
    .excerpt("The ultimate widget")
    .body_html("<p>Full description of Widget Pro.</p>")
    .status("published")
    .featured_image(OGImage(url="https://cdn.example.com/pro.jpg", width=1200, height=630, alt="Widget Pro"))
    .published_at("2025-01-15")
    .updated_at("2025-02-01")
    .author_name("Jane Doe")
    .breadcrumbs([
        Breadcrumb(name="Home", url="/"),
        Breadcrumb(name="Products", url="/products"),
    ])
    .sku("WIDGET-PRO-001")
    .price(99.99)
    .price_currency("USD")
    .availability("InStock")
    .same_as(["https://twitter.com/widgetpro"])
    .address("123 Widget St")
    .faq_items([FAQItem(question="Is it waterproof?", answer="Yes.")])
    .build()
)
```

## When to use it

Use the builder when:

- You prefer method chaining over positional arguments
- You need to conditionally set fields
- You want to pass the builder around before calling `build()`

Use `SEOEntity(...)` directly when you have all data upfront.
