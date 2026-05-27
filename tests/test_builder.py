"""Tests for SEO payload builder."""

from seoslug import SEOConfig, SEOEntity, SEOOverrides, URLPolicy, build_seo_payload


def _config() -> SEOConfig:
    return SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        default_og_image="https://cdn.example.com/default.jpg",
        site_name="Portal",
        title_template="{title}",
    )


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


def test_canonical_override_and_schema_passthrough() -> None:
    entity = SEOEntity(entity_type="page", title="About")
    overrides = SEOOverrides(
        canonical_url="https://portal.example.com/custom-about",
        schema_jsonld={"@context": "https://schema.org", "@type": "WebPage"},
    )
    payload = build_seo_payload(entity, "/about", _config(), overrides)
    assert payload["canonical"] == "https://portal.example.com/custom-about"
    assert payload["schema_jsonld"]["@type"] == "WebPage"


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


def test_schema_list_passthrough() -> None:
    entity = SEOEntity(entity_type="page", title="Docs")
    schema = [{"@type": "BreadcrumbList"}, {"@type": "WebPage"}]
    payload = build_seo_payload(entity, "/docs", _config(), SEOOverrides(schema_jsonld=schema))
    assert payload["schema_jsonld"] == schema
