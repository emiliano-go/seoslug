"""Tests for JSON-LD normalization helpers."""

import pytest

from seoslug.jsonld import normalize_schema_jsonld


def test_normalize_schema_jsonld_none_returns_none() -> None:
    assert normalize_schema_jsonld(None) is None


def test_normalize_schema_jsonld_returns_copy_for_dict() -> None:
    schema = {"@type": "WebPage", "name": "Home"}
    normalized = normalize_schema_jsonld(schema)
    assert normalized == schema
    assert normalized is not schema


def test_normalize_schema_jsonld_returns_copy_for_list() -> None:
    schema = [{"@type": "WebPage"}, {"@type": "BreadcrumbList"}]
    normalized = normalize_schema_jsonld(schema)
    assert normalized == schema
    assert normalized is not schema


def test_normalize_schema_jsonld_rejects_invalid_type() -> None:
    with pytest.raises(ValueError):
        normalize_schema_jsonld("bad")  # type: ignore[arg-type]
