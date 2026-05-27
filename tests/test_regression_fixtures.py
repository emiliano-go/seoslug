"""Regression fixtures for representative entity types."""

from seoslug import SEOConfig, SEOEntity, URLPolicy, build_seo_payload


def _config() -> SEOConfig:
    return SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        default_og_image="https://cdn.example.com/default.jpg",
        search_robots="noindex,follow",
    )


def test_regression_entity_type_fixtures() -> None:
    fixtures = [
        ("home", "/", "index,follow", "website"),
        ("post", "/posts/p", "index,follow", "article"),
        ("page", "/about", "index,follow", "website"),
        ("video", "/videos/v", "index,follow", "article"),
        ("taxonomy", "/topics/python", "index,follow", "website"),
        ("search", "/search?q=x", "noindex,follow", "website"),
    ]

    for entity_type, route, robots, og_type in fixtures:
        entity = SEOEntity(
            entity_type=entity_type,
            title=f"{entity_type} title",
            excerpt=f"{entity_type} excerpt",
            status="published",
        )
        payload = build_seo_payload(entity, route, _config())
        assert payload["title"] == f"{entity_type} title"
        assert payload["description"] == f"{entity_type} excerpt"
        assert payload["canonical"].startswith("https://portal.example.com")
        assert payload["robots"] == robots
        assert payload["og"]["type"] == og_type
        assert payload["twitter"]["card"] == "summary_large_image"
