# seoslug - Step-by-Step Implementation Plan

This plan translates `spec.md` into an execution checklist for building and shipping the `seoslug` package.

## 1) Confirm package identity and naming

1. Set distribution/package name to `seoslug` everywhere.
2. Use import path `from seoslug import ...` in docs/tests/examples.
3. Align repository docs and metadata to remove old `zenith-seo-core` naming.

## 2) Scaffold project structure

1. Create `pyproject.toml` with modern Python packaging metadata.
2. Create source layout under `src/seoslug/`.
3. Add module files:
   - `__init__.py`
   - `config.py`
   - `schemas.py`
   - `normalization.py`
   - `builder.py`
   - `jsonld.py`
   - `text.py`
4. Add tests directory and files:
   - `tests/test_normalization.py`
   - `tests/test_builder.py`
   - `tests/test_fallbacks.py`
   - `tests/test_robots_rules.py`

## 3) Define public API contract (v1)

1. Export the following symbols from `seoslug.__init__`:
   - `SEOConfig`
   - `URLPolicy`
   - `SEOEntity`
   - `SEOOverrides`
   - `normalize_public_url`
   - `normalize_path`
   - `build_seo_payload`
2. Keep public signatures exactly as specified in `spec.md`.
3. Treat this API as stable for `v1.0.0`.

## 4) Implement configuration and validation models

1. Implement `URLPolicy` defaults:
   - `enforce_https=True`
   - `lowercase_paths=True`
   - `trailing_slash="never"`
   - `collapse_duplicate_slashes=True`
   - `strip_tracking_params=True`
   - `allowed_query_params=[]`
2. Implement `SEOConfig` fields and defaults, including robots defaults.
3. Validate required config values at init/model creation.
4. Raise `ValueError` for invalid config.

## 5) Implement input models

1. Implement `SEOEntity` with required enum-like `entity_type` options:
   - `home`, `post`, `page`, `video`, `taxonomy`, `search`, `other`
2. Implement optional content/status/date/media fields.
3. Implement `SEOOverrides` with all override fields (meta, canonical, robots, OG, Twitter, schema).
4. Ensure missing optional fields never crash payload building.

## 6) Build URL normalization engine

1. Implement `normalize_path(path, policy)`:
   - collapse duplicate slashes (policy-driven)
   - lowercase paths (policy-driven)
   - apply trailing slash behavior (`always`/`never`/`preserve`)
2. Implement `normalize_public_url(url_or_path, config)`:
   - accept absolute URL or relative path
   - force configured canonical host
   - enforce HTTPS when enabled
   - normalize path via `normalize_path`
   - strip tracking params (`utm_*`, `gclid`, `fbclid`) when enabled
   - if allowlist exists, keep only allowed query params
   - return absolute URL
3. Implement best-effort malformed URL handling; raise `ValueError` if impossible.
4. Verify idempotency behavior:
   - `normalize_public_url(normalize_public_url(x), config) == normalize_public_url(x, config)`

## 7) Implement text extraction utilities

1. Add safe HTML-to-text extraction in `text.py`.
2. Strip tags without executing HTML.
3. Normalize whitespace and trim output.
4. Provide snippet helper for description fallback from `body_html`.

## 8) Implement SEO payload builder

1. Implement `build_seo_payload(entity, route_path, config, overrides=None)`.
2. Return contract:
   - `title`, `description`, `canonical`, `robots`
   - `og` object (`type`, `title`, `description`, `url`, `image`)
   - `twitter` object (`card`, `title`, `description`, `image`)
   - `schema_jsonld`
3. Apply mandatory fallback hierarchies exactly:
   - title: override -> entity title -> fallback
   - description: override -> excerpt -> HTML snippet
   - canonical: override -> normalized route
   - robots: override -> entity/status/search logic -> config defaults
   - OG image: override -> featured image -> config default image
   - Twitter: overrides -> OG/title/description/image -> default card
4. Map OG type by entity type (for example, article-like for posts/pages/videos as needed by implementation policy).
5. Keep output deterministic and stable.

## 9) Implement schema handling

1. In `jsonld.py`, pass through `schema_jsonld` when provided in overrides.
2. Support both dict and list[dict].
3. Default to empty object/list convention chosen by implementation and keep it consistent in tests.

## 10) Write tests for normalization rules

1. Cover host enforcement.
2. Cover protocol enforcement.
3. Cover trailing slash modes.
4. Cover duplicate slash cleanup.
5. Cover query tracking param stripping.
6. Cover allowlist filtering.
7. Cover lowercase transformation.
8. Cover idempotency.

## 11) Write tests for payload and fallback hierarchy

1. Test each branch in title fallback chain.
2. Test each branch in description fallback chain.
3. Test canonical override vs computed canonical.
4. Test robots logic by entity type/status (`published`, non-published, `search`).
5. Test OG/Twitter precedence and inheritance rules.
6. Test schema passthrough behavior.

## 12) Add regression fixtures/snapshots

1. Create representative entity fixtures:
   - `home`, `post`, `page`, `video`, `taxonomy`, `search`
2. Generate expected payload snapshots for each fixture.
3. Ensure outputs remain byte-stable for deterministic serialization use.

## 13) Documentation and usage examples

1. Write README quickstart with copy-paste example.
2. Document model fields and function signatures.
3. Add cookbook examples:
   - content API item
   - static page
   - search page
4. Include migration guidance for teams replacing legacy SEO logic.

## 14) Performance and quality checks

1. Run test suite in CI and local.
2. Add lightweight benchmarks/checks for target performance:
   - URL normalization sub-millisecond average
   - payload build sub-2ms average
3. Confirm no network/DB calls in core logic.

## 15) Release readiness (v1.0.0)

1. Confirm section 5 API is fully implemented.
2. Confirm section 13 test coverage expectations are met.
3. Verify package builds and installs via `pip`.
4. Tag/release under SemVer as `1.0.0` when all criteria pass.

## 16) Definition of Done checklist

- Public API implemented and exported.
- All fallback and normalization rules implemented.
- Tests pass in CI.
- README examples work as written.
- Package build/install succeeds.
- Project naming is consistently `seoslug`.
