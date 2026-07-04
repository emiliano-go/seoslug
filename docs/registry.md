---
{}
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
