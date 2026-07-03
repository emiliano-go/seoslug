---
seo:
  title: Hooks and plugins - seoslug
  canonical: https://seoslug.emiliano-go.com/hooks/
  robots: index,follow
  og:
    type: website
    title: Hooks and plugins - seoslug
    description: Hooks let you modify the SEO payload after buildseopayload has assembled
      it. This is useful for adding custom JSON-LD fields, transforming descriptions...
    url: https://seoslug.emiliano-go.com/hooks/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Hooks and plugins - seoslug
    description: Hooks let you modify the SEO payload after buildseopayload has assembled
      it. This is useful for adding custom JSON-LD fields, transforming descriptions...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Hooks let you modify the SEO payload after buildseopayload has assembled
    it. This is useful for adding custom JSON-LD fields, transforming descriptions...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Hooks and plugins - seoslug
    url: https://seoslug.emiliano-go.com/hooks/
    description: Hooks let you modify the SEO payload after buildseopayload has assembled
      it. This is useful for adding custom JSON-LD fields, transforming descriptions...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Hooks and plugins - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Hooks let you modify the SEO payload after buildseopayload has assembled\
  \ it. This is useful for adding custom JSON-LD fields, transforming descriptions...\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/hooks/\">\n<meta\
  \ name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Hooks and plugins - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Hooks let you modify the SEO payload\
  \ after buildseopayload has assembled it. This is useful for adding custom JSON-LD\
  \ fields, transforming descriptions...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/hooks/\">\n<meta property=\"og:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"og:image:width\"\
  \ content=\"225\">\n<meta property=\"og:image:height\" content=\"225\">\n<meta property=\"\
  og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\" content=\"en_US\"\
  >\n<meta name=\"twitter:card\" content=\"summary_large_image\">\n<meta name=\"twitter:title\"\
  \ content=\"Hooks and plugins - seoslug\">\n<meta name=\"twitter:description\" content=\"\
  Hooks let you modify the SEO payload after buildseopayload has assembled it. This\
  \ is useful for adding custom JSON-LD fields, transforming descriptions...\">\n\
  <meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Hooks and plugins - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/hooks/\"\
  ,\n  \"description\": \"Hooks let you modify the SEO payload after buildseopayload\
  \ has assembled it. This is useful for adding custom JSON-LD fields, transforming\
  \ descriptions...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Hooks and plugins

Hooks let you modify the SEO payload after `build_seo_payload` has assembled it. This is useful for adding custom JSON-LD fields, transforming descriptions per-section, injecting site-wide organization data, or any other post-processing.

## How it works

After building the payload, `build_seo_payload` calls `run_hooks("post_process", payload, entity, config)`. Each registered hook receives the payload and must return it (possibly modified). Hooks run in registration order.

## Registering a hook

### Decorator

```python
from seoslug import hook

@hook("post_process")
def add_breadcrumb(payload, entity, config):
    payload["breadcrumb"] = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [...],
    }
    return payload
```

### Programmatic

```python
from seoslug import register_hook

def add_custom_tag(payload, entity, config):
    payload["custom_tag"] = f"generated-at-{entity.slug}"
    return payload

register_hook("post_process", add_custom_tag)
```

## Hook function signature

Every hook receives three arguments and must return a dict:

```python
def my_hook(payload: dict, entity: SEOEntity, config: SEOConfig) -> dict:
    # payload is the current state (may have been modified by previous hooks)
    # entity is the original SEOEntity passed to build_seo_payload
    # config is the SEOConfig used for generation
    return payload
```

## Available hook points

| Name | When it runs | Default registrations |
|---|---|---|
| `post_process` | End of `build_seo_payload`, before returning | None |

The `post_process` hook point is the only built-in hook point. More may be added in future versions.

## Scoped hooks (multi-config / multi-tenant)

When your application serves multiple sites or configs in the same process,
use ``HookRegistry`` to scope hooks per ``SEOConfig``:

