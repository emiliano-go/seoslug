"""Tests for fallback hierarchy behavior."""

from seoslug import SEOConfig, SEOEntity, SEOOverrides, URLPolicy, build_seo_payload


def _config() -> SEOConfig:
    return SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        default_og_image="https://cdn.example.com/default.jpg",
    )


def test_title_and_description_fallbacks() -> None:
    entity = SEOEntity(entity_type="post", title=None, excerpt=None, body_html="<p>Hello body</p>")
    payload = build_seo_payload(entity, "/x", _config())
    assert payload["title"] == "Untitled"
    assert payload["description"] == "Hello body"


def test_override_precedence() -> None:
    entity = SEOEntity(entity_type="post", title="Entity title", excerpt="Entity desc")
    ov = SEOOverrides(meta_title="Override title", meta_description="Override desc")
    payload = build_seo_payload(entity, "/x", _config(), ov)
    assert payload["title"] == "Override title"
    assert payload["description"] == "Override desc"


def test_og_and_twitter_image_fallbacks() -> None:
    entity = SEOEntity(entity_type="post", featured_image=None)
    payload = build_seo_payload(entity, "/x", _config())
    assert payload["og"]["image"] == "https://cdn.example.com/default.jpg"
    assert payload["twitter"]["image"] == "https://cdn.example.com/default.jpg"
