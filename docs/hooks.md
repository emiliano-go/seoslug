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
