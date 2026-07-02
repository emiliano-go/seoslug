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
