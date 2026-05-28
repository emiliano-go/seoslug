# Core concepts

seoslug is built on three core principles.

## Determinism

Identical inputs always produce identical outputs.
This enables snapshot testing and aggressive caching.
You can commit expected output to Git and validate it in CI.

```python
payload1 = build_seo_payload(entity, path, config)
payload2 = build_seo_payload(entity, path, config)
assert payload1 == payload2  # always True
```

The same URL always generates an identical payload.
You can cache forever without invalidation logic.
Diff staging against production to reveal configuration drift.

## Single responsibility

seoslug generates SEO metadata and does nothing else.
It does not rewrite your content.
It does not make HTTP requests.
It does not store state.

## Pure functions

The library uses no environment variables.
It uses no system clock.
It uses no random numbers.
It uses no external API calls.

What you see in the config is what you get in the output.

## How it works

seoslug takes three inputs: a configuration, an entity, and a route path.

The configuration defines your site wide SEO rules.
The entity represents a single piece of content.
The route path is the URL path for that content.

The output is a dictionary with seven keys: title, description, canonical, robots, og, twitter, and schema_jsonld.

Each key is resolved through a fallback chain.
If a value is missing from the entity, seoslug tries the next source in the chain.
If the chain is exhausted, seoslug uses a sensible default.

## Next steps

Read [Configuration Overview](configuration/index.md) to learn about all configuration options.
Read [URL Normalization](url-normalization.md) to understand how URLs are cleaned.
