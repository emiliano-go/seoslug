---
seo:
  title: SchemaRegistry - seoslug
  canonical: https://seoslug.emiliano-go.com/registry/
  robots: index,follow
  og:
    type: website
    title: SchemaRegistry - seoslug
    description: SchemaRegistry lets you register custom JSON-LD generators for any
      schema.org type. When a schema type matches a registered generator, it is called
      instead of...
    url: https://seoslug.emiliano-go.com/registry/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: SchemaRegistry - seoslug
    description: SchemaRegistry lets you register custom JSON-LD generators for any
      schema.org type. When a schema type matches a registered generator, it is called
      instead of...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: SchemaRegistry lets you register custom JSON-LD generators for any
    schema.org type. When a schema type matches a registered generator, it is called
    instead of...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: SchemaRegistry - seoslug
    url: https://seoslug.emiliano-go.com/registry/
    description: SchemaRegistry lets you register custom JSON-LD generators for any
      schema.org type. When a schema type matches a registered generator, it is called
      instead of...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>SchemaRegistry - seoslug</title>\n<meta name=\"description\" content=\"\
  SchemaRegistry lets you register custom JSON-LD generators for any schema.org type.\
  \ When a schema type matches a registered generator, it is called instead of...\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/registry/\">\n\
  <meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"SchemaRegistry - seoslug\">\n\
  <meta property=\"og:description\" content=\"SchemaRegistry lets you register custom\
  \ JSON-LD generators for any schema.org type. When a schema type matches a registered\
  \ generator, it is called instead of...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/registry/\">\n<meta property=\"og:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta property=\"\
  og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\" content=\"\
  768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\">\n<meta\
  \ property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\" content=\"\
  en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\">\n<meta name=\"\
  twitter:title\" content=\"SchemaRegistry - seoslug\">\n<meta name=\"twitter:description\"\
  \ content=\"SchemaRegistry lets you register custom JSON-LD generators for any schema.org\
  \ type. When a schema type matches a registered generator, it is called instead\
  \ of...\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"SchemaRegistry - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/registry/\"\
  ,\n  \"description\": \"SchemaRegistry lets you register custom JSON-LD generators\
  \ for any schema.org type. When a schema type matches a registered generator, it\
  \ is called instead of...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# SchemaRegistry

`SchemaRegistry` lets you register custom JSON-LD generators for any schema.org type.
When a schema type matches a registered generator, it is called instead of the built-in builder.

This is how you extend seoslug for schema types it does not support natively.

## Quick start

```python
from seoslug import SchemaRegistry, SEOConfig

registry = SchemaRegistry()

def podcast_gen(entity, config, canonical, title, description, og_image):
    return {
        "@context": "https://schema.org",
        "@type": "Podcast",
        "name": title,
        "url": canonical,
        "description": description,
    }

registry.register("Podcast", podcast_gen)

config = SEOConfig(
    ...,
    schema_type_map={"other": "Podcast"},
    schema_registry=registry,
)
```

## register / unregister / get

```python
registry = SchemaRegistry()

# Register
registry.register("Podcast", my_generator)

# Look up
gen = registry.get("Podcast")  # returns my_generator or None

# Unregister
registry.unregister("Podcast")
registry.get("Podcast")  # None
```

`register` raises `ValueError` for empty schema type strings.

## Generator protocol / signature

Every generator must match the `SchemaGenerator` protocol:

```python
from seoslug.schemas import SEOEntity
from seoslug.config import SEOConfig
from typing import Protocol

class SchemaGenerator(Protocol):
    def __call__(
        self,
        entity: SEOEntity,
        config: SEOConfig,
        canonical: str,
        title: str,
        description: str | None,
        og_image: str | None,
    ) -> dict | None: ...
```

Parameters:

| Parameter     | Type         | Description        |
|---------------|--------------|--------------------|
| `entity`      | `SEOEntity`  | The content entity |
| `config`      | `SEOConfig`  | Your configuration |
| `canonical`   | `str`        | Resolved canonical URL |
| `title`       | `str`        | Resolved page title |
| `description` | `str \| None` | Resolved description |
| `og_image`    | `str \| None` | Resolved OG image URL |

Return a `dict` for a single schema, or `None` to skip.

## Dispatch priority

When `build_schema()` looks up a schema type, it follows this order:

1. **Registry**: if a generator is registered for the schema type, call it
2. **Built-in builder**: if no registry match, check built-in builders (Product, Organization, LocalBusiness, FAQPage)
3. **Generic fallback**: produce a standard schema with name, url, description, image, dates, author, publisher

Each step is tried in sequence. The first match wins.

```
Registry match?
  Yes -> call registered generator
  No  -> Built-in builder exists?
           Yes -> call built-in builder
           No  -> Generic fallback
```

## Example: Custom Podcast schema

```python
from seoslug import SchemaRegistry, SEOConfig, URLPolicy, SEOEntity, build_seo_payload

registry = SchemaRegistry()

def podcast_gen(entity, config, canonical, title, description, og_image):
    schema = {
        "@context": "https://schema.org",
        "@type": "Podcast",
        "name": title,
        "url": canonical,
    }
    if description:
        schema["description"] = description
    if og_image:
        schema["image"] = og_image
    if entity.author_name:
        schema["author"] = {"@type": "Person", "name": entity.author_name}
    if entity.same_as:
        schema["sameAs"] = entity.same_as
    return schema

registry.register("Podcast", podcast_gen)

config = SEOConfig(
    canonical_host="podcast.example.com",
    public_base_url="https://podcast.example.com",
    url_policy=URLPolicy(),
    schema_type_map={"post": "Podcast"},
    schema_registry=registry,
)

entity = SEOEntity(
    entity_type="post",
    title="Episode 42: The Future of AI",
    author_name="Jane Doe",
    same_as=["https://twitter.com/mypodcast"],
)

payload = build_seo_payload(entity, "/episodes/42", config)
# payload["schema_jsonld"]["@type"] == "Podcast"
```

## When to use the registry

- Custom schema.org types not in the built-in set (e.g. Podcast, Event, Recipe, Course)
- Overriding built-in behavior for a specific schema type (registry dispatch takes priority over built-in builders)
- Per-type custom logic (e.g. always add `aggregateRating` for Product schemas)

For simple per-page overrides, use `SEOOverrides(schema_jsonld=...)` instead.
