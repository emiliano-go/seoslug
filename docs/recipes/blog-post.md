---
seo:
  title: 'Recipe: Blog Post - seoslug'
  canonical: https://seoslug.emiliano-go.com/recipes/blog-post/
  robots: index,follow
  og:
    type: website
    title: 'Recipe: Blog Post - seoslug'
    description: A blog post with BlogPosting schema, structured OGImage, breadcrumbs,
      author, and custom SchemaRegistry.
    url: https://seoslug.emiliano-go.com/recipes/blog-post/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: 'Recipe: Blog Post - seoslug'
    description: A blog post with BlogPosting schema, structured OGImage, breadcrumbs,
      author, and custom SchemaRegistry.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: A blog post with BlogPosting schema, structured OGImage, breadcrumbs,
    author, and custom SchemaRegistry.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: 'Recipe: Blog Post - seoslug'
    url: https://seoslug.emiliano-go.com/recipes/blog-post/
    description: A blog post with BlogPosting schema, structured OGImage, breadcrumbs,
      author, and custom SchemaRegistry.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Recipe: Blog Post - seoslug</title>\n<meta name=\"description\"\
  \ content=\"A blog post with BlogPosting schema, structured OGImage, breadcrumbs,\
  \ author, and custom SchemaRegistry.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/recipes/blog-post/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Recipe: Blog Post - seoslug\"\
  >\n<meta property=\"og:description\" content=\"A blog post with BlogPosting schema,\
  \ structured OGImage, breadcrumbs, author, and custom SchemaRegistry.\">\n<meta\
  \ property=\"og:url\" content=\"https://seoslug.emiliano-go.com/recipes/blog-post/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Recipe: Blog Post - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"A blog post with BlogPosting schema, structured\
  \ OGImage, breadcrumbs, author, and custom SchemaRegistry.\">\n<meta name=\"twitter:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Recipe: Blog\
  \ Post - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/recipes/blog-post/\"\
  ,\n  \"description\": \"A blog post with BlogPosting schema, structured OGImage,\
  \ breadcrumbs, author, and custom SchemaRegistry.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Recipe: Blog Post

A blog post with BlogPosting schema, structured OGImage, breadcrumbs, author, and custom SchemaRegistry.

## Configuration

```python
from seoslug import SEOConfig, URLPolicy, SchemaRegistry

# Custom generator for BlogPosting
registry = SchemaRegistry()

def blog_posting_gen(entity, config, canonical, title, description, og_image):
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": title,
        "url": canonical,
        "mainEntityOfPage": {"@id": canonical},
    }
    if description:
        schema["description"] = description
    if og_image:
        schema["image"] = og_image
    if entity.published_at:
        schema["datePublished"] = entity.published_at
    if entity.updated_at:
        schema["dateModified"] = entity.updated_at
    if entity.author_name:
        schema["author"] = {"@type": "Person", "name": entity.author_name}
    if config.publisher_name:
        publisher = {"@type": "Organization", "name": config.publisher_name}
        if config.publisher_logo:
            publisher["logo"] = config.publisher_logo
        schema["publisher"] = publisher
    return schema

registry.register("BlogPosting", blog_posting_gen)

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(
        strip_tracking_params=True,
        lowercase_paths=True,
        trailing_slash="never",
    ),
    title_template="{title} - My Blog",
    site_name="My Blog",
    publisher_name="My Company",
    default_og_image="https://cdn.example.com/default.jpg",
    schema_type_map={"post": "BlogPosting"},
    schema_registry=registry,
)
```

## Entity

```python
from seoslug import SEOEntity, OGImage, Breadcrumb

entity = SEOEntity(
    entity_type="post",
    title="Hello World",
    excerpt="A brief introduction to the blog.",
    body_html="<p>Full article content here.</p>",
    status="published",
    featured_image=OGImage(
        url="https://cdn.example.com/hello.jpg",
        width=1200,
        height=630,
        alt="Hello World featured image",
    ),
    published_at="2025-01-15",
    updated_at="2025-02-01",
    author_name="Jane Doe",
    breadcrumbs=[
        Breadcrumb(name="Home", url="/"),
        Breadcrumb(name="Blog", url="/blog"),
    ],
)
```

## Generate

```python
from seoslug import build_seo_payload

payload = build_seo_payload(entity, "/blog/hello-world", config)
```

## Result

```python
{
    "title": "Hello World - My Blog",
    "description": "A brief introduction to the blog.",
    "canonical": "https://blog.example.com/blog/hello-world",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "Hello World - My Blog",
        "description": "A brief introduction to the blog.",
        "url": "https://blog.example.com/blog/hello-world",
        "image": "https://cdn.example.com/hello.jpg",
        "image:width": 1200,
        "image:height": 630,
        "image:alt": "Hello World featured image",
        "site_name": "My Blog",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "Hello World - My Blog",
        "description": "A brief introduction to the blog.",
        "image": "https://cdn.example.com/hello.jpg",
        "image:alt": "Hello World featured image",
    },
    "schema_jsonld": [
        {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": "Hello World - My Blog",
            "url": "https://blog.example.com/blog/hello-world",
            "mainEntityOfPage": {"@id": "https://blog.example.com/blog/hello-world"},
            "description": "A brief introduction to the blog.",
            "image": "https://cdn.example.com/hello.jpg",
            "datePublished": "2025-01-15",
            "dateModified": "2025-02-01",
            "author": {"@type": "Person", "name": "Jane Doe"},
            "publisher": {
                "@type": "Organization",
                "name": "My Company",
            },
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://blog.example.com/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://blog.example.com/blog"},
            ],
        },
    ],
}
```
