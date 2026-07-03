"""Tests for SEOPayload dataclass with dict compatibility."""

from seoslug.payload import OGPayload, SEOPayload, TwitterPayload


_OG_KW = dict(type="website", title="Test", description=None, url="https://ex.com", image="https://ex.com/img.jpg")
_TW_KW = dict(card="summary", title="Test", description=None, image="https://ex.com/img.jpg")


def test_seo_payload_attribute_access() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert p.title == "Test"
    assert p.canonical == "https://ex.com"
    assert p.og.title == "Test"
    assert p.twitter.card == "summary"
    assert p.og.image == "https://ex.com/img.jpg"


def test_seo_payload_dict_access() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert p["title"] == "Test"
    assert p["canonical"] == "https://ex.com"
    assert p["og"]["title"] == "Test"
    assert p["twitter"]["card"] == "summary"


def test_seo_payload_to_dict() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(card="summary", title="Test", description="Desc", image="https://ex.com/img.jpg")
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    d = p.to_dict()
    assert isinstance(d, dict)
    assert d["title"] == "Test"
    assert d["canonical"] == "https://ex.com"
    assert d["og"]["title"] == "Test"
    assert d["twitter"]["card"] == "summary"
    assert "schema_jsonld" not in d


def test_seo_payload_contains() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert "title" in p
    assert "schema_jsonld" not in p
    assert "og" in p
    assert "twitter" in p


def test_og_payload_to_dict_maps_colon_keys() -> None:
    og = OGPayload(
        type="article", title="Post", description=None, url="https://ex.com/p", image="https://ex.com/img.jpg",
        image_width=1200, image_height=630, image_alt="Hero",
        locale="en_US", locale_alternate=["es_ES"],
    )
    d = og.to_dict()
    assert d["image:width"] == 1200
    assert d["image:height"] == 630
    assert d["image:alt"] == "Hero"
    assert d["locale:alternate"] == ["es_ES"]
    assert d["type"] == "article"
    assert d["image"] == "https://ex.com/img.jpg"


def test_og_payload_dict_access_colon_keys() -> None:
    og = OGPayload(type="article", title="Post", description=None, url="https://ex.com/p", image="https://ex.com/img.jpg", image_width=1200)
    assert og["image:width"] == 1200
    assert og["image"] == "https://ex.com/img.jpg"
    assert "image:width" in og


def test_og_payload_none_values_excluded() -> None:
    og = OGPayload(**_OG_KW)
    assert "image:width" not in og
    assert "site_name" not in og
    assert og.get("site_name") is None


def test_twitter_payload_dict_access() -> None:
    tw = TwitterPayload(card="summary", title="Test", description=None, image="https://ex.com/img.jpg", image_alt="Alt")
    assert tw["image:alt"] == "Alt"
    assert "image:alt" in tw


def test_payload_equals_dict() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    expected = {
        "title": "Test",
        "canonical": "https://ex.com",
        "robots": "index,follow",
        "og": {"type": "website", "title": "Test", "url": "https://ex.com", "image": "https://ex.com/img.jpg"},
        "twitter": {"card": "summary", "title": "Test", "image": "https://ex.com/img.jpg"},
    }
    assert p == expected


def test_render_html_contains_title() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_html()
    assert "<title>Test</title>" in html
    assert 'name="description" content="Desc"' in html
    assert 'rel="canonical" href="https://ex.com"' in html
    assert 'name="robots" content="index,follow"' in html


def test_render_html_og_and_twitter_tags() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(card="summary", title="Test", description="Desc", image="https://ex.com/img.jpg")
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_html()
    assert 'property="og:type" content="website"' in html
    assert 'property="og:title" content="Test"' in html
    assert 'property="og:image" content="https://ex.com/img.jpg"' in html
    assert 'name="twitter:card" content="summary"' in html
    assert 'name="twitter:title" content="Test"' in html
    assert 'name="twitter:description" content="Desc"' in html


def test_render_html_schema_jsonld() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)
    p.schema_jsonld = {"@context": "https://schema.org", "@type": "Article", "name": "Test"}

    html = p.render_html()
    assert '<script type="application/ld+json">' in html
    assert '"@type": "Article"' in html
    assert '"name": "Test"' in html
    assert "</script>" in html


