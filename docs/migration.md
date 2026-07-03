# Migration guide: 1.x to 2.0.0

This guide covers breaking changes between seoslug 1.x and 2.0.0.

## Return type is now SEOPayload dataclass

In 1.x, `build_seo_payload` returned a plain `dict`. In 2.0.0, it returns an `SEOPayload` dataclass.

```python
# 1.x (old) - returns dict
payload = build_seo_payload(entity, "/path", config)
title = payload["title"]  # dict access

# 2.0.0 (new) - returns SEOPayload dataclass
payload = build_seo_payload(entity, "/path", config)
title = payload.title      # attribute access - RECOMMENDED
title = payload["title"]   # dict-style access - still works
```

### How to migrate

**Option A: Use attribute access.** The `SEOPayload` dataclass has typed fields. This is the recommended approach.

```python
payload = build_seo_payload(entity, "/path", config)
# Old: payload["title"], payload["description"], etc.
# New: payload.title, payload.description, payload.canonical, etc.
# New: payload.og.title, payload.og.description, payload.twitter.card, etc.
```

**Option B: Call `.to_dict()`.** Convert the payload back to a dict for backward compatibility.

```python
payload = build_seo_payload(entity, "/path", config).to_dict()
```

**Option C: Use `build_seo_payload_dict`.** New shorthand that returns a dict directly.

```python
from seoslug import build_seo_payload_dict

payload = build_seo_payload_dict(entity, "/path", config)
# payload is a plain dict - identical to 1.x behavior
```

### OGPayload and TwitterPayload are dataclasses

The `og` and `twitter` fields in `SEOPayload` are now `OGPayload` and `TwitterPayload` dataclasses. They support both attribute and dict-style access.

```python
# Old
og_image = payload["og"]["image"]

# New - attribute access
og_image = payload.og.image

# New - dict-style access (still works)
og_image = payload["og"]["image"]
```

## lxml and detrack moved to optional extras

In 1.x, lxml and detrack were required dependencies. In 2.0.0, they are
optional extras. Two extras are available:

- **`[fast]`** (recommended): lxml + detrack, same as 1.x behavior
- **`[light]`**: pure-Python fallbacks, minimal footprint

### How to migrate

Update your dependency specification:

```bash
# Old
pip install seoslug

# New - same behavior as 1.x (recommended)
pip install "seoslug[fast]"

# New - pure Python only (minimal)
pip install "seoslug[light]"
```

## New entity types

2.0.0 adds `product`, `organization`, `local_business`, and `faq` to the accepted `entity_type` values. If you validate entity types explicitly in your code, update your allowlist.

```python
# If you had a custom validation list:
VALID_TYPES = {"home", "post", "page", "video", "taxonomy", "search", "other",
               "product", "organization", "local_business", "faq"}  # new types added
```

No code changes are needed if you were using the existing string values. The new types are backward-compatible additions.

## Summary of changes

| Area | 1.x | 2.0.0 |
|------|-----|-------|
| `build_seo_payload` return type | `dict` | `SEOPayload` dataclass |
| Dict access | `payload["key"]` | `payload["key"]` (still works) |
| Attribute access | Not available | `payload.key` (recommended) |
| `.to_dict()` | Not needed | Converts dataclass to dict |
| `build_seo_payload_dict` | Not available | Returns dict directly |
| lxml dependency | Required | Optional (`[fast]` / `[light]` extras) |
| detrack dependency | Required | Optional (`[fast]` / `[light]` extras) |
| Entity types | 7 types | 11 types (+product, organization, local_business, faq) |
| HTML extraction | lxml only | Pure-Python fallback, lxml optional |
