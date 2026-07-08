---
{}
---

# Validation

seoslug has three validation layers:

1. payload warnings from `validate_payload()`
2. schema-shape warnings from `validate_schema_jsonld()`
3. rendered HTML checks from `validate_html_jsonld()`

`build_seo_payload()` always runs validation, but warning emission is still gated by `SEOConfig.emit_warnings`.

## Payload warnings

```python
from seoslug.validation import validate_payload

warnings = validate_payload(payload_dict, config)
```

These cover title length, description length, canonical URLs, OG image URLs, robots format, and schema JSON-LD warnings.

## Schema validation

```python
from seoslug.validation import validate_schema_jsonld

warnings = validate_schema_jsonld(schema_jsonld)
validate_schema_jsonld(schema_jsonld, strict=True)
```

`strict=True` turns warnings into errors. Structural problems always raise `SEOEntityError`.

## HTML validation

```python
from seoslug.validation import validate_html_jsonld

warnings = validate_html_jsonld(rendered_html)
```

This checks rendered HTML for exact duplicate JSON-LD blocks.

## CLI

```bash
seoslug validate-html path/to/page.html --strict
```

Use `-` to read from stdin.