def test_render_html_escapes_values() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title='Test "Title"', description="Desc <script>", canonical="https://ex.com?a=1&b=2", robots="index,follow", og=og, twitter=tw)

    html = p.render_html()
    assert "&quot;Title&quot;" in html
    assert "&lt;script&gt;" in html
    assert "&amp;b=2" in html


def test_render_html_no_description_when_empty() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description="", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_html()
    assert "<title>Test</title>" in html
    assert 'name="description"' not in html


def test_render_html_no_schema_when_none() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_html()
    assert "application/ld+json" not in html


def test_hash_is_deterministic() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert p.hash() == p.hash()
    assert isinstance(p.hash(), str)
    assert len(p.hash()) == 64


def test_hash_differs_when_payload_differs() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p1 = SEOPayload(title="A", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)
    p2 = SEOPayload(title="B", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert p1.hash() != p2.hash()


def test_etag_format() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    etag = p.etag()
    assert etag.startswith('"')
    assert etag.endswith('"')
    assert len(etag) == 66  # 64 hex chars + 2 quotes


# -- Granular render helpers -- #


def test_render_opengraph_basic() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_opengraph()
    assert 'property="og:type" content="website"' in html
    assert 'property="og:title" content="Test"' in html
    assert 'property="og:image" content="https://ex.com/img.jpg"' in html


def test_render_opengraph_list_values() -> None:
    og = OGPayload(type="article", title="Post", description=None, url="https://ex.com/p", image="https://ex.com/img.jpg",
                   locale_alternate=["es_ES", "fr_FR"])
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_opengraph()
    assert 'property="og:locale:alternate" content="es_ES"' in html
    assert 'property="og:locale:alternate" content="fr_FR"' in html


def test_render_opengraph_omits_none_fields() -> None:
    og = OGPayload(type="website", title=None, description=None, url=None, image=None)
    tw = TwitterPayload(card="summary", title=None, description=None, image=None)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_opengraph()
    # type is always present; other None fields should be omitted
    assert 'property="og:type" content="website"' in html
    assert 'og:title' not in html
    assert 'og:image' not in html


def test_render_twitter_basic() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(card="summary_large_image", title="TwTitle", description="TwDesc", image="https://ex.com/tw.jpg")
    p = SEOPayload(title="Test", description="Desc", canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_twitter()
    assert 'name="twitter:card" content="summary_large_image"' in html
    assert 'name="twitter:title" content="TwTitle"' in html
    assert 'name="twitter:description" content="TwDesc"' in html
    assert 'name="twitter:image" content="https://ex.com/tw.jpg"' in html


def test_render_twitter_colon_key() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(card="summary", title="Test", description=None, image="https://ex.com/img.jpg", image_alt="Alt text")
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    html = p.render_twitter()
    assert 'name="twitter:image:alt" content="Alt text"' in html


def test_render_jsonld_basic() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)
    p.schema_jsonld = {"@context": "https://schema.org", "@type": "Article", "name": "Test"}

    html = p.render_jsonld()
    assert '<script type="application/ld+json">' in html
    assert '"@type": "Article"' in html
    assert '"name": "Test"' in html
    assert "</script>" in html


def test_render_jsonld_empty_when_none() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(**_TW_KW)
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert p.render_jsonld() == ""


def test_render_html_composition_matches_individual_methods() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(card="summary", title="Test", description="Desc", image="https://ex.com/img.jpg")
    p = SEOPayload(title="Test Title", description="Test Desc", canonical="https://ex.com/page", robots="index,follow", og=og, twitter=tw)
    p.schema_jsonld = {"@context": "https://schema.org", "@type": "Article"}

    full = p.render_html()
    assert "<title>Test Title</title>" in full
    assert p.render_opengraph() in full
    assert p.render_twitter() in full
    assert p.render_jsonld() in full


def test_render_helpers_escape_html() -> None:
    og = OGPayload(**_OG_KW)
    tw = TwitterPayload(card="summary", title='Title "X"', description='Desc <br>', image="https://ex.com/img.jpg")
    p = SEOPayload(title="Test", description=None, canonical="https://ex.com", robots="index,follow", og=og, twitter=tw)

    assert "&quot;X&quot;" in p.render_twitter()
    assert "&lt;br&gt;" in p.render_twitter()
