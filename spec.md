# zenith-seo-core - Full Specification

## 1) Package Identity

- **Proposed name:** `zenith-seo-core`
- **Purpose:** Framework-agnostic Python library for canonical URL normalization and deterministic SEO payload generation.
- **Scope:** Pure business logic; no DB/session/framework dependencies.

## 2) Goals

1. Provide one stable engine for URL canonicalization.
2. Provide one stable engine for SEO payload generation with strict fallback hierarchy.
3. Make behavior deterministic, testable, and portable across services.
4. Keep integration lightweight for FastAPI, Django, Flask, or offline ETL tools.

## 3) Non-goals

- No HTTP server/router built in.
- No ORM models/migrations.
- No direct Redis/cache implementation.
- No crawler/ranking analytics.

## 4) Target Users

- Backend teams exposing SEO-ready content APIs.
- Migration teams moving from legacy CMS to headless/API-driven frontend.
- Platform teams standardizing canonical and metadata behavior across apps.

## 5) Public API (v1)

```python
from zenith_seo_core import (
    SEOConfig,
    URLPolicy,
    SEOEntity,
    SEOOverrides,
    normalize_public_url,
    normalize_path,
    build_seo_payload,
)
```

### 5.1 Config Models

- `URLPolicy`
  - `enforce_https: bool = True`
  - `lowercase_paths: bool = True`
  - `trailing_slash: Literal["always", "never", "preserve"] = "never"`
  - `collapse_duplicate_slashes: bool = True`
  - `strip_tracking_params: bool = True`
  - `allowed_query_params: list[str] = []`

- `SEOConfig`
  - `canonical_host: str`
  - `public_base_url: str`
  - `url_policy: URLPolicy`
  - `default_robots: str = "index,follow"`
  - `default_og_image: str | None = None`
  - `site_name: str | None = None`
  - `title_template: str | None = "{title}"`
  - `search_robots: str = "noindex,follow"`

### 5.2 Input Models

- `SEOEntity`
  - `entity_type: Literal["home", "post", "page", "video", "taxonomy", "search", "other"]`
  - `slug: str | None`
  - `title: str | None`
  - `excerpt: str | None`
  - `body_html: str | None`
  - `status: str | None` (`published`, `draft`, etc.)
  - `featured_image: str | None`
  - `published_at: str | None`
  - `updated_at: str | None`

- `SEOOverrides`
  - `meta_title: str | None`
  - `meta_description: str | None`
  - `canonical_url: str | None`
  - `robots: str | None`
  - `og_title: str | None`
  - `og_description: str | None`
  - `og_image: str | None`
  - `twitter_card: str | None`
  - `twitter_title: str | None`
  - `twitter_description: str | None`
  - `twitter_image: str | None`
  - `schema_jsonld: dict | list[dict] | None`

### 5.3 Functions

- `normalize_path(path: str, policy: URLPolicy) -> str`
- `normalize_public_url(url_or_path: str, config: SEOConfig) -> str`
- `build_seo_payload(entity: SEOEntity, route_path: str, config: SEOConfig, overrides: SEOOverrides | None = None) -> dict`

## 6) Output Contract

`build_seo_payload(...)` returns:

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

## 7) Fallback Hierarchy (Mandatory)

### Title
1. `overrides.meta_title`
2. `entity.title`
3. `"Untitled"` (or caller template fallback)

### Description
1. `overrides.meta_description`
2. `entity.excerpt`
3. Plain-text snippet extracted from `entity.body_html` (trimmed)

### Canonical
1. `overrides.canonical_url`
2. `normalize_public_url(route_path, config)`

### Robots
1. `overrides.robots`
2. entity-derived default:
   - `published` content: `index,follow`
   - non-published/search pages: config-driven (`search_robots` for search)
   - otherwise: `config.default_robots`

### OG Image
1. `overrides.og_image`
2. `entity.featured_image`
3. `config.default_og_image`

### Twitter
1. override fields
2. OG/title/description/image fallbacks
3. default card: `summary_large_image`

## 8) URL Normalization Rules

1. Accept absolute URL or relative path as input.
2. Enforce configured host.
3. Enforce HTTPS when `enforce_https=True`.
4. Collapse duplicate slashes in path.
5. Lowercase path when enabled.
6. Apply trailing-slash policy.
7. Strip tracking params (`utm_*`, `gclid`, `fbclid`) when enabled.
8. Keep only `allowed_query_params` if allowlist present.
9. Return absolute URL.

## 9) Error Handling

- Invalid config -> raise `ValueError` at model validation/init.
- Malformed URL input -> normalize best-effort; if impossible, raise `ValueError`.
- Missing optional fields -> never crash; fallback logic must complete.

## 10) Performance Targets

- URL normalization: sub-millisecond average in local benchmarks.
- SEO payload build: sub-2ms average for typical entities.
- No network/DB calls in core library.

## 11) Determinism and Idempotency

- Same inputs must produce byte-equivalent outputs (ordering stable for dict serialization when caller uses deterministic serializer).
- Normalization should be idempotent:
  - `normalize_public_url(normalize_public_url(x)) == normalize_public_url(x)`

## 12) Package Structure

```text
zenith-seo-core/
  pyproject.toml
  README.md
  spec.md
  src/
    zenith_seo_core/
      __init__.py
      config.py
      schemas.py
      normalization.py
      builder.py
      jsonld.py
      text.py
  tests/
    test_normalization.py
    test_builder.py
    test_fallbacks.py
    test_robots_rules.py
```

## 13) Testing Specification

### 13.1 URL tests
- host enforcement
- protocol enforcement
- trailing slash modes
- duplicate slash cleanup
- query param stripping/allowlist
- lowercase transformation
- idempotency

### 13.2 Payload tests
- each fallback branch for title/description/canonical/og/twitter
- robots logic by entity type/status
- OG/Twitter values match expected precedence
- schema passthrough when provided

### 13.3 Regression tests
- fixtures for representative content types (home/post/page/video/taxonomy/search)
- snapshot tests for stable output contract

## 14) Versioning

- SemVer (`MAJOR.MINOR.PATCH`)
- v1.0.0 requirements:
  - stable public API listed in section 5
  - complete tests from section 13
  - documented migration notes for future changes

## 15) Integration Pattern (FastAPI Example)

```python
from zenith_seo_core import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="portal.example.com",
    public_base_url="https://portal.example.com",
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
        collapse_duplicate_slashes=True,
        strip_tracking_params=True,
        allowed_query_params=["page", "q"],
    ),
)

entity = SEOEntity(
    entity_type="post",
    slug="my-post",
    title="My Post",
    excerpt="Example excerpt",
    body_html="<p>Body</p>",
    status="published",
    featured_image="https://cdn.example.com/post.jpg",
)

seo = build_seo_payload(entity, "/posts/my-post", config)
```

## 16) Security and Safety Notes

- Do not execute or trust HTML; strip tags for description snippets.
- Avoid reflecting raw query params into canonical unless allowlisted.
- Ensure generated URLs are absolute and same-host per policy.

## 17) Documentation Requirements

- README quickstart
- API reference for models/functions
- cookbook examples (content API, static page, search page)
- migration guide for adopting existing custom logic

## 18) Definition of Done

`zenith-seo-core` is complete when:

1. Public API in section 5 is implemented.
2. All fallback and normalization rules are implemented.
3. Tests in section 13 pass in CI.
4. README includes working copy-paste examples.
5. Package is buildable and installable via `pip`.
