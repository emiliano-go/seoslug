"""Tests for SEO payload and JSON-LD validation."""

import warnings

import pytest

from seoslug import SEOConfig, SEOEntity, SEOEntityError, SEOOverrides, URLPolicy, build_seo_payload
from seoslug.validation import validate_html_jsonld, validate_schema_jsonld


def _config(**kw) -> SEOConfig:
    defaults = dict(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        emit_warnings=True,
    )
    defaults.update(kw)
    return SEOConfig(**defaults)


def test_title_too_long_warns() -> None:
    entity = SEOEntity(entity_type="page", title="A" * 70)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        build_seo_payload(entity, "/page", _config())
    assert any("Title exceeds 60" in str(msg.message) for msg in w), [str(m.message) for m in w]


def test_description_too_long_warns() -> None:
    entity = SEOEntity(entity_type="page", title="Page", excerpt="B" * 300)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        build_seo_payload(entity, "/page", _config())
    assert any("Description exceeds 160" in str(msg.message) for msg in w), [str(m.message) for m in w]


def test_emit_warnings_false_no_warnings() -> None:
    config = SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        emit_warnings=False,
    )
    entity = SEOEntity(entity_type="page", title="A" * 70)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        build_seo_payload(entity, "/page", config)
    seo_warnings = [msg for msg in w if "seoslug" in str(msg.message).lower() or "Title" in str(msg.message)]
    assert len(seo_warnings) == 0


# ---------------------------------------------------------------------------
# Additional coverage: _nested_get
# ---------------------------------------------------------------------------


def test_nested_get_non_dict_intermediate() -> None:
    from seoslug.validation import _nested_get
    d = {"og": "not a dict"}
    result = _nested_get(d, ("og", "image"), "default")
    assert result == "default"


# ---------------------------------------------------------------------------
# Additional coverage: _valid_robots_format
# ---------------------------------------------------------------------------


def test_valid_robots_format_empty() -> None:
    from seoslug.validation import _valid_robots_format
    assert _valid_robots_format("") is False


def test_valid_robots_format_empty_stripped_directive() -> None:
    from seoslug.validation import _valid_robots_format
    assert _valid_robots_format("index, ") is False
    assert _valid_robots_format(", follow") is False


def test_valid_robots_format_colon_empty_name_returns_false() -> None:
    from seoslug.validation import _valid_robots_format
    assert _valid_robots_format(":value") is False


def test_valid_robots_format_colon_empty_value_returns_false() -> None:
    from seoslug.validation import _valid_robots_format
    assert _valid_robots_format("name:") is False


def test_valid_robots_format_unknown_directive_returns_false() -> None:
    from seoslug.validation import _valid_robots_format
    assert _valid_robots_format("unknown") is False
    assert _valid_robots_format("index,unknown") is False


# ---------------------------------------------------------------------------
# Additional coverage: validate_payload warnings
# ---------------------------------------------------------------------------


def test_canonical_not_absolute_warns() -> None:
    from seoslug.validation import validate_payload

    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    payload = {
        "title": "Test",
        "canonical": "relative/path",
    }
    warnings_list = validate_payload(payload, config)
    assert any("Canonical URL is not absolute" in w for w in warnings_list)


def test_og_image_not_absolute_warns() -> None:
    from seoslug.validation import validate_payload

    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    payload = {
        "title": "Test",
        "og": {"image": "relative/image.jpg"},
    }
    warnings_list = validate_payload(payload, config)
    assert any("OG image URL is not absolute" in w for w in warnings_list)


def test_malformed_robots_warns() -> None:
    from seoslug.validation import validate_payload

    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    payload = {
        "title": "Test",
        "robots": "unknown_directive",
    }
    warnings_list = validate_payload(payload, config)
    assert any("Robots directive may be malformed" in w for w in warnings_list)


def test_validate_schema_jsonld_recurses_graph() -> None:
    warnings_list = validate_schema_jsonld(
        {
            "@context": "https://schema.org",
            "@graph": [
                {"@context": "https://schema.org", "@type": "WebPage", "name": "Home"},
                {"@context": "https://schema.org", "@type": "Article", "headline": "Post"},
            ],
        }
    )
    assert any("recommended description is missing" in warning for warning in warnings_list)


def test_validate_schema_jsonld_strict_raises() -> None:
    with pytest.raises(SEOEntityError):
        validate_schema_jsonld({"@context": "https://schema.org", "@type": "WebPage"}, strict=True)


def test_validate_html_jsonld_detects_exact_duplicates() -> None:
    html = """
    <html><head>
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage"}</script>
    <script type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage"}</script>
    </head></html>
    """
    warnings_list = validate_html_jsonld(html)
    assert any("Duplicate JSON-LD block" in warning for warning in warnings_list)
