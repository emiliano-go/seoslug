"""Tests for SEOEntity and SEOOverrides models."""

import pytest

from seoslug import (
    Breadcrumb,
    FAQItem,
    OGImage,
    Robots,
    SEOConfig,
    SEOEntity,
    SEOEntityError,
    SEOOverrides,
    SchemaRegistry,
    URLPolicy,
    build_seo_payload,
)


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
    with pytest.raises(SEOEntityError):
        SEOEntity(entity_type="invalid")


def test_entity_rejects_non_string_optional_field() -> None:
    with pytest.raises(SEOEntityError):
        SEOEntity(entity_type="post", title=123)  # type: ignore[arg-type]


def test_overrides_normalize_and_validate_schema_type() -> None:
    overrides = SEOOverrides(meta_title="  A ", robots="  ")
    assert overrides.meta_title == "A"
    assert overrides.robots is None

    with pytest.raises(SEOEntityError):
        SEOOverrides(schema_jsonld=[{"@type": "WebPage"}, "bad"])  # type: ignore[list-item]


# --- canonical_host validation (issue #2) ---

def _valid_config(**kw) -> SEOConfig:
    defaults = dict(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    defaults.update(kw)
    return SEOConfig(**defaults)


def test_canonical_host_rejects_port() -> None:
    with pytest.raises(ValueError, match="host-only"):
        _valid_config(canonical_host="example.com:8080")


def test_canonical_host_rejects_trailing_dot() -> None:
    with pytest.raises(ValueError, match="trailing dot"):
        _valid_config(canonical_host="example.com.")


def test_canonical_host_rejects_ipv6() -> None:
    with pytest.raises(ValueError, match="IPv6"):
        _valid_config(canonical_host="[::1]")


def test_canonical_host_rejects_scheme() -> None:
    with pytest.raises(ValueError, match="host-only"):
        _valid_config(canonical_host="https://example.com")


def test_canonical_host_rejects_path() -> None:
    with pytest.raises(ValueError, match="host-only"):
        _valid_config(canonical_host="example.com/path")


def test_canonical_host_valid_examples() -> None:
    for host in ["example.com", "blog.example.com", "localhost", "127.0.0.1"]:
        config = _valid_config(canonical_host=host)
        assert config.canonical_host == host


# --- skip_title_template (issue #6) ---

def test_skip_title_template_bypasses_template() -> None:
    entity = SEOEntity(entity_type="page", title="About")
    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
        title_template="{title} | My Site",
    )
    payload = build_seo_payload(entity, "/about", config, SEOOverrides(skip_title_template=True))
    assert payload["title"] == "About"


# --- New dataclass: OGImage ---

def test_og_image_basic() -> None:
    img = OGImage(url="https://example.com/img.jpg")
    assert img.url == "https://example.com/img.jpg"
    assert img.width is None
    assert img.height is None
    assert img.alt is None


def test_og_image_full() -> None:
    img = OGImage(url="https://example.com/img.jpg", width=1200, height=630, alt="Hero")
    assert img.width == 1200
    assert img.height == 630
    assert img.alt == "Hero"


def test_og_image_rejects_empty_url() -> None:
    with pytest.raises(ValueError, match="OGImage.url"):
        OGImage(url="")


def test_entity_accepts_og_image_featured() -> None:
    img = OGImage(url="https://example.com/img.jpg", width=800, alt="Desc")
    entity = SEOEntity(entity_type="post", featured_image=img)
    assert isinstance(entity.featured_image, OGImage)
    assert entity.featured_image.url == "https://example.com/img.jpg"
    assert entity.featured_image.width == 800
    assert entity.featured_image.alt == "Desc"


def test_entity_featured_image_string_still_works() -> None:
    entity = SEOEntity(entity_type="post", featured_image=" https://example.com/img.jpg ")
    assert entity.featured_image == "https://example.com/img.jpg"


def test_overrides_accepts_og_image() -> None:
    img = OGImage(url="https://ex.com/og.jpg", width=1200)
    ov = SEOOverrides(og_image=img)
    assert isinstance(ov.og_image, OGImage)
    assert ov.og_image.width == 1200


def test_overrides_accepts_string_og_image() -> None:
    ov = SEOOverrides(og_image="https://ex.com/og.jpg")
    assert ov.og_image == "https://ex.com/og.jpg"


# --- New dataclass: Breadcrumb ---

def test_breadcrumb_basic() -> None:
    bc = Breadcrumb(name="Blog", url="/blog")
    assert bc.name == "Blog"
    assert bc.url == "/blog"


