# FAQ

## Why deterministic?

Determinism enables testing, caching, and confidence.
You can snapshot test your SEO layer.
You can cache payloads without invalidation logic.
You can diff staging against production to find configuration drift.

## Can I add custom meta tags?

Not directly through seoslug.
But you can extend the payload after generation.
The returned dictionary is a plain Python dict.
Add your custom tags before passing it to your template.

```python
payload = build_seo_payload(entity, "/path", config)
payload["custom_tags"] = '<meta name="foo" content="bar">'
```

## How do I disable auto generated schema?

Set `auto_generate_schema` to False in SEOConfig.

```python
config = SEOConfig(
    auto_generate_schema=False,
)
```

Or set `omit_schema` to True in SEOOverrides for a single entity.

```python
overrides = SEOOverrides(omit_schema=True)
```

## Does seoslug work with Django?

Yes. See the [Django integration guide](integrations/django.md).

## Does seoslug work with FastAPI?

Yes. See the [FastAPI integration guide](integrations/fastapi.md).

## Does seoslug work with static site generators?

Yes. See the [SSG integration guide](integrations/ssg.md).

## Why no backlink features?

Backlink management is off page SEO.
seoslug focuses on on page SEO metadata generation.
These two concerns are separate.

## Can I use seoslug without the detrack library?

seoslug depends on detrack for tracking parameter stripping.
But you can disable tracking stripping in URLPolicy.

```python
URLPolicy(strip_tracking_params=False)
```

This keeps all query parameters unchanged.

## What Python versions are supported?

Python 3.10 and later.

## Is seoslug thread safe?

Yes. The library has no mutable shared state.
All functions are pure and stateless.

## How do I report a bug?

Open an issue on GitHub.
Include the version, input, expected output, and actual output.
