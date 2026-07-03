---
seo:
  title: FastAPI integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/fastapi/
  robots: index,follow
  og:
    type: website
    title: FastAPI integration - seoslug
    description: Use buildseopayloadasync from seoslug.asyncbuilder in your route
      handlers. It runs the synchronous builder in a thread pool so it does not block
      the event loop.
    url: https://seoslug.emiliano-go.com/integrations/fastapi/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: FastAPI integration - seoslug
    description: Use buildseopayloadasync from seoslug.asyncbuilder in your route
      handlers. It runs the synchronous builder in a thread pool so it does not block
      the event loop.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: Use buildseopayloadasync from seoslug.asyncbuilder in your route handlers.
    It runs the synchronous builder in a thread pool so it does not block the event
    loop.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: FastAPI integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/fastapi/
    description: Use buildseopayloadasync from seoslug.asyncbuilder in your route
      handlers. It runs the synchronous builder in a thread pool so it does not block
      the event loop.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>FastAPI integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Use buildseopayloadasync from seoslug.asyncbuilder in your route handlers.\
  \ It runs the synchronous builder in a thread pool so it does not block the event\
  \ loop.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/fastapi/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"FastAPI integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Use buildseopayloadasync from seoslug.asyncbuilder\
  \ in your route handlers. It runs the synchronous builder in a thread pool so it\
  \ does not block the event loop.\">\n<meta property=\"og:url\" content=\"https://seoslug.emiliano-go.com/integrations/fastapi/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"FastAPI integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Use buildseopayloadasync from seoslug.asyncbuilder\
  \ in your route handlers. It runs the synchronous builder in a thread pool so it\
  \ does not block the event loop.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"FastAPI integration - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/fastapi/\"\
  ,\n  \"description\": \"Use buildseopayloadasync from seoslug.asyncbuilder in your\
  \ route handlers. It runs the synchronous builder in a thread pool so it does not\
  \ block the event loop.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# FastAPI integration

Use `build_seo_payload_async` from `seoslug.async_builder` in your route handlers. It runs the synchronous builder in a thread pool so it does not block the event loop.

## Basic route handler

```python
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from seoslug import SEOConfig, URLPolicy, SEOEntity
from seoslug.async_builder import build_seo_payload_async

app = FastAPI()

def get_seo_config():
    return SEOConfig(
        canonical_host="blog.example.com",
        public_base_url="https://blog.example.com",
        url_policy=URLPolicy(),
    )

@app.get("/posts/{slug}", response_class=HTMLResponse)
async def get_post(slug: str, config: SEOConfig = Depends(get_seo_config)):
    entity = SEOEntity(
        entity_type="post",
        title="My Post",
        excerpt="A short description",
        status="published",
    )
    payload = await build_seo_payload_async(entity, f"/posts/{slug}", config)
    return HTMLResponse(f"""
    <head>
        <title>{payload.title}</title>
        <meta name="description" content="{payload.description}">
        <link rel="canonical" href="{payload.canonical}">
    </head>
    """)
```

## Dependency injection pattern

Use FastAPI's `Depends` to provide `SEOConfig`. This keeps configuration centralised and testable.

```python
from functools import lru_cache
from seoslug import SEOConfig, URLPolicy

@lru_cache
def get_seo_config():
    return SEOConfig(
        canonical_host="blog.example.com",
        public_base_url="https://blog.example.com",
        url_policy=URLPolicy(allowed_query_params=["page"]),
        site_name="My Blog",
        locale="en_US",
    )
```

Inject the config into any route that needs SEO metadata.

## ETag caching

seoslug is deterministic. Same input always produces the same `SEOPayload`. Use this for ETag-based HTTP caching.

```python
import hashlib
from fastapi import Request, Response

@app.get("/posts/{slug}")
async def get_post_cached(
    request: Request,
    slug: str,
    config: SEOConfig = Depends(get_seo_config),
):
    entity = SEOEntity(entity_type="post", title="My Post", status="published")
    payload = await build_seo_payload_async(entity, f"/posts/{slug}", config)
    etag = hashlib.sha256(str(payload.to_dict()).encode()).hexdigest()[:16]

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    return Response(
        content=render_template(payload),
        headers={"ETag": etag},
    )
```

## Template rendering with Jinja2

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/posts/{slug}")
async def get_post(
    request: Request,
    slug: str,
    config: SEOConfig = Depends(get_seo_config),
):
    entity = SEOEntity(entity_type="post", title="My Post", status="published")
    payload = await build_seo_payload_async(entity, f"/posts/{slug}", config)
    return templates.TemplateResponse("post.html", {
        "request": request,
        "payload": payload.to_dict(),
    })
```

The `SEOPayload` dataclass is dict-compatible. You can pass it directly or use `.to_dict()` for explicit serialization.

## Customising the thread pool

```python
from concurrent.futures import ThreadPoolExecutor
from seoslug.async_builder import set_executor

executor = ThreadPoolExecutor(max_workers=8)
set_executor(executor)
```

Call `set_executor(None)` to reset to the default 4-worker pool.
