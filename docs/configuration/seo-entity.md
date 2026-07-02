# SEOEntity reference

`SEOEntity` represents a single piece of content. It holds the raw data seoslug uses to generate every SEO field. Create one per page, pass it to `build_seo_payload`.

## Entity types

The `entity_type` field determines which schema.org type is used and how Open Graph type is set.

| Type | OG type | Default schema type | Description |
|---|---|---|---|
| `"home"` | `website` | `WebPage` | Homepage / landing page |
| `"post"` | `article` | `Article` | Blog post or article |
| `"page"` | `website` | `WebPage` | Static page (about, contact) |
| `"video"` | `article` | `VideoObject` | Video content page |
| `"taxonomy"` | `website` | `CollectionPage` | Category, tag, archive |
| `"search"` | `website` | `SearchResultsPage` | Search results page |
| `"other"` | `website` | (from schema_type_map) | Any other content type |
| `"product"` | `website` | `Product` | Product page |
| `"organization"` | `website` | `Organization` | Organization / about page |
| `"local_business"` | `website` | `LocalBusiness` | Local business page |
| `"faq"` | `website` | `FAQPage` | FAQ page |

## Fields

| Option | Type | Default | Description |
|---|---|---|---|
| `entity_type` | `Literal` | required | Content type from the table above. |
| `slug` | `str` or `None` | `None` | URL slug. Used as fallback title source. |
| `title` | `str` or `None` | `None` | Content title. Primary source for the title tag. |
| `excerpt` | `str` or `None` | `None` | Short description. Primary source for meta description. |
| `body_html` | `str` or `None` | `None` | Full HTML body. Fallback for description when excerpt is missing. |
| `status` | `str` or `None` | `None` | Publication status. `"published"` triggers `"index,follow"`. |
| `featured_image` | `str` or `OGImage` or `None` | `None` | Featured image URL or structured OGImage. |
| `published_at` | `str` or `None` | `None` | Publication date. Emitted as `datePublished` in JSON-LD. |
| `updated_at` | `str` or `None` | `None` | Last modified date. Emitted as `dateModified` in JSON-LD. |
| `author_name` | `str` or `None` | `None` | Author name. Emitted as `author` (Person) in JSON-LD. |
| `breadcrumbs` | `list[Breadcrumb]` or `None` | `None` | Breadcrumb trail. Emitted as `BreadcrumbList` JSON-LD. |
| `sku` | `str` or `None` | `None` | Stock-keeping unit. Used in Product schema. |
| `price` | `str` or `None` | `None` | Product price as string. Used in Product schema. |
| `price_currency` | `str` or `None` | `None` | ISO 4217 currency code. Used in Product schema. |
| `availability` | `str` or `None` | `None` | Schema.org availability (e.g. `"InStock"`). |
| `same_as` | `list[str]` or `None` | `None` | Social profile URLs. Emitted as `sameAs` in Organization schema. |
| `address` | `str` or `None` | `None` | Street address. Emitted in LocalBusiness schema. |
| `faq_items` | `list[FAQItem]` or `None` | `None` | FAQ question-answer pairs. Emitted as `mainEntity` in FAQPage schema. |

### entity_type (required)

Determines the entire shape of the SEO output. Each type maps to a schema.org type and an Open Graph type. See the entity types table above.

```python
SEOEntity(entity_type="post")
```

### slug

The URL slug. Used as a fallback when `title` is not set (avoids "Untitled").

```python
SEOEntity(entity_type="post", slug="my-post")
```

### title

The content title. Primary source for the title tag, `og:title`, and `twitter:title`. Defaults to `"Untitled"` when not set.

```python
SEOEntity(entity_type="post", title="My Post")
```

### excerpt

Short description. Primary source for the meta description tag. Also used for `og:description` and `twitter:description`.

```python
SEOEntity(entity_type="post", excerpt="A brief description")
```

### body_html

Full HTML body. When `excerpt` is not set, seoslug extracts a plain-text snippet from `body_html` and truncates it to 160 characters for the description.

```python
SEOEntity(entity_type="post", body_html="<p>Full article content here</p>")
```

### status

Publication status. When set to `"published"` (case-insensitive), the entity gets `"index,follow"` as its default robots directive. Any other value uses `config.default_robots`. Entities with `entity_type="search"` always use `config.search_robots`.

