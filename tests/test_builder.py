"""Tests for SEO payload builder."""

from seoslug import Breadcrumb, OGImage, Robots, SEOConfig, SEOEntity, SEOOverrides, URLPolicy, build_seo_payload


def _config(**kwargs) -> SEOConfig:
    defaults = dict(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        default_og_image="https://cdn.example.com/default.jpg",
        site_name="Portal",
        title_template="{title}",
    )
    defaults.update(kwargs)
    return SEOConfig(**defaults)


def test_payload_contract_shape() -> None:
    entity = SEOEntity(
        entity_type="post",
        slug="my-post",
        title="My Post",
        excerpt="Example excerpt",
        body_html="<p>Body</p>",
        status="published",
        featured_image="https://cdn.example.com/post.jpg",
    )
    payload = build_seo_payload(entity, "/posts/my-post", _config())

    assert set(payload.keys()) == {
        "title",
        "description",
        "canonical",
        "robots",
        "og",
        "twitter",
        "schema_jsonld",
    }
    assert payload["canonical"] == "https://portal.example.com/posts/my-post"
    assert payload["og"]["url"] == payload["canonical"]
    assert payload["og"]["site_name"] == "Portal"
    assert payload["twitter"]["card"] == "summary_large_image"
    assert payload["schema_jsonld"]["@type"] == "Article"


def test_canonical_override_and_schema_passthrough() -> None:
    entity = SEOEntity(entity_type="page", title="About")
    overrides = SEOOverrides(
        canonical_url="https://portal.example.com/custom-about",
        schema_jsonld={"@context": "https://schema.org", "@type": "WebPage"},
    )
    payload = build_seo_payload(entity, "/about", _config(), overrides)
    assert payload["canonical"] == "https://portal.example.com/custom-about"
    assert payload["schema_jsonld"]["@type"] == "WebPage"


def test_schema_list_passthrough() -> None:
    entity = SEOEntity(entity_type="page", title="Docs")
    schema = [{"@type": "BreadcrumbList"}, {"@type": "WebPage"}]
    payload = build_seo_payload(entity, "/docs", _config(), SEOOverrides(schema_jsonld=schema))
    assert payload["schema_jsonld"] == schema


def test_omit_schema_flag_removes_key() -> None:
    entity = SEOEntity(entity_type="post", title="Post")
    overrides = SEOOverrides(omit_schema=True)
    payload = build_seo_payload(entity, "/post", _config(), overrides)
    assert "schema_jsonld" not in payload


def test_omit_schema_flag_still_applies_when_override_given() -> None:
    entity = SEOEntity(entity_type="post", title="Post")
    overrides = SEOOverrides(omit_schema=True, schema_jsonld={"@type": "Product"})
    payload = build_seo_payload(entity, "/post", _config(), overrides)
    assert "schema_jsonld" not in payload


def test_auto_generate_schema_false_omits_key() -> None:
    entity = SEOEntity(entity_type="post", title="Post")
    payload = build_seo_payload(entity, "/post", _config(auto_generate_schema=False))
    assert "schema_jsonld" not in payload


def test_auto_generate_schema_still_allows_override() -> None:
    entity = SEOEntity(entity_type="post", title="Post")
    overrides = SEOOverrides(schema_jsonld={"@type": "Product"})
    payload = build_seo_payload(entity, "/post", _config(auto_generate_schema=False), overrides)
    assert payload["schema_jsonld"]["@type"] == "Product"


def test_unmapped_entity_type_skips_schema() -> None:
    config = _config(schema_type_map={})
    entity = SEOEntity(entity_type="post", title="Post")
    payload = build_seo_payload(entity, "/post", config)
    assert "schema_jsonld" not in payload


def test_author_injected_into_auto_schema() -> None:
    entity = SEOEntity(entity_type="post", title="Post", author_name="Jane Doe")
    payload = build_seo_payload(entity, "/post", _config())
    assert payload["schema_jsonld"]["author"] == {"@type": "Person", "name": "Jane Doe"}


def test_publisher_injected_into_auto_schema() -> None:
    entity = SEOEntity(entity_type="post", title="Post")
    config = _config(publisher_name="Acme Corp", publisher_logo="https://example.com/logo.png")
    payload = build_seo_payload(entity, "/post", config)
    assert payload["schema_jsonld"]["publisher"] == {
        "@type": "Organization",
        "name": "Acme Corp",
        "logo": "https://example.com/logo.png",
    }


def test_twitter_override_precedence() -> None:
    entity = SEOEntity(entity_type="post", title="Entity Title", excerpt="Entity Excerpt")
    overrides = SEOOverrides(
        og_title="OG Title",
        twitter_title="Twitter Title",
        twitter_description="Twitter Description",
    )
    payload = build_seo_payload(entity, "/posts/t", _config(), overrides)
    assert payload["og"]["title"] == "OG Title"
    assert payload["twitter"]["title"] == "Twitter Title"
    assert payload["twitter"]["description"] == "Twitter Description"


