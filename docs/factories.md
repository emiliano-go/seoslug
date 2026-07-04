---
{}
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
