---
seo:
  title: Testing and CI/CD - seoslug
  canonical: https://seoslug.emiliano-go.com/testing/
  robots: index,follow
  og:
    type: website
    title: Testing and CI/CD - seoslug
    description: seoslug is deterministic. Same inputs always produce the same outputs.
      This makes your SEO layer fully snapshot-testable.
    url: https://seoslug.emiliano-go.com/testing/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Testing and CI/CD - seoslug
    description: seoslug is deterministic. Same inputs always produce the same outputs.
      This makes your SEO layer fully snapshot-testable.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: seoslug is deterministic. Same inputs always produce the same outputs.
    This makes your SEO layer fully snapshot-testable.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Testing and CI/CD - seoslug
    url: https://seoslug.emiliano-go.com/testing/
    description: seoslug is deterministic. Same inputs always produce the same outputs.
      This makes your SEO layer fully snapshot-testable.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Testing and CI/CD - seoslug</title>\n<meta name=\"description\"\
  \ content=\"seoslug is deterministic. Same inputs always produce the same outputs.\
  \ This makes your SEO layer fully snapshot-testable.\">\n<link rel=\"canonical\"\
  \ href=\"https://seoslug.emiliano-go.com/testing/\">\n<meta name=\"robots\" content=\"\
  index,follow\">\n<meta property=\"og:type\" content=\"website\">\n<meta property=\"\
  og:title\" content=\"Testing and CI/CD - seoslug\">\n<meta property=\"og:description\"\
  \ content=\"seoslug is deterministic. Same inputs always produce the same outputs.\
  \ This makes your SEO layer fully snapshot-testable.\">\n<meta property=\"og:url\"\
  \ content=\"https://seoslug.emiliano-go.com/testing/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Testing and CI/CD - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"seoslug is deterministic. Same inputs always\
  \ produce the same outputs. This makes your SEO layer fully snapshot-testable.\"\
  >\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Testing and CI/CD - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/testing/\"\
  ,\n  \"description\": \"seoslug is deterministic. Same inputs always produce the\
  \ same outputs. This makes your SEO layer fully snapshot-testable.\",\n  \"image\"\
  : \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n  \"publisher\"\
  : {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano Gandini Outeda\"\
  ,\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\n\
  \  }\n}\n</script>\n"
---

# Testing and CI/CD

seoslug is deterministic. Same inputs always produce the same outputs.
This makes your SEO layer fully snapshot-testable.

## Snapshot testing

Generate a payload once and assert nothing changes.

```python
from seoslug import build_seo_payload

EXPECTED = {
    "title": "My Post - My Blog",
    "canonical": "https://blog.example.com/posts/my-post",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "My Post - My Blog",
        "url": "https://blog.example.com/posts/my-post",
    },
    "twitter": {"card": "summary_large_image"},
}

def test_blog_post_snapshot():
    entity = SEOEntity(entity_type="post", title="My Post", status="published")
    payload = build_seo_payload(entity, "/posts/my-post", _config())
    assert payload["title"] == EXPECTED["title"]
    assert payload["canonical"] == EXPECTED["canonical"]
```

Use `payload == EXPECTED` for full payload equality (works because `SEOPayload` supports dict comparison):

```python
EXPECTED_PAYLOAD = {
    "title": "My Post - My Blog",
    "description": "My excerpt",
    "canonical": "https://blog.example.com/posts/my-post",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "My Post - My Blog",
        "description": "My excerpt",
        "url": "https://blog.example.com/posts/my-post",
        "image": "https://cdn.example.com/default.jpg",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "My Post - My Blog",
        "description": "My excerpt",
        "image": "https://cdn.example.com/default.jpg",
    },
}

def test_full_payload():
    entity = SEOEntity(
        entity_type="post",
        title="My Post",
        excerpt="My excerpt",
        status="published",
    )
    payload = build_seo_payload(entity, "/posts/my-post", _config())
    assert payload == EXPECTED_PAYLOAD
```

## Regression testing

Parameterize across entity types to catch regressions:

```python
import pytest

@pytest.mark.parametrize("entity_type,route,expected", [
    ("home", "/", HOME_EXPECTED),
    ("post", "/posts/p", POST_EXPECTED),
    ("page", "/about", PAGE_EXPECTED),
    ("video", "/videos/v", VIDEO_EXPECTED),
    ("taxonomy", "/topics/python", TAXONOMY_EXPECTED),
    ("search", "/search?q=x", SEARCH_EXPECTED),
    ("other", "/other", OTHER_EXPECTED),
    ("product", "/products/widget", PRODUCT_EXPECTED),
    ("organization", "/about", ORGANIZATION_EXPECTED),
    ("local_business", "/shop", LOCAL_BUSINESS_EXPECTED),
    ("faq", "/faq", FAQ_EXPECTED),
])
def test_regression_entity_type_snapshots(entity_type, route, expected):
    entity = SEOEntity(
        entity_type=entity_type,
        title=f"{entity_type} title",
        excerpt=f"{entity_type} excerpt",
        status="published",
    )
    payload = build_seo_payload(entity, route, _config())
    assert payload == expected
```

Store expected dicts in a fixtures module.
Update intentionally when you change your SEO strategy.

## CI integration

```yaml
# .github/workflows/seo-tests.yml
name: SEO Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python: ["3.10", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python }}
      - run: pip install -e .[test]
      - run: pytest --cov=seoslug tests/
```

## What to test

- Title and description fallback chains
- Canonical URL normalization (including sub-path and idempotency)
- Robots directive based on entity status and type
- Open Graph and Twitter card generation
- OGImage structured data (width, height, alt)
- Schema.org JSON-LD structure per entity type
- Override precedence for every field
- Tracking parameter stripping and query allowlists
- BreadcrumbList auto-generation
- SEOEntityBuilder fluent builder output
- Async builder matches sync builder
- Validation warnings (title length, description length, URL scheme)
