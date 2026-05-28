# Static site generators

Static site generators benefit from deterministic SEO.
Generate all SEO payloads at build time and write them to JSON files.
In your templates, read the pre generated payload instead of calling seoslug at request time.
This gives you complete SEO without runtime overhead.

## Build time generation

Create a script that generates SEO payloads for all your content.

```python
import json
from pathlib import Path
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)

posts = [
    {"slug": "hello-world", "title": "Hello World"},
    {"slug": "second-post", "title": "Second Post"},
]

output_dir = Path("_data/seo")
output_dir.mkdir(parents=True, exist_ok=True)

for post in posts:
    entity = SEOEntity(
        entity_type="post",
        title=post["title"],
        status="published",
    )
    payload = build_seo_payload(entity, f"/posts/{post['slug']}", config)
    path = output_dir / f"{post['slug']}.json"
    path.write_text(json.dumps(payload, indent=2))
```

## Pelican plugin

In Pelican, call seoslug during content generation.

```python
from pelican import signals
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)

def add_seo_metadata(content):
    entity = SEOEntity(
        entity_type="post",
        title=content.title,
        excerpt=getattr(content, "summary", None),
        status="published",
    )
    content.seo_payload = build_seo_payload(
        entity, content.url, config,
    )

def register():
    signals.content_object_init.connect(add_seo_metadata)
```

## MkDocs plugin

In MkDocs, use the `on_page_markdown` event.

```python
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="docs.example.com",
    public_base_url="https://docs.example.com",
    url_policy=URLPolicy(),
)

def on_page_markdown(markdown, page, config, files):
    entity = SEOEntity(
        entity_type="page",
        title=page.title,
        status="published",
    )
    page.seo_payload = build_seo_payload(
        entity, page.url, config,
    )
```

## Template usage

In your templates, read the payload from the pre generated file.

```jinja
<head>
    <title>{{ seo.title }}</title>
    <meta name="description" content="{{ seo.description }}">
    <link rel="canonical" href="{{ seo.canonical }}">
</head>
```
