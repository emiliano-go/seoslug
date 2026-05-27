"""Tests for robots rule behavior."""

from seoslug import SEOConfig, SEOEntity, SEOOverrides, URLPolicy, build_seo_payload


def _config() -> SEOConfig:
    return SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        default_robots="index,follow",
        search_robots="noindex,follow",
    )


def test_published_content_defaults_to_index_follow() -> None:
    entity = SEOEntity(entity_type="post", status="published")
    payload = build_seo_payload(entity, "/posts/x", _config())
    assert payload["robots"] == "index,follow"


def test_search_uses_search_robots() -> None:
    entity = SEOEntity(entity_type="search", status="published")
    payload = build_seo_payload(entity, "/search?q=x", _config())
    assert payload["robots"] == "noindex,follow"


def test_override_robots_wins() -> None:
    entity = SEOEntity(entity_type="post", status="draft")
    ov = SEOOverrides(robots="noindex,nofollow")
    payload = build_seo_payload(entity, "/posts/x", _config(), ov)
    assert payload["robots"] == "noindex,nofollow"