def test_breadcrumb_rejects_empty_name() -> None:
    with pytest.raises(ValueError, match="Breadcrumb.name"):
        Breadcrumb(name="", url="/x")


def test_breadcrumb_rejects_empty_url() -> None:
    with pytest.raises(ValueError, match="Breadcrumb.url"):
        Breadcrumb(name="X", url="")


def test_entity_accepts_breadcrumbs() -> None:
    bcs = [Breadcrumb(name="Home", url="/"), Breadcrumb(name="Blog", url="/blog")]
    entity = SEOEntity(entity_type="page", breadcrumbs=bcs)
    assert len(entity.breadcrumbs) == 2
    assert entity.breadcrumbs[0].name == "Home"


# --- New dataclass: FAQItem ---

def test_faq_item_basic() -> None:
    item = FAQItem(question="Q?", answer="A.")
    assert item.question == "Q?"
    assert item.answer == "A."


def test_faq_item_rejects_empty() -> None:
    with pytest.raises(ValueError, match="FAQItem.question"):
        FAQItem(question="", answer="A")
    with pytest.raises(ValueError, match="FAQItem.answer"):
        FAQItem(question="Q", answer="")


def test_entity_accepts_faq_items() -> None:
    items = [FAQItem(question="Q1", answer="A1")]
    entity = SEOEntity(entity_type="faq", faq_items=items)
    assert len(entity.faq_items) == 1


# --- New dataclass: Robots ---

def test_robots_default_serialize() -> None:
    assert Robots().serialize() == "index,follow"


def test_robots_noindex_nofollow() -> None:
    assert Robots(index=False, follow=False).serialize() == "noindex,nofollow"


def test_robots_with_max_snippet() -> None:
    assert Robots(max_snippet=-1).serialize() == "index,follow,max-snippet:-1"


def test_robots_with_image_preview() -> None:
    assert Robots(max_image_preview="large").serialize() == "index,follow,max-image-preview:large"


def test_robots_all_options() -> None:
    r = Robots(index=True, follow=False, max_snippet=100, max_image_preview="standard", max_video_preview=-1)
    assert r.serialize() == "index,nofollow,max-snippet:100,max-image-preview:standard,max-video-preview:-1"


def test_overrides_accepts_robots_object() -> None:
    ov = SEOOverrides(robots=Robots(index=False))
    assert isinstance(ov.robots, Robots)
    assert ov.robots.serialize() == "noindex,follow"


def test_overrides_accepts_robots_string() -> None:
    ov = SEOOverrides(robots="noindex,nofollow")
    assert ov.robots == "noindex,nofollow"


# --- New entity types ---

def test_entity_accepts_product_type() -> None:
    entity = SEOEntity(entity_type="product", title="Widget")
    assert entity.entity_type == "product"


def test_entity_accepts_organization_type() -> None:
    entity = SEOEntity(entity_type="organization", title="Acme")
    assert entity.entity_type == "organization"


def test_entity_accepts_local_business_type() -> None:
    entity = SEOEntity(entity_type="local_business", title="Shop")
    assert entity.entity_type == "local_business"


def test_entity_accepts_faq_type() -> None:
    entity = SEOEntity(entity_type="faq", title="FAQ")
    assert entity.entity_type == "faq"


# --- New SEOEntity fields ---

def test_entity_new_ecommerce_fields() -> None:
    entity = SEOEntity(
        entity_type="product",
        sku="WIDG-001",
        price="29.99",
        price_currency="USD",
        availability="InStock",
    )
    assert entity.sku == "WIDG-001"
    assert entity.price == "29.99"
    assert entity.price_currency == "USD"
    assert entity.availability == "InStock"


def test_entity_same_as_normalizes() -> None:
    entity = SEOEntity(
        entity_type="organization",
        same_as=[" https://twitter.com/acme ", "https://fb.me/acme", ""],
    )
    assert entity.same_as == ["https://twitter.com/acme", "https://fb.me/acme"]


def test_entity_same_as_empty_becomes_none() -> None:
    entity = SEOEntity(entity_type="organization", same_as=[])
    assert entity.same_as is None


def test_entity_address() -> None:
    entity = SEOEntity(entity_type="local_business", address="123 Main St")
    assert entity.address == "123 Main St"


def test_entity_normalizes_sku_price() -> None:
    entity = SEOEntity(entity_type="product", sku="  ABC  ", price="  10.00  ")
    assert entity.sku == "ABC"
    assert entity.price == "10.00"


# --- New SEOOverrides fields ---

