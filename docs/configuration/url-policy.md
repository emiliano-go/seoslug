# URLPolicy reference

`URLPolicy` controls how URLs are normalized before becoming canonical.

## Fields

### enforce_https (optional)

Converts HTTP to HTTPS in canonical URLs.
Defaults to True.

```python
URLPolicy(enforce_https=True)
```

When True, the scheme is always https.
When False, the scheme from public_base_url is used.

### lowercase_paths (optional)

Normalizes path case to lowercase.
Defaults to True.

```python
URLPolicy(lowercase_paths=True)
```

`/Blog/My-Post` becomes `/blog/my-post`.

### trailing_slash (optional)

Controls trailing slash behavior.
Accepts three values: `"always"`, `"never"`, or `"preserve"`.
Defaults to `"never"`.

```python
URLPolicy(trailing_slash="always")   # /blog/post/
URLPolicy(trailing_slash="never")    # /blog/post
URLPolicy(trailing_slash="preserve") # keeps original
```

### collapse_duplicate_slashes (optional)

Collapses consecutive slashes into one.
Defaults to True.

```python
URLPolicy(collapse_duplicate_slashes=True)
```

`//blog//post//` becomes `/blog/post/`.

### strip_tracking_params (optional)

Removes tracking parameters from URLs.
Defaults to True.

```python
URLPolicy(strip_tracking_params=True)
```

Removes UTM parameters, fbclid, gclid, and 60+ other tracking parameters.
This feature requires the detrack library, which is installed automatically.

### allowed_query_params (optional)

List of query parameters to keep.
When set, all other parameters are removed.
Defaults to an empty list, which keeps all non tracking parameters.

```python
URLPolicy(allowed_query_params=["page", "q", "sort"])
```

When combined with `strip_tracking_params`, tracking parameters are removed first,
then the allowlist is applied.

## Example

A complete URLPolicy that enforces strict canonical URLs.

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

This policy produces clean, canonical URLs that are consistent across all pages.
