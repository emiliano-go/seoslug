# Testing and CI/CD

Because seoslug is deterministic, you can snapshot test your entire SEO layer.

## Snapshot testing

Generate a payload once and save it as a JSON file.
In your test suite, regenerate the payload and assert it matches the snapshot.
If anything changes, the test fails.

```python
import json
import pytest
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

EXPECTED = {
    "title": "My Post",
    "canonical": "https://blog.example.com/posts/my-post",
    "robots": "index,follow",
}

def test_blog_post_snapshot():
    entity = SEOEntity(
        entity_type="post",
        title="My Post",
        status="published",
    )
    payload = build_seo_payload(entity, "/posts/my-post", _config())
    assert payload["title"] == EXPECTED["title"]
    assert payload["canonical"] == EXPECTED["canonical"]
    assert payload["robots"] == EXPECTED["robots"]
```

## Full payload assertions

Test the complete payload structure including all nested objects.

```python
EXPECTED_PAYLOAD = {
    "title": "My Post",
    "description": "My excerpt",
    "canonical": "https://blog.example.com/posts/my-post",
    "robots": "index,follow",
    "og": {
        "type": "article",
        "title": "My Post",
        "description": "My excerpt",
        "url": "https://blog.example.com/posts/my-post",
        "image": "https://cdn.example.com/default.jpg",
    },
    "twitter": {
        "card": "summary_large_image",
        "title": "My Post",
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

Test that specific entity types produce the expected output.
This catches regressions when you change your SEO strategy.

```python
@pytest.mark.parametrize("entity_type,route", [
    ("home", "/"),
    ("post", "/posts/p"),
    ("page", "/about"),
    ("video", "/videos/v"),
    ("taxonomy", "/topics/python"),
    ("search", "/search?q=x"),
])
def test_entity_type_snapshots(entity_type, route):
    entity = SEOEntity(
        entity_type=entity_type,
        title=f"{entity_type} title",
        excerpt=f"{entity_type} excerpt",
        status="published",
    )
    payload = build_seo_payload(entity, route, _config())
    # Add your assertions here
    assert payload["canonical"].startswith("https://")
    assert "schema_jsonld" in payload
```

## CI integration

Run your SEO tests in CI to catch regressions before they reach production.
Update snapshots intentionally when you change your SEO configuration.

```yaml
# .github/workflows/seo-tests.yml
- run: pip install seoslug pytest
- run: pytest tests/seo/
```

## What to test

- Title and description fallback chains
- Canonical URL normalization
- Robots directive based on status
- Open Graph and Twitter card generation
- Schema.org JSON-LD structure
- Override precedence
- Tracking parameter stripping
- Idempotency of URL normalization
