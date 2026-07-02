"""Tests for JSON-LD normalization and schema building."""

import pytest

from seoslug import Breadcrumb, SEOConfig, SEOEntity, SEOEntityError, SchemaRegistry, URLPolicy
from seoslug.jsonld import build_breadcrumb_list, build_schema, normalize_schema_jsonld


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
    with pytest.raises(SEOEntityError):
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


# --- New schema builders ---

class TestProductSchema:
    def test_basic_product(self) -> None:
        entity = _entity(entity_type="product", title="Widget", sku="W-001", price="29.99", price_currency="USD")
        schema = build_schema(entity, _config(), "https://ex.com/p", "Widget", "A widget", None)
        assert schema["@type"] == "Product"
        assert schema["sku"] == "W-001"
        assert schema["offers"]["price"] == "29.99"
        assert schema["offers"]["priceCurrency"] == "USD"

    def test_product_availability(self) -> None:
        entity = _entity(entity_type="product", availability="InStock")
        schema = build_schema(entity, _config(), "https://ex.com/p", "Product", None, None)
        assert schema["offers"]["availability"] == "https://schema.org/InStock"

    def test_product_no_offer_when_no_data(self) -> None:
        entity = _entity(entity_type="product")
        schema = build_schema(entity, _config(), "https://ex.com/p", "Product", None, None)
        assert "offers" not in schema


class TestOrganizationSchema:
    def test_basic_organization(self) -> None:
        entity = _entity(entity_type="organization", title="Acme Inc", same_as=["https://twitter.com/acme"])
        schema = build_schema(entity, _config(), "https://ex.com", "Acme Inc", None, None)
        assert schema["@type"] == "Organization"
        assert schema["sameAs"] == ["https://twitter.com/acme"]

    def test_org_with_logo(self) -> None:
        entity = _entity(entity_type="organization")
        schema = build_schema(entity, _config(publisher_logo="https://ex.com/logo.png"), "https://ex.com", "Acme", None, None)
        assert schema["logo"] == "https://ex.com/logo.png"


class TestLocalBusinessSchema:
    def test_basic_local_business(self) -> None:
        entity = _entity(entity_type="local_business", title="My Shop", address="123 Main St")
        schema = build_schema(entity, _config(), "https://ex.com/shop", "My Shop", None, None)
        assert schema["@type"] == "LocalBusiness"
        assert schema["address"]["streetAddress"] == "123 Main St"
        assert "sameAs" not in schema  # inherits from Organization builder

    def test_local_business_with_same_as(self) -> None:
        entity = _entity(entity_type="local_business", same_as=["https://fb.me/shop"])
        schema = build_schema(entity, _config(), "https://ex.com/shop", "Shop", None, None)
        assert schema["sameAs"] == ["https://fb.me/shop"]


class TestFAQPageSchema:
    def test_basic_faq(self) -> None:
        from seoslug import FAQItem
        entity = _entity(entity_type="faq", title="FAQ", faq_items=[FAQItem(question="Q1?", answer="A1.")])
        schema = build_schema(entity, _config(), "https://ex.com/faq", "FAQ", None, None)
        assert schema["@type"] == "FAQPage"
        assert len(schema["mainEntity"]) == 1
        assert schema["mainEntity"][0]["@type"] == "Question"
        assert schema["mainEntity"][0]["name"] == "Q1?"
        assert schema["mainEntity"][0]["acceptedAnswer"]["text"] == "A1."

    def test_faq_no_items(self) -> None:
        entity = _entity(entity_type="faq")
        schema = build_schema(entity, _config(), "https://ex.com/faq", "FAQ", None, None)
        assert "mainEntity" not in schema


class TestBreadcrumbListSchema:
    def test_basic_breadcrumbs(self) -> None:
        bcs = [Breadcrumb(name="Home", url="/"), Breadcrumb(name="Blog", url="/blog")]
        schema = build_breadcrumb_list(bcs, _config())
        assert schema["@type"] == "BreadcrumbList"
        assert len(schema["itemListElement"]) == 2
        assert schema["itemListElement"][0]["position"] == 1
        assert schema["itemListElement"][0]["name"] == "Home"
        assert schema["itemListElement"][0]["item"] == "https://example.com/"
        assert schema["itemListElement"][1]["item"] == "https://example.com/blog"


class TestSchemaRegistry:
    def test_registry_called_when_registered(self) -> None:
        registry = SchemaRegistry()
        called = False
        def podcast_gen(entity, config, canonical, title, description, og_image):
            nonlocal called
            called = True
            return {"@type": "Podcast", "name": title}
        registry.register("Podcast", podcast_gen)
        config = _config(schema_type_map={"other": "Podcast"}, schema_registry=registry)
        entity = _entity(entity_type="other", title="My Podcast")
        schema = build_schema(entity, config, "https://ex.com/pod", "My Podcast", None, None)
        assert called
        assert schema["@type"] == "Podcast"

    def test_registry_falls_back_to_builtin(self) -> None:
        registry = SchemaRegistry()
        config = _config(schema_registry=registry)
        entity = _entity(entity_type="post")
        schema = build_schema(entity, config, "https://ex.com/p", "Post", "Desc", None)
        assert schema["@type"] == "Article"