def test_title_template_is_applied() -> None:
    config = SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        title_template="{title} | Portal",
    )
    payload = build_seo_payload(SEOEntity(entity_type="page", title="About"), "/about", config)
    assert payload["title"] == "About | Portal"


def test_description_prefers_excerpt_over_body_snippet() -> None:
    entity = SEOEntity(
        entity_type="post",
        excerpt="Excerpt text",
        body_html="<p>Body fallback text</p>",
    )
    payload = build_seo_payload(entity, "/posts/p", _config())
    assert payload["description"] == "Excerpt text"


def test_sub_path_deployment_canonical() -> None:
    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com/blog",
        url_policy=URLPolicy(),
    )
    entity = SEOEntity(entity_type="page", title="About")
    payload = build_seo_payload(entity, "/about", config)
    assert payload["canonical"] == "https://example.com/blog/about"
    assert payload["og"]["url"] == "https://example.com/blog/about"


def test_sub_path_deployment_home_route() -> None:
    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com/blog/",
        url_policy=URLPolicy(),
    )
    entity = SEOEntity(entity_type="home", title="Home")
    payload = build_seo_payload(entity, "/", config)
    assert payload["canonical"] == "https://example.com/blog"


def test_twitter_falls_back_to_og_values() -> None:
    entity = SEOEntity(entity_type="post", title="Entity")
    overrides = SEOOverrides(
        og_title="OG T",
        og_description="OG D",
        og_image="https://cdn.example.com/og.jpg",
    )
    payload = build_seo_payload(entity, "/posts/p", _config(), overrides)
    assert payload["twitter"]["title"] == "OG T"
    assert payload["twitter"]["description"] == "OG D"
    assert payload["twitter"]["image"] == "https://cdn.example.com/og.jpg"


# --- OGImage structured ---

def test_og_image_with_dimensions() -> None:
    img = OGImage(url="https://cdn.example.com/hero.jpg", width=1200, height=630, alt="Hero")
    entity = SEOEntity(entity_type="post", title="Post", featured_image=img)
    payload = build_seo_payload(entity, "/post", _config())
    assert payload["og"]["image"] == "https://cdn.example.com/hero.jpg"
    assert payload["og"]["image:width"] == 1200
    assert payload["og"]["image:height"] == 630
    assert payload["og"]["image:alt"] == "Hero"


def test_og_image_string_still_works() -> None:
    entity = SEOEntity(entity_type="post", title="Post", featured_image="https://cdn.example.com/img.jpg")
    payload = build_seo_payload(entity, "/post", _config())
    assert payload["og"]["image"] == "https://cdn.example.com/img.jpg"
    assert "image:width" not in payload["og"]


def test_twitter_image_alt_from_og_image() -> None:
    img = OGImage(url="https://ex.com/img.jpg", alt="Alt text")
    entity = SEOEntity(entity_type="post", title="Post", featured_image=img)
    payload = build_seo_payload(entity, "/post", _config())
    assert payload["twitter"]["image"] == "https://ex.com/img.jpg"
    assert payload["twitter"]["image:alt"] == "Alt text"


def test_og_image_override_structured() -> None:
    img = OGImage(url="https://ex.com/og.jpg", width=800)
    ov = SEOOverrides(og_image=img)
    entity = SEOEntity(entity_type="post", title="Post")
    payload = build_seo_payload(entity, "/post", _config(), ov)
    assert payload["og"]["image"] == "https://ex.com/og.jpg"
    assert payload["og"]["image:width"] == 800


# --- Breadcrumb auto-generation ---

def test_breadcrumbs_appended_to_schema() -> None:
    entity = SEOEntity(
        entity_type="post", title="Post", status="published",
        breadcrumbs=[Breadcrumb(name="Home", url="/"), Breadcrumb(name="Blog", url="/blog")],
    )
    payload = build_seo_payload(entity, "/posts/my-post", _config())
    assert isinstance(payload["schema_jsonld"], list)
    assert len(payload["schema_jsonld"]) == 2
    assert payload["schema_jsonld"][0]["@type"] == "Article"
    assert payload["schema_jsonld"][1]["@type"] == "BreadcrumbList"


def test_breadcrumbs_with_override_schema() -> None:
    entity = SEOEntity(
        entity_type="page", title="Page",
        breadcrumbs=[Breadcrumb(name="Home", url="/")],
    )
    ov = SEOOverrides(schema_jsonld={"@type": "WebPage"})
    payload = build_seo_payload(entity, "/page", _config(), ov)
    assert isinstance(payload["schema_jsonld"], list)
    assert len(payload["schema_jsonld"]) == 2
    assert payload["schema_jsonld"][0]["@type"] == "WebPage"


