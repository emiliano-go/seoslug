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


def test_canonical_fallback_uses_normalized_route() -> None:
    entity = SEOEntity(entity_type="page", title="About")
    payload = build_seo_payload(entity, "/About//Team?utm_source=x", _config())
    assert payload["canonical"] == "https://portal.example.com/about/team"


def test_og_image_precedence_override_then_entity_then_default() -> None:
    base_entity = SEOEntity(entity_type="post", featured_image="https://cdn.example.com/entity.jpg")
    with_override = build_seo_payload(
        base_entity,
        "/x",
        _config(),
        SEOOverrides(og_image="https://cdn.example.com/override.jpg"),
    )
    assert with_override["og"]["image"] == "https://cdn.example.com/override.jpg"

    without_override = build_seo_payload(base_entity, "/x", _config())
    assert without_override["og"]["image"] == "https://cdn.example.com/entity.jpg"

    no_entity_image = build_seo_payload(SEOEntity(entity_type="post"), "/x", _config())
    assert no_entity_image["og"]["image"] == "https://cdn.example.com/default.jpg"


def test_twitter_override_fields_take_highest_precedence() -> None:
    entity = SEOEntity(entity_type="post", title="Entity", excerpt="Excerpt")
    payload = build_seo_payload(
        entity,
        "/x",
        _config(),
        SEOOverrides(
            twitter_card="summary",
            twitter_title="Tw Title",
            twitter_description="Tw Desc",
            twitter_image="https://cdn.example.com/tw.jpg",
            og_title="OG Title",
            og_description="OG Desc",
            og_image="https://cdn.example.com/og.jpg",
        ),
    )
    assert payload["twitter"]["card"] == "summary"
    assert payload["twitter"]["title"] == "Tw Title"
    assert payload["twitter"]["description"] == "Tw Desc"
    assert payload["twitter"]["image"] == "https://cdn.example.com/tw.jpg"