```python
SEOEntity(entity_type="post", status="published")
```

### featured_image

The featured image for Open Graph and Twitter Cards. Accepts a plain URL string or a structured `OGImage` dataclass with width, height, and alt text.

```python
# String form
SEOEntity(
    entity_type="post",
    featured_image="https://cdn.example.com/image.jpg",
)

# Structured form
from seoslug import OGImage

SEOEntity(
    entity_type="post",
    featured_image=OGImage(
        url="https://cdn.example.com/image.jpg",
        width=1200,
        height=630,
        alt="Post image",
    ),
)
```

When structured, dimensions and alt text are emitted as `og:image:width`, `og:image:height`, and `og:image:alt`.

### published_at

Publication date as an ISO date string. Added to JSON-LD schema as `datePublished`.

```python
SEOEntity(entity_type="post", published_at="2025-01-15")
```

### updated_at

Last modified date. Added to JSON-LD schema as `dateModified`.

```python
SEOEntity(entity_type="post", updated_at="2025-02-01")
```

### author_name

Author display name. Added to JSON-LD schema as an `author` field with `@type: Person`.

```python
SEOEntity(entity_type="post", author_name="Jane Doe")
```

### breadcrumbs

A list of `Breadcrumb` dataclass instances. Automatically generates a `BreadcrumbList` JSON-LD schema that merges with the main schema output.

```python
from seoslug import Breadcrumb

SEOEntity(
    entity_type="page",
    breadcrumbs=[
        Breadcrumb(name="Home", url="/"),
        Breadcrumb(name="Blog", url="/blog"),
        Breadcrumb(name="Category", url="/blog/category"),
    ],
)
```

### sku

Stock-keeping unit identifier for Product schema. Emitted in JSON-LD as `sku`.

```python
SEOEntity(entity_type="product", sku="WIDGET-001")
```

### price

Product price. String value emitted in JSON-LD under `offers.price`. Used together with `price_currency` and `availability` to build the `offers` object.

```python
SEOEntity(
    entity_type="product",
    price="29.99",
    price_currency="USD",
    availability="InStock",
)
```

### price_currency

ISO 4217 currency code (e.g. `"USD"`, `"EUR"`). Emitted as `offers.priceCurrency`.

### availability

Schema.org availability value. Prepended with `https://schema.org/` in the output. Common values: `"InStock"`, `"OutOfStock"`, `"PreOrder"`, `"Discontinued"`.

```python
SEOEntity(
    entity_type="product",
    availability="InStock",
)
```

Output: `"availability": "https://schema.org/InStock"`

### same_as

List of social profile URLs. Emitted as `sameAs` in Organization and LocalBusiness schemas.

```python
SEOEntity(
    entity_type="organization",
    same_as=[
        "https://twitter.com/myorg",
        "https://github.com/myorg",
    ],
)
```

### address

Street address string. Emitted as `address.streetAddress` in LocalBusiness schema.

```python
SEOEntity(
    entity_type="local_business",
    address="123 Main St, Springfield, IL 62701",
)
```

### faq_items

List of `FAQItem` dataclass instances. Each item has a `question` and `answer` string. Emitted as `mainEntity` with `Question`/`Answer` types in FAQPage schema.

```python
from seoslug import FAQItem

SEOEntity(
    entity_type="faq",
    faq_items=[
        FAQItem(question="What is seoslug?", answer="A deterministic SEO library."),
        FAQItem(question="Is it free?", answer="Yes, MIT licensed."),
    ],
)
```

## Complete example

A blog post with all common fields:

```python
from seoslug import SEOEntity

entity = SEOEntity(
    entity_type="post",
    slug="hello-world",
    title="Hello World",
    excerpt="A brief introduction",
    body_html="<p>Welcome to my blog.</p>",
    status="published",
    featured_image="https://cdn.example.com/hello.jpg",
    published_at="2025-01-15",
    author_name="Jane Doe",
)
```

A product with structured image:

```python
from seoslug import SEOEntity, OGImage

entity = SEOEntity(
    entity_type="product",
    title="Premium Widget",
    sku="PW-001",
    price="49.99",
    price_currency="USD",
    availability="InStock",
    featured_image=OGImage(
        url="https://cdn.example.com/widget.jpg",
        width=1200,
        height=1200,
        alt="Premium Widget",
    ),
)
```
