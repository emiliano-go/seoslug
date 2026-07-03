# seoslug vs manual SEO

Manual SEO metadata is repetitive, error-prone, and hard to maintain across
a growing site. Here is exactly what seoslug removes from your to-do list.

| Task | Manual | seoslug |
|---|---|---|
| Canonical URL | Construct by hand, handle edge cases | `build_seo_payload(entity, path, config)` |
| Open Graph tags | 10+ `<meta property="og:...">` tags | `payload.og` dataclass or `payload.render_html()` |
| Twitter Cards | 6+ `<meta name="twitter:...">` tags | `payload.twitter` dataclass or `payload.render_html()` |
| JSON-LD schema | Write and maintain schema.org JSON | `payload.schema_jsonld` auto-generated |
| BreadcrumbList | Manual `BreadcrumbList` JSON-LD | `Breadcrumb(name, url)` auto-generates |
| Robots directives | `index`/`noindex`, `follow`/`nofollow` logic | `Robots` dataclass or string, applied automatically |
| URL normalization | HTTPS enforcement, trailing slash, lowercase, dedupe | `URLPolicy` handles it |
| Tracking-param stripping | Regex or detrack wiring | Built-in, configurable |
| HTML-to-text excerpt | Strip tags, decode entities, truncate | `html_to_text()` built in |
| Validation | Manual audit of title length, description length, OG image | `emit_warnings=True` in config |
| HTML rendering | Jinja2/ template tags for every meta tag | `payload.render_html()` one call |
| Content-based ETag | Manual hash of serialized output | `payload.etag()` one call |
| Testing | Snapshot tests need manual fixture setup | Deterministic by design, assert `payload == expected_dict` |
| CI verification | Manual diff of SEO output | Deterministic: commit output, diff in CI |

## What you write

**Manual approach**: template code for every tag, every route, every entity
type, plus a JSON-LD builder per schema:

```html
<title>{{ title }}</title>
<meta name="description" content="{{ description }}">
<link rel="canonical" href="{{ canonical }}">
<meta name="robots" content="{{ robots }}">
<meta property="og:title" content="{{ og_title }}">
<meta property="og:description" content="{{ og_description }}">
<meta property="og:image" content="{{ og_image }}">
<meta property="og:url" content="{{ canonical }}">
<meta property="og:type" content="{{ og_type }}">
<meta name="twitter:card" content="{{ twitter_card }}">
<meta name="twitter:title" content="{{ twitter_title }}">
<meta name="twitter:description" content="{{ twitter_description }}">
<script type="application/ld+json">{{ schema_jsonld }}</script>
```

**seoslug**: one function call:

```python
payload = build_seo_payload(entity, path, config)
head_html = payload.render_html()
```

## What you maintain

Every new entity type in the manual approach means a new template or a new
set of conditionals. Every schema.org change means updating your JSON-LD
builder. Every URL policy change means auditing every route.

seoslug centralises all of it in a single `SEOConfig` and a single
`build_seo_payload` call. Change the config, every route changes with it.

## Performance

```
10,000 payloads in 276 ms  (28 µs/payload)
```

That is 10,000 complete SEO metadata objects (canonical, OG, Twitter,
robots, JSON-LD) in the time it takes to load a single page image.

## Next steps

- [Getting started](getting-started.md): build your first payload in 5
  minutes
- [Benchmarks](https://github.com/emiliano-go/seoslug): profile on your
  own hardware
