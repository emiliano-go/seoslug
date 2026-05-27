"""Tests for SEO payload builder."""

from seoslug import SEOConfig, SEOEntity, SEOOverrides, URLPolicy, build_seo_payload


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
