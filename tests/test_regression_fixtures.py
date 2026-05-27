"""Regression fixtures for representative entity types."""

import pytest

from seoslug import SEOConfig, SEOEntity, URLPolicy, build_seo_payload


def _config() -> SEOConfig:
    return SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=URLPolicy(),
        default_og_image="https://cdn.example.com/default.jpg",
        search_robots="noindex,follow",
    )


@pytest.mark.parametrize(
    ("entity_type", "route", "expected"),
    [
        (
            "home",
            "/",
            {
                "title": "home title",
                "description": "home excerpt",
                "canonical": "https://portal.example.com/",
                "robots": "index,follow",
                "og": {
                    "type": "website",
                    "title": "home title",
                    "description": "home excerpt",
                    "url": "https://portal.example.com/",
                    "image": "https://cdn.example.com/default.jpg",
                },
                "twitter": {
                    "card": "summary_large_image",
                    "title": "home title",
                    "description": "home excerpt",
                    "image": "https://cdn.example.com/default.jpg",
                },
            },
        ),
        (
            "post",
            "/posts/p",
            {
                "title": "post title",
                "description": "post excerpt",
                "canonical": "https://portal.example.com/posts/p",
                "robots": "index,follow",
                "og": {
                    "type": "article",
                    "title": "post title",
                    "description": "post excerpt",
                    "url": "https://portal.example.com/posts/p",
                    "image": "https://cdn.example.com/default.jpg",
                },
                "twitter": {
                    "card": "summary_large_image",
                    "title": "post title",
                    "description": "post excerpt",
                    "image": "https://cdn.example.com/default.jpg",
                },
            },
        ),
        (
            "page",
            "/about",
            {
                "title": "page title",
                "description": "page excerpt",
                "canonical": "https://portal.example.com/about",
                "robots": "index,follow",
                "og": {
                    "type": "website",
                    "title": "page title",
                    "description": "page excerpt",
                    "url": "https://portal.example.com/about",
                    "image": "https://cdn.example.com/default.jpg",
                },
                "twitter": {
                    "card": "summary_large_image",
                    "title": "page title",
                    "description": "page excerpt",
                    "image": "https://cdn.example.com/default.jpg",
                },
            },
        ),
        (
            "video",
            "/videos/v",
            {
                "title": "video title",
                "description": "video excerpt",
                "canonical": "https://portal.example.com/videos/v",
                "robots": "index,follow",
                "og": {
                    "type": "article",
                    "title": "video title",
                    "description": "video excerpt",
                    "url": "https://portal.example.com/videos/v",
                    "image": "https://cdn.example.com/default.jpg",
                },
                "twitter": {
                    "card": "summary_large_image",
                    "title": "video title",
                    "description": "video excerpt",
                    "image": "https://cdn.example.com/default.jpg",
                },
            },
        ),
        (
            "taxonomy",
            "/topics/python",
            {
                "title": "taxonomy title",
                "description": "taxonomy excerpt",
                "canonical": "https://portal.example.com/topics/python",
                "robots": "index,follow",
                "og": {
                    "type": "website",
                    "title": "taxonomy title",
                    "description": "taxonomy excerpt",
                    "url": "https://portal.example.com/topics/python",
                    "image": "https://cdn.example.com/default.jpg",
                },
                "twitter": {
                    "card": "summary_large_image",
                    "title": "taxonomy title",
                    "description": "taxonomy excerpt",
                    "image": "https://cdn.example.com/default.jpg",
                },
            },
        ),
        (
            "search",
            "/search?q=x",
            {
                "title": "search title",
                "description": "search excerpt",
                "canonical": "https://portal.example.com/search?q=x",
                "robots": "noindex,follow",
                "og": {
                    "type": "website",
                    "title": "search title",
                    "description": "search excerpt",
                    "url": "https://portal.example.com/search?q=x",
                    "image": "https://cdn.example.com/default.jpg",
                },
                "twitter": {
                    "card": "summary_large_image",
                    "title": "search title",
                    "description": "search excerpt",
                    "image": "https://cdn.example.com/default.jpg",
                },
            },
        ),
    ],
)
def test_regression_entity_type_snapshots(
    entity_type: str,
    route: str,
    expected: dict,
) -> None:
    entity = SEOEntity(
        entity_type=entity_type,
        title=f"{entity_type} title",
        excerpt=f"{entity_type} excerpt",
        status="published",
    )
    payload = build_seo_payload(entity, route, _config())
    assert payload == expected
