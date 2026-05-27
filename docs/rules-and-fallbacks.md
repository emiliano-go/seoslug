# Rules and Fallbacks

## URL normalization rules

1. Accept absolute URL or relative path.
2. Enforce configured host.
3. Enforce HTTPS when enabled.
4. Collapse duplicate slashes in path.
5. Lowercase path when enabled.
6. Apply trailing slash policy.
7. Strip tracking params, `utm_*`, `gclid`, `fbclid`, when enabled.
8. Keep only `allowed_query_params` when allowlist is present.
9. Return absolute URL.

## Fallback hierarchy

- Title: `overrides.meta_title`, `entity.title`, `Untitled`.
- Description: `overrides.meta_description`, `entity.excerpt`, snippet from `entity.body_html`.
- Canonical: `overrides.canonical_url`, `normalize_public_url(route_path, config)`.
- Robots: `overrides.robots`, entity/type default.
- OG image: `overrides.og_image`, `entity.featured_image`, `config.default_og_image`.
- Twitter: override fields, then OG/title/description/image fallback, then default card `summary_large_image`.

## Payload shape

```json
{
  "title": "...",
  "description": "...",
  "canonical": "https://example.com/path",
  "robots": "index,follow",
  "og": {
    "type": "article",
    "title": "...",
    "description": "...",
    "url": "https://example.com/path",
    "image": "https://cdn.example.com/..."
  },
  "twitter": {
    "card": "summary_large_image",
    "title": "...",
    "description": "...",
    "image": "https://cdn.example.com/..."
  },
  "schema_jsonld": {}
}
```