def test_overrides_twitter_creator() -> None:
    ov = SEOOverrides(twitter_creator="@janedoe")
    assert ov.twitter_creator == "@janedoe"


def test_overrides_og_audio_video() -> None:
    ov = SEOOverrides(og_audio="https://ex.com/audio.mp3", og_video="https://ex.com/vid.mp4")
    assert ov.og_audio == "https://ex.com/audio.mp3"
    assert ov.og_video == "https://ex.com/vid.mp4"


def test_overrides_normalizes_new_string_fields() -> None:
    ov = SEOOverrides(twitter_creator="  @joe  ")
    assert ov.twitter_creator == "@joe"


# --- SEOConfig new fields ---

def test_config_locale() -> None:
    config = SEOConfig(canonical_host="ex.com", public_base_url="https://ex.com", url_policy=URLPolicy(), locale="en_US")
    assert config.locale == "en_US"


def test_config_locale_alternate() -> None:
    config = SEOConfig(canonical_host="ex.com", public_base_url="https://ex.com", url_policy=URLPolicy(), locale_alternate=["es_ES", "fr_FR"])
    assert config.locale_alternate == ["es_ES", "fr_FR"]


def test_config_twitter_site() -> None:
    config = SEOConfig(canonical_host="ex.com", public_base_url="https://ex.com", url_policy=URLPolicy(), twitter_site="@mysite")
    assert config.twitter_site == "@mysite"


def test_config_accepts_robots_object_for_default() -> None:
    config = SEOConfig(canonical_host="ex.com", public_base_url="https://ex.com", url_policy=URLPolicy(), default_robots=Robots(index=False))
    assert isinstance(config.default_robots, Robots)


def test_config_accepts_robots_object_for_search() -> None:
    config = SEOConfig(canonical_host="ex.com", public_base_url="https://ex.com", url_policy=URLPolicy(), search_robots=Robots(index=False, follow=False))
    assert isinstance(config.search_robots, Robots)


def test_config_accepts_og_image_for_default() -> None:
    img = OGImage(url="https://ex.com/default.jpg", width=1200)
    config = SEOConfig(canonical_host="ex.com", public_base_url="https://ex.com", url_policy=URLPolicy(), default_og_image=img)
    assert isinstance(config.default_og_image, OGImage)


def test_config_emit_warnings_default() -> None:
    config = _valid_config()
    assert config.emit_warnings is False


# --- SchemaRegistry ---

def test_registry_register_and_get() -> None:
    from seoslug import SchemaRegistry
    registry = SchemaRegistry()
    def my_gen(*a, **kw): return None
    registry.register("Podcast", my_gen)
    assert registry.get("Podcast") is my_gen


def test_registry_unregister() -> None:
    from seoslug import SchemaRegistry
    registry = SchemaRegistry()
    def my_gen(*a, **kw): return None
    registry.register("X", my_gen)
    registry.unregister("X")
    assert registry.get("X") is None


def test_registry_rejects_empty_type() -> None:
    from seoslug import SchemaRegistry
    registry = SchemaRegistry()
    with pytest.raises(ValueError, match="schema_type"):
        registry.register("", lambda *a, **kw: None)


# --- SEOEntityBuilder ---

def test_entity_builder_basic() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").title("My Post").build()
    assert entity.entity_type == "post"
    assert entity.title == "My Post"


def test_entity_builder_full() -> None:
    from seoslug import Breadcrumb, FAQItem, OGImage, SEOEntityBuilder
    entity = (
        SEOEntityBuilder()
        .entity_type("product")
        .title("Widget")
        .sku("W-001")
        .price(29.99)
        .price_currency("USD")
        .availability("InStock")
        .featured_image(OGImage(url="https://ex.com/img.jpg", width=800))
        .breadcrumbs([Breadcrumb(name="Home", url="/")])
        .faq_items([FAQItem(question="Q?", answer="A.")])
        .build()
    )
    assert entity.entity_type == "product"
    assert entity.sku == "W-001"
    assert entity.price == "29.99"
    assert entity.featured_image.width == 800


def test_entity_builder_requires_entity_type() -> None:
    from seoslug import SEOEntityBuilder
    import pytest
    with pytest.raises(ValueError, match="entity_type"):
        SEOEntityBuilder().build()





# ── Normalization helper coverage ──────────────────────────────────────────


