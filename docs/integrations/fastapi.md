# FastAPI integration

In FastAPI, you can use seoslug inside your route handlers.
Create a dependency that loads your SEO config and entity.
Call `build_seo_payload` before rendering your template.

## Basic example

```python
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

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
    payload = build_seo_payload(entity, f"/posts/{slug}", config)
    # Render template with payload
    return HTMLResponse(f"""
    <head>
        <title>{payload['title']}</title>
        <meta name="description" content="{payload['description']}">
        <link rel="canonical" href="{payload['canonical']}">
    </head>
    """)
```

## Caching with ETags

Use seoslug's deterministic output for ETag based caching.
Compare the hash of the payload against the If-None-Match header.

```python
import hashlib
from fastapi import Request, Response

@app.get("/posts/{slug}")
async def get_post_cached(request: Request, slug: str, config=Depends(get_seo_config)):
    entity = SEOEntity(entity_type="post", title="My Post")
    payload = build_seo_payload(entity, f"/posts/{slug}", config)
    etag = hashlib.sha256(str(payload).encode()).hexdigest()[:16]

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    return Response(
        content=render_template(payload),
        headers={"ETag": etag},
    )
```

## Jinja templates

Use Jinja2Templates for full HTML rendering.

```python
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@app.get("/posts/{slug}")
async def get_post(request: Request, slug: str, config=Depends(get_seo_config)):
    entity = SEOEntity(entity_type="post", title="My Post")
    payload = build_seo_payload(entity, f"/posts/{slug}", config)
    return templates.TemplateResponse("post.html", {
        "request": request,
        "payload": payload,
    })
```