def test_breadcrumbs_omit_schema_still_adds_breadcrumbs() -> None:
    entity = SEOEntity(
        entity_type="page", title="Page",
        breadcrumbs=[Breadcrumb(name="Home", url="/")],
    )
    ov = SEOOverrides(omit_schema=True)
    payload = build_seo_payload(entity, "/page", _config(), ov)
    assert payload["schema_jsonld"]["@type"] == "BreadcrumbList"


def test_no_schema_no_breadcrumbs_omits_key() -> None:
    entity = SEOEntity(entity_type="other", title="Other")
    payload = build_seo_payload(entity, "/other", _config())
    assert "schema_jsonld" not in payload


# --- Social metadata ---

def test_locale_in_og() -> None:
    config = _config(locale="en_US")
    entity = SEOEntity(entity_type="page", title="Page")
    payload = build_seo_payload(entity, "/page", config)
    assert payload["og"]["locale"] == "en_US"


def test_locale_alternate_in_og() -> None:
    config = _config(locale_alternate=["es_ES", "fr_FR"])
    entity = SEOEntity(entity_type="page", title="Page")
    payload = build_seo_payload(entity, "/page", config)
    assert payload["og"]["locale:alternate"] == ["es_ES", "fr_FR"]


def test_twitter_site() -> None:
    config = _config(twitter_site="@mysite")
    entity = SEOEntity(entity_type="page", title="Page")
    payload = build_seo_payload(entity, "/page", config)
    assert payload["twitter"]["site"] == "@mysite"


def test_twitter_creator() -> None:
    ov = SEOOverrides(twitter_creator="@janedoe")
    entity = SEOEntity(entity_type="post", title="Post")
    payload = build_seo_payload(entity, "/post", _config(), ov)
    assert payload["twitter"]["creator"] == "@janedoe"


def test_og_audio_video() -> None:
    ov = SEOOverrides(og_audio="https://ex.com/a.mp3", og_video="https://ex.com/v.mp4")
    entity = SEOEntity(entity_type="page", title="Page")
    payload = build_seo_payload(entity, "/page", _config(), ov)
    assert payload["og"]["audio"] == "https://ex.com/a.mp3"
    assert payload["og"]["video"] == "https://ex.com/v.mp4"


# --- Robots structured ---

def test_robots_object_in_default_serialized() -> None:
    config = _config(default_robots=Robots(index=False, follow=False))
    entity = SEOEntity(entity_type="page", title="Page", status="draft")
    payload = build_seo_payload(entity, "/page", config)
    assert payload["robots"] == "noindex,nofollow"


def test_robots_object_in_override_serialized() -> None:
    ov = SEOOverrides(robots=Robots(index=True, follow=False))
    entity = SEOEntity(entity_type="post", title="Post")
    payload = build_seo_payload(entity, "/post", _config(), ov)
    assert payload["robots"] == "index,nofollow"


def test_robots_string_still_works() -> None:
    ov = SEOOverrides(robots="noindex,nofollow")
    entity = SEOEntity(entity_type="post", title="Post")
    payload = build_seo_payload(entity, "/post", _config(), ov)
    assert payload["robots"] == "noindex,nofollow"


# --- Product schema end-to-end ---

def test_product_schema_in_payload() -> None:
    entity = SEOEntity(
        entity_type="product", title="Widget", status="published",
        sku="W-001", price="29.99", price_currency="USD", availability="InStock",
    )
    payload = build_seo_payload(entity, "/products/widget", _config())
    assert payload["og"]["type"] == "website"
    assert payload["schema_jsonld"]["@type"] == "Product"
    assert payload["schema_jsonld"]["sku"] == "W-001"
    assert payload["schema_jsonld"]["offers"]["price"] == "29.99"


# --- FAQPage schema end-to-end ---

def test_faq_schema_in_payload() -> None:
    from seoslug import FAQItem
    entity = SEOEntity(
        entity_type="faq", title="FAQ", status="published",
        faq_items=[FAQItem(question="Q?", answer="A.")],
    )
    payload = build_seo_payload(entity, "/faq", _config())
    assert payload["schema_jsonld"]["@type"] == "FAQPage"
    assert len(payload["schema_jsonld"]["mainEntity"]) == 1


# --- build_seo_payload_dict ---

def test_build_seo_payload_dict_returns_plain_dict() -> None:
    from seoslug import build_seo_payload_dict
    entity = SEOEntity(entity_type="page", title="About")
    d = build_seo_payload_dict(entity, "/about", _config())
    assert isinstance(d, dict)
    assert d["title"] == "About"
    assert d["canonical"] == "https://portal.example.com/about"


def test_build_seo_payload_dict_matches_to_dict() -> None:
    from seoslug import build_seo_payload_dict
    entity = SEOEntity(entity_type="post", title="Post", excerpt="Desc")
    d = build_seo_payload_dict(entity, "/post", _config())
    p = build_seo_payload(entity, "/post", _config())
    assert d == p.to_dict()