def test_normalize_image_empty_ogimage_url_raises_valueerror() -> None:
    import pytest
    from seoslug.schemas import _normalize_image, OGImage
    img = object.__new__(OGImage)
    object.__setattr__(img, "url", "")
    object.__setattr__(img, "width", None)
    object.__setattr__(img, "height", None)
    object.__setattr__(img, "alt", None)
    with pytest.raises(ValueError, match="OGImage.url must be non-empty"):
        _normalize_image(img, "test_field")


def test_normalize_image_invalid_type_raises_valueerror() -> None:
    import pytest
    from seoslug.schemas import _normalize_image
    with pytest.raises(ValueError, match="must be a string, OGImage, or None"):
        _normalize_image(42, "test_field")  # type: ignore[arg-type]


def test_normalize_robots_invalid_type_raises_valueerror() -> None:
    import pytest
    from seoslug.schemas import _normalize_robots
    with pytest.raises(ValueError, match="must be a string, Robots, or None"):
        _normalize_robots(42, "test_field")  # type: ignore[arg-type]


def test_normalize_string_list_non_list_raises_valueerror() -> None:
    import pytest
    from seoslug.schemas import _normalize_string_list
    with pytest.raises(ValueError, match="must be a list or None"):
        _normalize_string_list("not a list", "test_field")  # type: ignore[arg-type]


# ── SEOEntityBuilder additional method coverage ────────────────────────────


def test_entity_builder_slug() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").slug("  my-slug  ").build()
    assert entity.slug == "my-slug"


def test_entity_builder_excerpt() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").excerpt("  Short desc  ").build()
    assert entity.excerpt == "Short desc"


def test_entity_builder_body_html() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").body_html("<p>Hello</p>").build()
    assert entity.body_html == "<p>Hello</p>"


def test_entity_builder_status() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").status("published").build()
    assert entity.status == "published"


def test_entity_builder_published_at() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").published_at("2024-01-01").build()
    assert entity.published_at == "2024-01-01"


def test_entity_builder_updated_at() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").updated_at("2024-06-01").build()
    assert entity.updated_at == "2024-06-01"


def test_entity_builder_author_name() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("post").author_name("  Jane Doe  ").build()
    assert entity.author_name == "Jane Doe"


def test_entity_builder_same_as() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("organization").same_as(
        ["https://twitter.com/acme", "https://fb.me/acme"]
    ).build()
    assert entity.same_as == ["https://twitter.com/acme", "https://fb.me/acme"]


def test_entity_builder_address() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("local_business").address("123 Main St").build()
    assert entity.address == "123 Main St"


def test_entity_builder_breadcrumbs() -> None:
    from seoslug import Breadcrumb, SEOEntityBuilder
    bcs = [Breadcrumb(name="Home", url="/"), Breadcrumb(name="Blog", url="/blog")]
    entity = SEOEntityBuilder().entity_type("page").breadcrumbs(bcs).build()
    assert len(entity.breadcrumbs) == 2
    assert entity.breadcrumbs[0].name == "Home"


def test_entity_builder_faq_items() -> None:
    from seoslug import FAQItem, SEOEntityBuilder
    items = [FAQItem(question="Q?", answer="A.")]
    entity = SEOEntityBuilder().entity_type("faq").faq_items(items).build()
    assert len(entity.faq_items) == 1
    assert entity.faq_items[0].question == "Q?"


def test_entity_builder_price_float_converts_to_str() -> None:
    from seoslug import SEOEntityBuilder
    entity = SEOEntityBuilder().entity_type("product").price(29.99).build()
    assert entity.price == "29.99"


def test_entity_builder_returns_self() -> None:
    from seoslug import SEOEntityBuilder
    builder = SEOEntityBuilder()
    assert builder.entity_type("post") is builder
    assert builder.title("T") is builder
    assert builder.slug("s") is builder
    assert builder.excerpt("e") is builder
    assert builder.body_html("b") is builder
    assert builder.status("pub") is builder
    assert builder.author_name("a") is builder
    assert builder.published_at("2024") is builder
    assert builder.updated_at("2024") is builder
    assert builder.sku("SKU") is builder
    assert builder.price_currency("USD") is builder
    assert builder.availability("InStock") is builder
    assert builder.breadcrumbs([]) is builder
    assert builder.same_as([]) is builder
    assert builder.address("addr") is builder
    assert builder.faq_items([]) is builder


# ── SEOOverrides schema_jsonld validation ──────────────────────────────────


def test_overrides_invalid_schema_jsonld_type() -> None:
    import pytest
    with pytest.raises(SEOEntityError, match="schema_jsonld"):
        SEOOverrides(schema_jsonld="bad")  # type: ignore[arg-type]
