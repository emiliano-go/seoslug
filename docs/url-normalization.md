---
seo:
  title: URL Normalization - seoslug
  canonical: https://seoslug.emiliano-go.com/url-normalization/
  robots: index,follow
  og:
    type: website
    title: URL Normalization - seoslug
    description: seoslug normalizes URLs through a deterministic pipeline. The output
      is always a clean canonical URL.
    url: https://seoslug.emiliano-go.com/url-normalization/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: URL Normalization - seoslug
    description: seoslug normalizes URLs through a deterministic pipeline. The output
      is always a clean canonical URL.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: seoslug normalizes URLs through a deterministic pipeline. The output
    is always a clean canonical URL.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: URL Normalization - seoslug
    url: https://seoslug.emiliano-go.com/url-normalization/
    description: seoslug normalizes URLs through a deterministic pipeline. The output
      is always a clean canonical URL.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>URL Normalization - seoslug</title>\n<meta name=\"description\"\
  \ content=\"seoslug normalizes URLs through a deterministic pipeline. The output\
  \ is always a clean canonical URL.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/url-normalization/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"URL Normalization - seoslug\"\
  >\n<meta property=\"og:description\" content=\"seoslug normalizes URLs through a\
  \ deterministic pipeline. The output is always a clean canonical URL.\">\n<meta\
  \ property=\"og:url\" content=\"https://seoslug.emiliano-go.com/url-normalization/\"\
  >\n<meta property=\"og:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta property=\"og:image:width\" content=\"225\">\n<meta property=\"og:image:height\"\
  \ content=\"225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta\
  \ property=\"og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"\
  summary_large_image\">\n<meta name=\"twitter:title\" content=\"URL Normalization\
  \ - seoslug\">\n<meta name=\"twitter:description\" content=\"seoslug normalizes\
  \ URLs through a deterministic pipeline. The output is always a clean canonical\
  \ URL.\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"URL Normalization - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/url-normalization/\"\
  ,\n  \"description\": \"seoslug normalizes URLs through a deterministic pipeline.\
  \ The output is always a clean canonical URL.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# URL Normalization

seoslug normalizes URLs through a deterministic pipeline.
The output is always a clean canonical URL.

Every step is controlled by `URLPolicy` and `canonical_host`.

## The pipeline

URLs pass through these steps in order.

### 0. Base path prepending

If `public_base_url` contains a path, it is prepended to the route path before any other step.

```python
from seoslug import SEOConfig

config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com/blog",
    url_policy=...,
)
```

| Input  | Result          |
|--------|-----------------|
| `/page`   | `/blog/page`    |
| `/`       | `/blog`         |

This enables sub-path deployments like `https://example.com/blog/`.

### 1. Scheme enforcement

Sets the URL scheme. HTTPS by default.

| `enforce_https` | Behavior                          |
|-----------------|-----------------------------------|
| `True`          | Always `https`                    |
| `False`         | Uses scheme from `public_base_url`|

```python
from seoslug import URLPolicy

URLPolicy(enforce_https=True)
```

`http://other.com/page` becomes `https://portal.example.com/page`.

### 2. Host enforcement

Always replaces the host with `canonical_host`.
Host injection attacks are prevented.

```python
SEOConfig(canonical_host="portal.example.com")
```

`https://evil.com/path` becomes `https://portal.example.com/path`.

### 3. Path normalization

Two operations controlled by `URLPolicy`:

| Setting                     | Default | Effect |
|-----------------------------|---------|--------|
| `lowercase_paths`           | `True`  | Lowercases the path |
| `collapse_duplicate_slashes`| `True`  | Reduces `//` to `/` |

```python
URLPolicy(
    lowercase_paths=True,
    collapse_duplicate_slashes=True,
)
```

`//Blog//My-Post//` becomes `/blog/my-post`.

### 4. Trailing slash

Three modes:

| `trailing_slash` | Effect                    |
|------------------|---------------------------|
| `"never"`        | Removes trailing slash    |
| `"always"`       | Adds trailing slash       |
| `"preserve"`     | Leaves as-is              |

```python
URLPolicy(trailing_slash="never")
```

`/blog/post/` becomes `/blog/post`.

### 5. Query parameter filtering

Two layers of filtering:

**Tracking param stripping**: removes UTM parameters, fbclid, gclid, msclkid, and 60+ more. Uses the `detrack` library if installed, otherwise a built-in regex.

| `strip_tracking_params` | Behavior                          |
|-------------------------|-----------------------------------|
| `True` (default)        | Strips known tracking params      |
| `False`                 | Keeps all params                  |

**Query allowlist**: when set, only the listed params are kept. All others are removed.

```python
URLPolicy(
    strip_tracking_params=True,
    allowed_query_params=["q", "page", "sort"],
)
```

`?utm_source=twitter&q=python&bad=1&page=2` becomes `?q=python&page=2`.

## Sub-path deployment example

```python
from seoslug import SEOConfig, URLPolicy

config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com/blog",
    url_policy=URLPolicy(
        lowercase_paths=True,
        trailing_slash="never",
        collapse_duplicate_slashes=True,
        strip_tracking_params=True,
    ),
)

# Given route "/about"
# Result: "https://example.com/blog/about"

# Given route "/"
# Result: "https://example.com/blog"
```

Sub-path canonical URLs work because base path prepending happens at step 0, before path normalization.

## Standalone use

URL normalization functions are public. Use them without building a full payload.

```python
from seoslug import normalize_public_url, normalize_path, URLPolicy

# Normalize a full URL with config
url = normalize_public_url(
    "http://evil.com//Blog/Post?utm_source=x",
    config,
)
# Result: "https://example.com/blog/post"

# Normalize just the path with a policy
path = normalize_path(
    "//Blog//My-Post//",
    URLPolicy(lowercase_paths=True, trailing_slash="never"),
)
# Result: "/blog/my-post"
```

## Idempotency

Normalization is idempotent. Running it twice produces the same result.

```python
url = "http://example.com//A//B/?utm_campaign=x"
first = normalize_public_url(url, config)
second = normalize_public_url(first, config)
assert first == second  # always True
```

This holds for sub-path deployments too.
