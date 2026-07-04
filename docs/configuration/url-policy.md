---
{}
---

# URLPolicy reference

`URLPolicy` controls how URLs are normalized before they become canonical. Every canonical URL flows through this pipeline. Create one instance and attach it to your `SEOConfig`.

## Fields

| Option | Type | Default | Description |
|---|---|---|---|
| `enforce_https` | `bool` | `True` | Force HTTPS scheme in all canonical URLs. |
| `lowercase_paths` | `bool` | `True` | Lowercase the path component. |
| `trailing_slash` | `Literal` | `"never"` | Trailing slash policy: `"always"`, `"never"`, or `"preserve"`. |
| `collapse_duplicate_slashes` | `bool` | `True` | Collapse consecutive slashes into one. |
| `strip_tracking_params` | `bool` | `True` | Remove tracking parameters (UTM, fbclid, gclid, 60+ more). |
| `allowed_query_params` | `list[str]` | `[]` | Allowlist of query parameters to keep. Empty list keeps all non-tracking params. |

### enforce_https

When `True`, all canonical URLs use `https://`. When `False`, the scheme from `config.public_base_url` is used.

```python
URLPolicy(enforce_https=True)
# http://example.com/page → https://example.com/page

URLPolicy(enforce_https=False)
# Uses whatever scheme is in public_base_url
```

### lowercase_paths

When `True`, the path component is lowercased. This prevents duplicate content from case-insensitive URL variations.

```python
URLPolicy(lowercase_paths=True)
# /Blog/My-Post → /blog/my-post
```

### trailing_slash

Controls whether canonical URLs end with a trailing slash. Accepts exactly three values:

- `"always"`: append a trailing slash to every path
- `"never"`: remove trailing slashes from every path
- `"preserve"`: leave the path as-is

```python
URLPolicy(trailing_slash="always")
# /blog/post → /blog/post/

URLPolicy(trailing_slash="never")
# /blog/post/ → /blog/post

URLPolicy(trailing_slash="preserve")
# Keeps original casing and slash
```

### collapse_duplicate_slashes

When `True`, consecutive slashes are collapsed into a single slash. Prevents path injection-style duplicates.

```python
URLPolicy(collapse_duplicate_slashes=True)
# //blog//post// → /blog/post/
```

### strip_tracking_params

When `True`, removes common tracking parameters from URLs. Removes UTM parameters (`utm_source`, `utm_medium`, etc.), `fbclid`, `gclid`, `gclsrc`, and 60+ other tracking parameters.

This feature uses the optional `detrack` library when available, with a pure-Python fallback.

```python
URLPolicy(strip_tracking_params=True)
# /page?utm_source=twitter&utm_campaign=summer&gclid=abc → /page
```

### allowed_query_params

When set, only the listed query parameters are kept. All others are stripped. When empty (the default), all non-tracking parameters are preserved.

Processing order: tracking parameters are stripped first, then the allowlist is applied.

```python
URLPolicy(allowed_query_params=["q", "page", "sort"])
# /search?q=seo&page=2&utm_source=twitter&ref=sidebar → /search?q=seo&page=2
```

## Strict policy

Combines all options for maximum URL consistency. Use this when you need canonical URLs to be identical regardless of how users arrive.

```python
from seoslug import URLPolicy

policy = URLPolicy(
    enforce_https=True,
    lowercase_paths=True,
    trailing_slash="never",
    collapse_duplicate_slashes=True,
    strip_tracking_params=True,
    allowed_query_params=["q", "page"],
)
```

What this policy does:

- Forces HTTPS (no mixed content)
- Lowercases paths (`/Blog/Post` and `/blog/post` are the same)
- Removes trailing slashes (no slash/no-slash duplicates)
- Collapses `//` (no path injection)
- Strips UTM, fbclid, gclid (clean URLs)
- Keeps only `q` and `page` (no arbitrary query params)

```python
config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
        collapse_duplicate_slashes=True,
        strip_tracking_params=True,
        allowed_query_params=["q", "page"],
    ),
)
```

Result: every canonical URL is predictable, clean, and reproducible.
