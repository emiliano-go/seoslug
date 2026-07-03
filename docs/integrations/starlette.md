---
seo:
  title: Starlette integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/starlette/
  robots: index,follow
  og:
    type: website
    title: Starlette integration - seoslug
    description: Starlette is an async Python framework. Use buildseopayloadasync
      from seoslug.asyncbuilder in your endpoints. It runs the synchronous builder
      in a thread pool...
    url: https://seoslug.emiliano-go.com/integrations/starlette/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Starlette integration - seoslug
    description: Starlette is an async Python framework. Use buildseopayloadasync
      from seoslug.asyncbuilder in your endpoints. It runs the synchronous builder
      in a thread pool...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Starlette is an async Python framework. Use buildseopayloadasync from
    seoslug.asyncbuilder in your endpoints. It runs the synchronous builder in a thread
    pool...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Starlette integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/starlette/
    description: Starlette is an async Python framework. Use buildseopayloadasync
      from seoslug.asyncbuilder in your endpoints. It runs the synchronous builder
      in a thread pool...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Starlette integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Starlette is an async Python framework. Use buildseopayloadasync from\
  \ seoslug.asyncbuilder in your endpoints. It runs the synchronous builder in a thread\
  \ pool...\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/starlette/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Starlette integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Starlette is an async Python framework.\
  \ Use buildseopayloadasync from seoslug.asyncbuilder in your endpoints. It runs\
  \ the synchronous builder in a thread pool...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/starlette/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"\
  og:image:width\" content=\"225\">\n<meta property=\"og:image:height\" content=\"\
  225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"\
  og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Starlette integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Starlette is an async Python framework.\
  \ Use buildseopayloadasync from seoslug.asyncbuilder in your endpoints. It runs\
  \ the synchronous builder in a thread pool...\">\n<meta name=\"twitter:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Starlette integration\
  \ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/starlette/\"\
  ,\n  \"description\": \"Starlette is an async Python framework. Use buildseopayloadasync\
  \ from seoslug.asyncbuilder in your endpoints. It runs the synchronous builder in\
  \ a thread pool...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Starlette integration

Starlette is an async Python framework. Use `build_seo_payload_async` from `seoslug.async_builder` in your endpoints. It runs the synchronous builder in a thread pool so it does not block the event loop.

## Basic route

```python
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from seoslug import SEOConfig, URLPolicy, SEOEntity
from seoslug.async_builder import build_seo_payload_async

SEO_CONFIG = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)


async def home(request):
    entity = SEOEntity(
        entity_type="home",
        title="My Blog",
        excerpt="A blog about things.",
        status="published",
    )
    payload = await build_seo_payload_async(entity, "/", SEO_CONFIG)
    html = render_jinja_template("home.html", seo=payload)

    return HTMLResponse(html)
```

## Route with path parameters

Starlette passes path parameters via `request.path_params`:

```python
from starlette.responses import HTMLResponse
from seoslug import SEOConfig, URLPolicy, SEOEntity, Breadcrumb
from seoslug.async_builder import build_seo_payload_async


async def post_detail(request):
    slug = request.path_params["slug"]
    post = get_post_by_slug(slug)
    if post is None:
        from starlette.responses import PlainTextResponse
        return PlainTextResponse("Not found", status_code=404)

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
        published_at=post.published_at.isoformat(),
        updated_at=post.updated_at.isoformat() if post.updated_at else None,
        author_name=post.author,
        featured_image=post.cover_url,
        breadcrumbs=[
            Breadcrumb(name="Blog", url="/"),
            Breadcrumb(name=post.title, url=f"/{slug}/"),
        ],
    )
    payload = await build_seo_payload_async(entity, f"/{slug}/", SEO_CONFIG)
    html = render_jinja_template("post.html", post=post, seo=payload)

    return HTMLResponse(html)
```

## App setup with routes

Wire everything together with Starlette's `Route` list:

```python
from starlette.applications import Starlette
from starlette.routing import Route


routes = [
    Route("/", home),
    Route("/{slug}", post_detail),
]

app = Starlette(routes=routes)
```

## Template rendering

Use any async-compatible template engine. Starlette ships with Jinja2 support via `Jinja2Templates`:

```python
from starlette.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")


async def post_detail(request):
    slug = request.path_params["slug"]
    post = get_post_by_slug(slug)

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
    )
    payload = await build_seo_payload_async(entity, f"/{slug}/", SEO_CONFIG)

    return templates.TemplateResponse("post.html", {
        "request": request,
        "seo": payload,
        "post": post,
    })
```

In your Jinja2 template, render the full SEO block or individual parts:

```jinja
<head>
  {{ seo.render_html()|safe }}
</head>
```

Or compose the tags manually:

```jinja
<head>
  <title>{{ seo.title }}</title>
  <meta name="description" content="{{ seo.description }}">
  <link rel="canonical" href="{{ seo.canonical }}">
  <meta name="robots" content="{{ seo.robots }}">
  {{ seo.render_opengraph()|safe }}
  {{ seo.render_twitter()|safe }}
  {{ seo.render_jsonld()|safe }}
</head>
```

## JSON API

For JSON endpoints, use `build_seo_payload_async` and call `.to_dict()` on the result, or use the synchronous `build_seo_payload_dict`:

```python
from starlette.responses import JSONResponse
from seoslug import SEOEntity
from seoslug.async_builder import build_seo_payload_async


async def seo_json(request):
    slug = request.path_params["slug"]
    post = get_post_by_slug(slug)
    if post is None:
        return JSONResponse({"error": "not found"}, status_code=404)

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
    )
    payload = await build_seo_payload_async(entity, f"/{slug}/", SEO_CONFIG)

    return JSONResponse(payload.to_dict())
```

## Middleware pattern

For apps where every page needs SEO metadata, use middleware to attach the SEO payload to the request state:

```python
from starlette.middleware.base import BaseHTTPMiddleware
from seoslug.async_builder import build_seo_payload_async


class SEOMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        route = request.url.path
        entity = SEOEntity(
            entity_type="page",
            title=derive_title_from_route(route),
            excerpt="",
            status="published",
        )
        request.state.seo = await build_seo_payload_async(
            entity, route, SEO_CONFIG
        )
        return await call_next(request)
```

## ETag caching

Use seoslug's `etag()` for conditional responses:

```python
from starlette.responses import Response


async def post_detail(request):
    slug = request.path_params["slug"]
    post = get_post_by_slug(slug)

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
    )
    payload = await build_seo_payload_async(entity, f"/{slug}/", SEO_CONFIG)
    etag = payload.etag()

    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304)

    html = render_jinja_template("post.html", post=post, seo=payload)
    return Response(html, media_type="text/html", headers={"ETag": etag})
```

## Customising the thread pool

```python
from concurrent.futures import ThreadPoolExecutor
from seoslug.async_builder import set_executor

executor = ThreadPoolExecutor(max_workers=8)
set_executor(executor)
```

Call `set_executor(None)` to reset to the default 4-worker pool.
