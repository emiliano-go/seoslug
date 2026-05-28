# SEOEntity reference

`SEOEntity` represents your content.
It holds the data seoslug needs to generate metadata.

## Fields

### entity_type (required)

The type of content.
Accepts one of these values: `"home"`, `"post"`, `"page"`, `"video"`, `"taxonomy"`, `"search"`, `"other"`.

The entity type determines the Open Graph type and the schema.org type.

```python
SEOEntity(entity_type="post")
```

### slug (optional)

The URL slug for the entity.
Used as a fallback source for the title if title is not set.

```python
SEOEntity(entity_type="post", slug="my-post")
```

### title (optional)

The title of the content.
Used as the primary source for the title tag.
Defaults to "Untitled" if not set.

```python
SEOEntity(entity_type="post", title="My Post")
```

### excerpt (optional)

A short description of the content.
Used as the primary source for the meta description.

```python
SEOEntity(entity_type="post", excerpt="A brief description")
```

### body_html (optional)

The full HTML body of the content.
Used as a fallback for the description when excerpt is not set.
The HTML is converted to plain text and truncated to 160 characters.

```python
SEOEntity(entity_type="post", body_html="<p>Full article content here</p>")
```

### status (optional)

The publication status.
Accepted values include `"published"`, `"draft"`, or any string.
Published content gets `"index,follow"` as the default robots directive.
Unpublished content uses `default_robots` from SEOConfig.

```python
SEOEntity(entity_type="post", status="published")
```

### featured_image (optional)

The URL of the featured image.
Used as the primary source for Open Graph and Twitter card images.

```python
SEOEntity(
    entity_type="post",
    featured_image="https://cdn.example.com/image.jpg",
)
```

### published_at (optional)

The publication date as a string.
Added to JSON-LD as `datePublished`.

```python
SEOEntity(entity_type="post", published_at="2025-01-15")
```

### updated_at (optional)

The last update date as a string.
Added to JSON-LD as `dateModified`.

```python
SEOEntity(entity_type="post", updated_at="2025-02-01")
```

### author_name (optional)

The author's display name.
Added to JSON-LD as an `author` field with type Person.

```python
SEOEntity(entity_type="post", author_name="Jane Doe")
```

## Example

A complete entity for a published blog post.

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
