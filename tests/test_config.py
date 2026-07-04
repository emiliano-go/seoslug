"""Tests for config module — URLPolicy, SEOConfig, and helper validators."""

import pytest

from seoslug import (
    OGImage,
    Robots,
    SEOConfig,
    SEOConfigError,
    URLPolicy,
    URLPolicyError,
)
from seoslug.config import (
    _validate_canonical_host,
    _validate_image_config,
    _validate_public_base_url,
    _validate_robots_config,
)


# ── URLPolicy ──────────────────────────────────────────────────────────────


def test_invalid_trailing_slash_raises_error() -> None:
    with pytest.raises(URLPolicyError, match="trailing_slash"):
        URLPolicy(trailing_slash="invalid")


def test_allowed_query_params_non_string_raises_error() -> None:
    with pytest.raises(URLPolicyError, match="allowed_query_params must contain only strings"):
        URLPolicy(allowed_query_params=["ok", 42])


def test_allowed_query_params_empty_string_skipped() -> None:
    policy = URLPolicy(allowed_query_params=["  ", "page", ""])
    assert policy.allowed_query_params == ["page"]


def test_allowed_query_params_duplicates_deduplicated() -> None:
    policy = URLPolicy(allowed_query_params=["page", "page", "q", "q"])
    assert policy.allowed_query_params == ["page", "q"]


# ── SEOConfig ──────────────────────────────────────────────────────────────


def _valid_config(**kw) -> SEOConfig:
    defaults = dict(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    defaults.update(kw)
    return SEOConfig(**defaults)


def test_url_policy_not_urlpolicy_instance_raises_error() -> None:
    with pytest.raises(SEOConfigError, match="url_policy must be a URLPolicy instance"):
        SEOConfig(
            canonical_host="example.com",
            public_base_url="https://example.com",
            url_policy="invalid",  # type: ignore[arg-type]
        )


def test_site_name_empty_raises_error() -> None:
    with pytest.raises(SEOConfigError, match="site_name must be a non-empty string when set"):
        _valid_config(site_name="  ")


def test_title_template_empty_raises_error() -> None:
    with pytest.raises(SEOConfigError, match="title_template must be a non-empty string when set"):
        _valid_config(title_template="  ")


def test_title_template_missing_placeholder_raises_error() -> None:
    with pytest.raises(SEOConfigError, match="title_template must include"):
        _valid_config(title_template="Hello World")


def test_locale_empty_raises_error() -> None:
    with pytest.raises(ValueError, match="locale must be a non-empty string when set"):
        _valid_config(locale="  ")


def test_twitter_site_empty_raises_error() -> None:
    with pytest.raises(ValueError, match="twitter_site must be a non-empty string when set"):
        _valid_config(twitter_site="  ")


def test_locale_alternate_duplicates_cleaned() -> None:
    config = _valid_config(locale_alternate=["es_ES", "fr_FR", "es_ES", "", "fr_FR"])
    assert config.locale_alternate == ["es_ES", "fr_FR"]


# ── Helper validators ──────────────────────────────────────────────────────


def test_validate_robots_config_empty_string_raises_valueerror() -> None:
    with pytest.raises(ValueError, match="must be a non-empty string or Robots instance"):
        _validate_robots_config("  ", "test_field")


def test_validate_image_config_invalid_type_raises_valueerror() -> None:
    with pytest.raises(ValueError, match="must be a non-empty string, OGImage, or None"):
        _validate_image_config(42, "test_field")  # type: ignore[arg-type]


def test_validate_canonical_host_empty_string_raises_seoconfigerror() -> None:
    with pytest.raises(SEOConfigError, match="canonical_host must be a non-empty string"):
        _validate_canonical_host("  ")


def test_validate_public_base_url_empty_string_raises_seoconfigerror() -> None:
    with pytest.raises(SEOConfigError, match="public_base_url must be a non-empty string"):
        _validate_public_base_url("  ")


def test_validate_public_base_url_invalid_scheme_raises_seoconfigerror() -> None:
    with pytest.raises(SEOConfigError, match="must be an absolute http"):
        _validate_public_base_url("ftp://example.com")
