---
seo:
  title: Django integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/django/
  robots: index,follow
  og:
    type: website
    title: Django integration - seoslug
    description: Call buildseopayload in your view and pass the result as template
      context. Use buildseopayloaddict when you need a plain dict Django REST Framework,
      JSON...
    url: https://seoslug.emiliano-go.com/integrations/django/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Django integration - seoslug
    description: Call buildseopayload in your view and pass the result as template
      context. Use buildseopayloaddict when you need a plain dict Django REST Framework,
      JSON...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Call buildseopayload in your view and pass the result as template context.
    Use buildseopayloaddict when you need a plain dict Django REST Framework, JSON...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Django integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/django/
    description: Call buildseopayload in your view and pass the result as template
      context. Use buildseopayloaddict when you need a plain dict Django REST Framework,
      JSON...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Django integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Call buildseopayload in your view and pass the result as template context.\
  \ Use buildseopayloaddict when you need a plain dict Django REST Framework, JSON...\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/django/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Django integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Call buildseopayload in your view\
  \ and pass the result as template context. Use buildseopayloaddict when you need\
  \ a plain dict Django REST Framework, JSON...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/django/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"\
  og:image:width\" content=\"225\">\n<meta property=\"og:image:height\" content=\"\
  225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"\
  og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Django integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Call buildseopayload in your view and pass\
  \ the result as template context. Use buildseopayloaddict when you need a plain\
  \ dict Django REST Framework, JSON...\">\n<meta name=\"twitter:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Django integration\
  \ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/django/\"\
  ,\n  \"description\": \"Call buildseopayload in your view and pass the result as\
  \ template context. Use buildseopayloaddict when you need a plain dict Django REST\
  \ Framework, JSON...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Django integration

Call `build_seo_payload` in your view and pass the result as template context. Use `build_seo_payload_dict` when you need a plain dict (Django REST Framework, JSON responses).

## Function-based view

```python
from django.shortcuts import render
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

def post_detail(request, slug):
    config = SEOConfig(
        canonical_host="blog.example.com",
        public_base_url="https://blog.example.com",
        url_policy=URLPolicy(),
    )
    entity = SEOEntity(
        entity_type="post",
        title="My Post",
        excerpt="A short description",
        status="published",
    )
    payload = build_seo_payload(entity, f"/posts/{slug}", config)
    return render(request, "post.html", {"payload": payload})
```

## Class-based view

```python
from django.views.generic import DetailView
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

class PostDetailView(DetailView):
    template_name = "post.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        config = SEOConfig(
            canonical_host="blog.example.com",
            public_base_url="https://blog.example.com",
            url_policy=URLPolicy(),
        )
        entity = SEOEntity(
            entity_type="post",
            title=self.object.title,
            excerpt=self.object.excerpt,
            status="published",
        )
        context["payload"] = build_seo_payload(entity, self.object.get_absolute_url(), config)
        return context
```

## Template context

The `SEOPayload` dataclass supports dict-style access. Use it directly in Django templates.

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

    <script type="application/ld+json">{{ payload.schema_jsonld|safe }}</script>
</head>
```

You can also call `payload.to_dict()` and pass the result as context. Both approaches work.

## Django REST Framework

For DRF views, use `build_seo_payload_dict` to get a plain dict suitable for JSON serialization.

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload_dict

@api_view(["GET"])
def post_detail_api(request, slug):
    config = SEOConfig(
        canonical_host="blog.example.com",
        public_base_url="https://blog.example.com",
        url_policy=URLPolicy(),
    )
    entity = SEOEntity(
        entity_type="post",
        title="My Post",
        excerpt="A short description",
        status="published",
    )
    payload = build_seo_payload_dict(entity, f"/posts/{slug}", config)
    return Response({"seo": payload})
```

## Framework caching

Use Django's `@cache_page` decorator with a key prefix derived from the route.

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 60, key_prefix="seo")
def post_detail(request, slug):
    ...
```

For per-URL cache keys, use `make_key`:

```python
from django.views.decorators.cache import cache_page

def make_seo_key(group, request):
    return f"seo:{request.path}"

@cache_page(60 * 60, key_prefix="seo", make_key=make_seo_key)
def post_detail(request, slug):
    ...
```

## Settings module

Define your `SEOConfig` in `settings.py` for reuse across all views.

```python
# settings.py
from seoslug import SEOConfig, URLPolicy

SEO_CONFIG = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(allowed_query_params=["page"]),
    site_name="My Blog",
    default_og_image="https://blog.example.com/default.jpg",
)
```

```python
# views.py
from django.conf import settings
from seoslug import SEOEntity, build_seo_payload

def post_detail(request, slug):
    entity = SEOEntity(entity_type="post", title="My Post", status="published")
    payload = build_seo_payload(entity, f"/posts/{slug}", settings.SEO_CONFIG)
    return render(request, "post.html", {"payload": payload})
```
