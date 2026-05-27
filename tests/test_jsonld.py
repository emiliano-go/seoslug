"""Tests for JSON-LD normalization and schema building."""

import pytest

from seoslug import SEOConfig, SEOEntity, URLPolicy
from seoslug.jsonld import build_schema, normalize_schema_jsonld


def _config(**kwargs) -> SEOConfig:
    defaults = dict(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    defaults.update(kwargs)
    return SEOConfig(**defaults)


def _entity(**kwargs) -> SEOEntity:
    defaults = dict(entity_type="post", title="Test")
    defaults.update(kwargs)
    return SEOEntity(**defaults)


# -- normalize_schema_jsonld (unchanged) --

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


# -- build_schema --

class TestBuildSchema:
    def test_article_type_mapping(self) -> None:
        schema = build_schema(
            _entity(entity_type="post"),
            _config(),
            canonical="https://example.com/p",
            title="My Post",
            description="Desc",
            og_image=None,
        )
        assert schema["@type"] == "Article"
        assert schema["mainEntityOfPage"] == {"@id": "https://example.com/p"}

    def test_webpage_type_mapping(self) -> None:
        schema = build_schema(
            _entity(entity_type="page"),
            _config(),
            canonical="https://example.com/about",
            title="About",
            description=None,
            og_image=None,
        )
        assert schema["@type"] == "WebPage"
        assert "mainEntityOfPage" not in schema

    def test_video_type_mapping(self) -> None:
        schema = build_schema(
            _entity(entity_type="video"),
            _config(),
            canonical="https://example.com/v",
            title="My Video",
            description="Video desc",
            og_image=None,
        )
        assert schema["@type"] == "VideoObject"

    def test_collection_page_mapping(self) -> None:
        schema = build_schema(
            _entity(entity_type="taxonomy"),
            _config(),
            canonical="https://example.com/topics/t",
            title="Taxonomy",
            description=None,
            og_image=None,
        )
        assert schema["@type"] == "CollectionPage"

    def test_search_page_mapping(self) -> None:
        schema = build_schema(
            _entity(entity_type="search"),
            _config(),
            canonical="https://example.com/search?q=x",
            title="Search",
            description=None,
            og_image=None,
        )
        assert schema["@type"] == "SearchResultsPage"

    def test_returns_none_for_unmapped_type(self) -> None:
        config = _config(schema_type_map={})
        schema = build_schema(
            _entity(entity_type="post"),
            config,
            canonical="https://example.com/p",
            title="Post",
            description=None,
            og_image=None,
        )
        assert schema is None

    def test_custom_type_map(self) -> None:
        config = _config(schema_type_map={"other": "Product"})
        schema = build_schema(
            _entity(entity_type="other"),
            config,
            canonical="https://example.com/prod",
            title="Product",
            description=None,
            og_image=None,
        )
        assert schema["@type"] == "Product"

    def test_conditional_fields(self) -> None:
        schema = build_schema(
            _entity(
                entity_type="post",
                published_at="2024-01-15T10:00:00Z",
                updated_at="2024-01-16T12:00:00Z",
            ),
            _config(),
            canonical="https://example.com/p",
            title="Post",
            description="Desc",
            og_image="https://example.com/img.jpg",
        )
        assert schema["datePublished"] == "2024-01-15T10:00:00Z"
        assert schema["dateModified"] == "2024-01-16T12:00:00Z"
        assert schema["image"] == "https://example.com/img.jpg"
        assert schema["description"] == "Desc"

    def test_conditional_fields_omitted_when_missing(self) -> None:
        schema = build_schema(
            _entity(entity_type="page"),
            _config(),
            canonical="https://example.com/p",
            title="Page",
            description=None,
            og_image=None,
        )
        assert "datePublished" not in schema
        assert "dateModified" not in schema
        assert "image" not in schema
        assert "description" not in schema

    def test_author_field(self) -> None:
        schema = build_schema(
            _entity(entity_type="post", author_name="Jane Doe"),
            _config(),
            canonical="https://example.com/p",
            title="Post",
            description=None,
            og_image=None,
        )
        assert schema["author"] == {"@type": "Person", "name": "Jane Doe"}

    def test_publisher_field(self) -> None:
        schema = build_schema(
            _entity(entity_type="post"),
            _config(publisher_name="Acme Corp", publisher_logo="https://example.com/logo.png"),
            canonical="https://example.com/a",
            title="Article",
            description=None,
            og_image=None,
        )
        assert schema["publisher"] == {
            "@type": "Organization",
            "name": "Acme Corp",
            "logo": "https://example.com/logo.png",
        }

    def test_publisher_without_logo(self) -> None:
        schema = build_schema(
            _entity(entity_type="post"),
            _config(publisher_name="Acme Corp"),
            canonical="https://example.com/a",
            title="Article",
            description=None,
            og_image=None,
        )
        assert schema["publisher"] == {"@type": "Organization", "name": "Acme Corp"}
        assert "logo" not in schema["publisher"]
