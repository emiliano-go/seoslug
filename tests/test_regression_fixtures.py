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


HOME_EXPECTED = {
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
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "home title",
        "url": "https://portal.example.com/",
        "description": "home excerpt",
        "image": "https://cdn.example.com/default.jpg",
    },
}

POST_EXPECTED = {
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
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "Article",
        "name": "post title",
        "url": "https://portal.example.com/posts/p",
        "description": "post excerpt",
        "image": "https://cdn.example.com/default.jpg",
        "mainEntityOfPage": {"@id": "https://portal.example.com/posts/p"},
    },
}

PAGE_EXPECTED = {
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
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "page title",
        "url": "https://portal.example.com/about",
        "description": "page excerpt",
        "image": "https://cdn.example.com/default.jpg",
    },
}

VIDEO_EXPECTED = {
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
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "VideoObject",
        "name": "video title",
        "url": "https://portal.example.com/videos/v",
        "description": "video excerpt",
        "image": "https://cdn.example.com/default.jpg",
    },
}

TAXONOMY_EXPECTED = {
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
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "taxonomy title",
        "url": "https://portal.example.com/topics/python",
        "description": "taxonomy excerpt",
        "image": "https://cdn.example.com/default.jpg",
    },
}

SEARCH_EXPECTED = {
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
    "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "SearchResultsPage",
        "name": "search title",
        "url": "https://portal.example.com/search?q=x",
        "description": "search excerpt",
        "image": "https://cdn.example.com/default.jpg",
    },
}


@pytest.mark.parametrize(
    ("entity_type", "route", "expected"),
    [
        ("home", "/", HOME_EXPECTED),
        ("post", "/posts/p", POST_EXPECTED),
        ("page", "/about", PAGE_EXPECTED),
        ("video", "/videos/v", VIDEO_EXPECTED),
        ("taxonomy", "/topics/python", TAXONOMY_EXPECTED),
        ("search", "/search?q=x", SEARCH_EXPECTED),
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
