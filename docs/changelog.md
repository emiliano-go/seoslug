# Changelog

All notable changes to seoslug are documented here.
The format is based on Keep a Changelog.
The project follows semantic versioning.

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
