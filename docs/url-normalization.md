# URL normalization

seoslug normalizes URLs in a deterministic pipeline.
The result is a clean, canonical URL that never changes for the same input.

## The pipeline

URLs pass through these steps in order.

### 1. Scheme enforcement

If `enforce_https` is True, the scheme is set to https.
If False, the scheme from `public_base_url` is used.

```python
URLPolicy(enforce_https=True)
```

`http://example.com/page` becomes `https://example.com/page`.

### 2. Host enforcement

The host is always set to `canonical_host`.
Host injection attacks are prevented.

```python
SEOConfig(canonical_host="blog.example.com")
```

`https://evil.com/page` becomes `https://blog.example.com/page`.

### 3. Path normalization

Paths are lowercased if `lowercase_paths` is True.
Duplicate slashes are collapsed if `collapse_duplicate_slashes` is True.

```python
URLPolicy(lowercase_paths=True, collapse_duplicate_slashes=True)
```

`//Blog//My-Post//` becomes `/blog/my-post`.

### 4. Trailing slash

The trailing slash policy is applied.
Three modes are available: always, never, or preserve.

```python
URLPolicy(trailing_slash="never")
```

`/blog/post/` becomes `/blog/post`.

### 5. Query parameter filtering

Tracking parameters are stripped if `strip_tracking_params` is True.
This removes UTM parameters, fbclid, gclid, and 60+ other tracking parameters.
The detrack library handles this step automatically.

If `allowed_query_params` is set, only those parameters are kept.
All other parameters are removed.

```python
URLPolicy(
    strip_tracking_params=True,
    allowed_query_params=["q", "page"],
)
```

`?utm_source=twitter&q=python&bad=1` becomes `?q=python`.

## Standalone use

You can use the URL normalizer without generating a full SEO payload.

```python
from seoslug import normalize_public_url, normalize_path

# Normalize a full URL
url = normalize_public_url(
    "http://evil.com//Blog/Post?utm_source=x",
    config,
)
# Result: "https://blog.example.com/blog/post"

# Normalize just the path
path = normalize_path(
    "//Blog//My-Post//",
    URLPolicy(lowercase_paths=True),
)
# Result: "/blog/my-post"
```

## Idempotency

URL normalization is idempotent.
Normalizing an already normalized URL produces the same result.

```python
url = "http://example.com//A//B/?utm_campaign=x"
first = normalize_public_url(url, config)
second = normalize_public_url(first, config)
assert first == second
```
