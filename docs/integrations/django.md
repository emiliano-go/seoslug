# Django integration

In Django, call `build_seo_payload` in your view.
Pass the payload to your template through the context.

## View example

```python
from django.shortcuts import render
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)

def post_detail(request, slug):
    entity = SEOEntity(
        entity_type="post",
        title="My Post",
        excerpt="A short description",
        status="published",
    )
    payload = build_seo_payload(entity, f"/posts/{slug}", config)
    return render(request, "post.html", {"payload": payload})
```

## Template example

```html
<head>
    <title>{{ payload.title }}</title>
    <meta name="description" content="{{ payload.description }}">
    <link rel="canonical" href="{{ payload.canonical }}">
    <meta name="robots" content="{{ payload.robots }}">

    <meta property="og:title" content="{{ payload.og.title }}">
    <meta property="og:description" content="{{ payload.og.description }}">
    <meta property="og:url" content="{{ payload.og.url }}">
    <meta property="og:image" content="{{ payload.og.image }}">

    <meta name="twitter:card" content="{{ payload.twitter.card }}">
    <meta name="twitter:title" content="{{ payload.twitter.title }}">
    <meta name="twitter:description" content="{{ payload.twitter.description }}">
    <meta name="twitter:image" content="{{ payload.twitter.image }}">

    <script type="application/ld+json">
    {{ payload.schema_jsonld|jsonify }}
    </script>
</head>
```

## Caching

seoslug works with Django's caching framework.

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 60)
def post_detail(request, slug):
    # View code here
```

For more precise caching, use the payload hash as a cache key.

```python
import hashlib
from django.core.cache import cache

def post_detail(request, slug):
    cache_key = f"seo:{slug}"
    payload = cache.get(cache_key)

    if payload is None:
        entity = SEOEntity(entity_type="post", title="My Post")
        payload = build_seo_payload(entity, f"/posts/{slug}", config)
        cache.set(cache_key, payload, 60 * 60)

    return render(request, "post.html", {"payload": payload})
```