```python
from seoslug import HookRegistry, SEOConfig

site_a = HookRegistry()
site_a.register("post_process", lambda p, e, c: {**p, "site": "A"})

site_b = HookRegistry()
site_b.register("post_process", lambda p, e, c: {**p, "site": "B"})

config_a = SEOConfig(canonical_host="a.com", ..., hooks=site_a)
config_b = SEOConfig(canonical_host="b.com", ..., hooks=site_b)
```

Global hooks (registered with ``register`` / ``@hook``) run **before** scoped
hooks.  Use global hooks for cross-cutting concerns (logging, instrumentation)
and scoped hooks for per-site customization.

``HookRegistry`` is thread-safe: writes are protected by a ``threading.Lock``.

## Execution order

1. Global hooks run in registration order (FIFO).  For decorators, file import
   order determines registration order.
2. Scoped hooks (``config.hooks``) run next, in registration order.

Within a single registry, hooks are stored and executed in registration order.
If multiple hooks modify the same field, the last one wins.

## Thread safety

The module-level ``register()`` is safe for import-time registration (the
common case).  Runtime ``register()`` calls from multiple threads are not
locked; for concurrent registration, use a ``HookRegistry`` instance
attached to ``SEOConfig``, which protects writes with ``threading.Lock``.

Reads (``run()``) iterate a list that is typically populated at import time
and never modified afterward, so read-safety is fine in practice.

## Exception behavior

If a hook raises an exception, propagation is immediate.  Remaining hooks in
the chain are **skipped**.  There is no ``try/except`` wrapping.  Hook
failures should be loud because they indicate a programming error.

```python
@hook("post_process")
def broken_hook(payload, entity, config):
    raise ValueError("something went wrong")
    # The next hook in the chain will never run.
```

## Mutation guarantees

Each hook receives a plain ``dict`` (a copy of the payload at that point).
Mutations to the dict are safe because each hook works on its own reference.

The ``entity`` and ``config`` arguments must **not** be mutated.  Changes to
these are silently ignored by the builder.

```python
@hook("post_process")
def safe_hook(payload, entity, config):
    # payload is a copy -- safe to mutate
    payload["generator"] = "seoslug"
    return payload

@hook("post_process")
def unsafe_hook(payload, entity, config):
    # entity and config must not be mutated
    # entity.title = "Hacked"     # DON'T
    # config.canonical_host = "X" # DON'T
    return payload
```

## Lifecycle

### Clear hooks

```python
from seoslug import clear_hooks

clear_hooks("post_process")   # remove only post_process hooks
clear_hooks()                  # remove all hooks
```

### Inspect registered hooks

```python
from seoslug import get_registered_hooks

hooks = get_registered_hooks()
# {'post_process': [<function add_breadcrumb at 0x...>, ...]}
```

## Best practices

- **Keep hooks pure**. Don't make HTTP requests, write files, or mutate global state inside a hook. Hooks run every time `build_seo_payload` is called.
- **Return the payload**. If your hook forgets to return the payload, later hooks and the caller will receive `None`.
- **Order matters**. Hooks run in registration order. If you have multiple hooks that modify the same field, the last one wins.
- **Use overrides first**. If a transformation applies to a specific page rather than globally, prefer `SEOOverrides` over a hook. Hooks are best for site-wide post-processing.

## Example: inject Organization schema on every page

```python
from seoslug import hook

@hook("post_process")
def inject_organization(payload, entity, config):
    existing = payload.get("schema_jsonld")
    org = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": config.publisher_name or "My Site",
        "url": config.public_base_url,
    }
    if isinstance(existing, dict):
        payload["schema_jsonld"] = [org, existing]
    elif isinstance(existing, list):
        payload["schema_jsonld"] = [org] + existing
    else:
        payload["schema_jsonld"] = org
    return payload
```

## Example: skip canonical for draft entities

```python
from seoslug import hook

@hook("post_process")
def noindex_drafts(payload, entity, config):
    if entity.status == "draft":
        payload["robots"] = "noindex,nofollow"
        payload.pop("schema_jsonld", None)
    return payload
```
