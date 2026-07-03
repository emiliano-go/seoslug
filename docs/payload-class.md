# SEOPayload Dataclass

`build_seo_payload()` returns a `SEOPayload` dataclass instance.
It supports both attribute access and dict-style access.

Use attribute access for type safety in Python code.
Use dict access for template engines and JSON serialization.

## Attribute access vs dict access

Both forms work on the same data:

```python
payload = build_seo_payload(entity, route, config)

# Attribute access
payload.title          # "My Post"
payload.canonical      # "https://example.com/post"
payload.og.title       # "My Post"
payload.twitter.card   # "summary_large_image"

# Dict access
payload["title"]       # "My Post"
payload["canonical"]   # "https://example.com/post"
payload["og"]["title"] # "My Post"
```

## to_dict() method

Convert the payload to a plain dict. Nested OGPayload and TwitterPayload are also converted.

```python
d = payload.to_dict()
# Returns: {"title": "...", "description": "...", "canonical": "...", ...}
```

`build_seo_payload_dict()` is a convenience wrapper that calls `to_dict()` internally:

```python
from seoslug import build_seo_payload_dict

d = build_seo_payload_dict(entity, route, config)
# Same as: build_seo_payload(entity, route, config).to_dict()
```

## Nested dataclasses

### OGPayload

Fields: `type`, `title`, `description`, `url`, `image`, `image_width`, `image_height`, `image_alt`, `site_name`, `locale`, `locale_alternate`, `audio`, `video`.

```python
payload.og.title          # attribute
payload.og.image_width    # attribute
payload.og["image:width"] # colon-key access
```

### TwitterPayload

Fields: `card`, `title`, `description`, `image`, `image_alt`, `site`, `creator`.

```python
payload.twitter.card        # attribute
payload.twitter.image_alt   # attribute
payload.twitter["image:alt"]# colon-key access
```

## Colon-key access for og and twitter

Some Open Graph and Twitter keys use colons in their names (`image:width`, `image:height`, `image:alt`, `locale:alternate`).

These are accessible as Python attributes with underscores or as dict keys with colons:

```python
# OG
payload.og.image_width         # 1200 (attribute)
payload.og["image:width"]      # 1200 (colon dict key)
"image:width" in payload.og    # True

payload.og.locale_alternate    # ["es_ES"] (attribute)
payload.og["locale:alternate"] # ["es_ES"] (colon dict key)

# Twitter
payload.twitter.image_alt      # "Hero" (attribute)
payload.twitter["image:alt"]   # "Hero" (colon dict key)
```

The `to_dict()` method outputs colon keys:

```python
d = payload.og.to_dict()
d["image:width"]       # 1200
d["locale:alternate"]  # ["es_ES"]
```

## Equality comparison with dicts

`SEOPayload`, `OGPayload`, and `TwitterPayload` support direct equality comparison with dicts:

```python
payload = build_seo_payload(entity, route, config)

expected = {
    "title": "My Post",
    "canonical": "https://example.com/post",
    "robots": "index,follow",
    "og": {"type": "article", "title": "My Post", ...},
    "twitter": {"card": "summary_large_image", ...},
}

assert payload == expected  # True
```

This enables clean snapshot testing without calling `.to_dict()`.

## keys() method

`keys()` iterates over payload keys that have non-None values.

```python
list(payload.keys())
# ["title", "description", "canonical", "robots", "og", "twitter", "schema_jsonld"]
```

None values are excluded. Colon-mapped keys use their dict form.

```python
og = OGPayload(type="article", title="Post", description=None, ...)
list(og.keys())
# ["type", "title", "url", "image"]  (description excluded because None)
```

## render_html()

Render the full SEO `<head>` snippet in one call. Returns a string of
`<title>`, `<meta>`, `<link>`, and `<script>` tags separated by newlines.

```python
head_html = payload.render_html()
# <title>My Post</title>
# <meta name="description" content="Post description">
# <link rel="canonical" href="https://example.com/post">
# <meta name="robots" content="index,follow">
# <meta property="og:type" content="article">
# <meta property="og:title" content="My Post">
# <meta property="og:url" content="https://example.com/post">
# <meta property="og:image" content="https://example.com/img.jpg">
# <meta name="twitter:card" content="summary_large_image">
# <meta name="twitter:title" content="My Post">
# <script type="application/ld+json">
# { "@context": "https://schema.org", ... }
# </script>
```

Inject into a Jinja2 template:

```html
<head>
{{ payload.render_html()|safe }}
</head>
```

All values are HTML-escaped. JSON-LD is pretty-printed with 2-space indent.

## hash()

Deterministic SHA-256 hex digest of the serialised payload. Two calls with
identical input always return the same hash.

```python
h1 = payload.hash()
h2 = payload.hash()
assert h1 == h2  # Always
```

Use cases:
- **Caching keys**: use the hash as a cache key for the rendered HTML
- **Content-addressed storage**: store/fetch rendered head by hash
- **CI comparison**: assert the hash has not changed between commits

## etag()

HTTP ETag header value derived from `hash()`. Returns a quoted hex string:

```python
etag = payload.etag()
# '"abc123def456..."'
```

Use in FastAPI or Django responses:

```python
from fastapi.responses import HTMLResponse

head_html = payload.render_html()
return HTMLResponse(
    content=head_html,
    headers={"ETag": payload.etag()},
)
```

## build_seo_payload_dict() wrapper

```python
from seoslug import build_seo_payload_dict

d = build_seo_payload_dict(
    entity=entity,
    route_path="/posts/my-post",
    config=config,
    overrides=overrides,  # optional
)
```

Returns a plain `dict` identical to `payload.to_dict()`.
Useful for template engines that expect raw dictionaries.
