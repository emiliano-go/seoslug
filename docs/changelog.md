# Changelog

All notable changes to seoslug are documented here.
The format is based on Keep a Changelog.
The project follows semantic versioning.

## 1.1.0 (2026-06-17)

### Added

- Plugin/hook system for payload post-processing via `hook`, `register_hook`, `clear_hooks`, `get_registered_hooks`, and `run_hooks`.
- Custom exception hierarchy: `SEOError`, `SEOConfigError`, `SEOEntityError`, `URLPolicyError`, `SEOPayloadError`.
- `author_name` field on `SEOEntity` for JSON-LD author injection.
- `omit_schema` field on `SEOOverrides` for per-call schema suppression.
- `publisher_name` and `publisher_logo` fields on `SEOConfig` for JSON-LD publisher injection.

### Changed

- `build_seo_payload` now runs `post_process` hooks before returning.
- HTML body description extraction is now lazy — only parsed when no higher-precedence source is available.

## 1.0.2 (2026-06-??)

### Changed

- Minor internal improvements and documentation updates.

## 1.0.1 (2026-05-28)

### Changed

- Replaced inline tracking parameter logic with the detrack library.
- Tracking coverage expanded from 3 patterns to 60+ patterns.
Added detrack as a dependency.

## 1.0.0 (2026-04-15)

### Added

- First stable release.
- SEOConfig, URLPolicy, SEOEntity, SEOOverrides dataclasses.
- build_seo_payload function for complete SEO payload generation.
- normalize_public_url and normalize_path for URL normalization.
- Automatic JSON-LD schema generation.
- Open Graph and Twitter Card generation.
- Deterministic, pure function design.
