---
seo:
  title: Factory Functions - seoslug
  canonical: https://seoslug.emiliano-go.com/factories/
  robots: index,follow
  og:
    type: website
    title: Factory Functions - seoslug
    description: Factory functions create pre-configured SEOEntity instances for common
      content types. They save you from manually setting entitytype, status, and other...
    url: https://seoslug.emiliano-go.com/factories/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Factory Functions - seoslug
    description: Factory functions create pre-configured SEOEntity instances for common
      content types. They save you from manually setting entitytype, status, and other...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Factory functions create pre-configured SEOEntity instances for common
    content types. They save you from manually setting entitytype, status, and other...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Factory Functions - seoslug
    url: https://seoslug.emiliano-go.com/factories/
    description: Factory functions create pre-configured SEOEntity instances for common
      content types. They save you from manually setting entitytype, status, and other...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Factory Functions - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Factory functions create pre-configured SEOEntity instances for common\
  \ content types. They save you from manually setting entitytype, status, and other...\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/factories/\">\n\
  <meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Factory Functions - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Factory functions create pre-configured\
  \ SEOEntity instances for common content types. They save you from manually setting\
  \ entitytype, status, and other...\">\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/factories/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"Factory Functions\
  \ - seoslug\">\n<meta name=\"twitter:description\" content=\"Factory functions create\
  \ pre-configured SEOEntity instances for common content types. They save you from\
  \ manually setting entitytype, status, and other...\">\n<meta name=\"twitter:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Factory Functions\
  \ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/factories/\",\n  \"\
  description\": \"Factory functions create pre-configured SEOEntity instances for\
  \ common content types. They save you from manually setting entitytype, status,\
  \ and other...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Factory Functions

Factory functions create pre-configured `SEOEntity` instances for common content types.
They save you from manually setting `entity_type`, `status`, and other boilerplate.

## from_blog_post

Create an `SEOEntity` for a blog post.

```python
from seoslug import from_blog_post

entity = from_blog_post(
    title="Hello World",
    body_html="<p>Full article content here.</p>",
    slug="hello-world",
    author="Jane Doe",
    excerpt="Optional explicit excerpt",
    breadcrumbs=[
        {"name": "Home", "url": "/"},
        {"name": "Blog", "url": "/blog"},
    ],
)
```

Parameters:

| Parameter    | Type              | Required | Default   | Description |
|-------------|-------------------|----------|-----------|-------------|
| `title`     | `str`             | Yes      | -         | Post title |
| `body_html` | `str`             | Yes      | -         | Full HTML body (used for auto-description snippet) |
| `slug`      | `str \| None`     | No       | `None`    | URL slug |
| `author`    | `str`             | No       | `""`      | Author name |
| `excerpt`   | `str \| None`     | No       | `None`    | Explicit excerpt; falls back to body snippet |
| `breadcrumbs` | `list[dict] \| None` | No    | `None`    | List of `{"name": ..., "url": ...}` dicts |

The factory sets `entity_type="post"` and `status="published"`.

## from_product

Create an `SEOEntity` for a product page.

```python
from seoslug import from_product

entity = from_product(
    name="Wireless Headphones",
    sku="WH-1000",
    price=79.99,
    currency="USD",
    availability="InStock",
    description="Premium wireless headphones with noise cancellation.",
    breadcrumbs=[
        {"name": "Home", "url": "/"},
        {"name": "Audio", "url": "/audio"},
    ],
)
```

Parameters:

| Parameter      | Type                  | Required | Default    | Description |
|---------------|-----------------------|----------|------------|-------------|
| `name`        | `str`                 | Yes      | -          | Product name (becomes entity.title) |
| `sku`         | `str`                 | Yes      | -          | Stock keeping unit |
| `price`       | `str \| float`        | Yes      | -          | Price (numeric or string like "29.99") |
| `currency`    | `str`                 | No       | `"USD"`    | ISO 4217 currency code |
| `availability`| `str`                 | No       | `"InStock"`| Schema.org availability value |
| `description` | `str \| None`         | No       | `None`     | Product description (becomes excerpt) |
| `breadcrumbs` | `list[dict] \| None`  | No       | `None`     | List of `{"name": ..., "url": ...}` dicts |

The factory sets `entity_type="product"` and `status="published"`.

## from_faq

Create an `SEOEntity` for an FAQ page.

```python
from seoslug import from_faq

entity = from_faq(
    questions=[
        {"question": "How do I return an item?", "answer": "Contact support within 30 days."},
        {"question": "Do you ship internationally?", "answer": "Yes, we ship to 50+ countries."},
    ],
    title="Frequently Asked Questions",
    description="Answers to common questions about our service.",
    breadcrumbs=[
        {"name": "Home", "url": "/"},
        {"name": "FAQ", "url": "/faq"},
    ],
)
```

Parameters:

| Parameter      | Type                    | Required | Default   | Description |
|---------------|-------------------------|----------|-----------|-------------|
| `questions`   | `list[dict[str, str]]`  | Yes      | -         | List of `{"question": "...", "answer": "..."}` dicts |
| `title`       | `str`                   | No       | `"FAQ"`   | Page title |
| `description` | `str \| None`           | No       | `None`    | Meta description |
| `breadcrumbs` | `list[dict] \| None`    | No       | `None`    | List of `{"name": ..., "url": ...}` dicts |

The factory sets `entity_type="faq"` and `status="published"`. Each question dict is converted to a `FAQItem` object.
