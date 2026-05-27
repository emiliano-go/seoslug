"""Tests for SEOEntity and SEOOverrides models."""

import pytest

from seoslug import SEOEntity, SEOOverrides


def test_entity_normalizes_optional_string_fields() -> None:
    entity = SEOEntity(
        entity_type="post",
        slug=" my-post ",
        title="  Hello ",
        excerpt="   ",
    )
    assert entity.slug == "my-post"
    assert entity.title == "Hello"
    assert entity.excerpt is None


def test_entity_rejects_invalid_entity_type() -> None:
    with pytest.raises(ValueError):
        SEOEntity(entity_type="invalid")


def test_entity_rejects_non_string_optional_field() -> None:
    with pytest.raises(ValueError):
        SEOEntity(entity_type="post", title=123)  # type: ignore[arg-type]


def test_overrides_normalize_and_validate_schema_type() -> None:
    overrides = SEOOverrides(meta_title="  A ", robots="  ")
    assert overrides.meta_title == "A"
    assert overrides.robots is None

    with pytest.raises(ValueError):
        SEOOverrides(schema_jsonld=[{"@type": "WebPage"}, "bad"])  # type: ignore[list-item]
