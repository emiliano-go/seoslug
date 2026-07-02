"""Tests for SEO payload validation warnings."""

import warnings

from seoslug import SEOConfig, SEOEntity, SEOOverrides, URLPolicy, build_seo_payload


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
