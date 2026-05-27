"""Input schemas for seoslug."""

from dataclasses import dataclass
from typing import Literal


_ENTITY_TYPES = {"home", "post", "page", "video", "taxonomy", "search", "other"}


def _normalize_optional_string(value: object, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string or None")
    normalized = value.strip()
    return normalized or None


@dataclass(slots=True)
class SEOEntity:
    entity_type: Literal["home", "post", "page", "video", "taxonomy", "search", "other"]
    slug: str | None = None
    title: str | None = None
    excerpt: str | None = None
    body_html: str | None = None
    status: str | None = None
    featured_image: str | None = None
    published_at: str | None = None
    updated_at: str | None = None

    def __post_init__(self) -> None:
        if self.entity_type not in _ENTITY_TYPES:
            raise ValueError("entity_type must be one of home/post/page/video/taxonomy/search/other")

        self.slug = _normalize_optional_string(self.slug, "slug")
        self.title = _normalize_optional_string(self.title, "title")
        self.excerpt = _normalize_optional_string(self.excerpt, "excerpt")
        self.body_html = _normalize_optional_string(self.body_html, "body_html")
        self.status = _normalize_optional_string(self.status, "status")
        self.featured_image = _normalize_optional_string(self.featured_image, "featured_image")
        self.published_at = _normalize_optional_string(self.published_at, "published_at")
        self.updated_at = _normalize_optional_string(self.updated_at, "updated_at")


@dataclass(slots=True)
class SEOOverrides:
    meta_title: str | None = None
    meta_description: str | None = None
    canonical_url: str | None = None
    robots: str | None = None
    og_title: str | None = None
    og_description: str | None = None
    og_image: str | None = None
    twitter_card: str | None = None
    twitter_title: str | None = None
    twitter_description: str | None = None
    twitter_image: str | None = None
    schema_jsonld: dict | list[dict] | None = None

    def __post_init__(self) -> None:
        self.meta_title = _normalize_optional_string(self.meta_title, "meta_title")
        self.meta_description = _normalize_optional_string(
            self.meta_description, "meta_description"
        )
        self.canonical_url = _normalize_optional_string(self.canonical_url, "canonical_url")
        self.robots = _normalize_optional_string(self.robots, "robots")
        self.og_title = _normalize_optional_string(self.og_title, "og_title")
        self.og_description = _normalize_optional_string(
            self.og_description, "og_description"
        )
        self.og_image = _normalize_optional_string(self.og_image, "og_image")
        self.twitter_card = _normalize_optional_string(self.twitter_card, "twitter_card")
        self.twitter_title = _normalize_optional_string(self.twitter_title, "twitter_title")
        self.twitter_description = _normalize_optional_string(
            self.twitter_description, "twitter_description"
        )
        self.twitter_image = _normalize_optional_string(self.twitter_image, "twitter_image")

        if self.schema_jsonld is None:
            return
        if isinstance(self.schema_jsonld, dict):
            return
        if isinstance(self.schema_jsonld, list) and all(
            isinstance(item, dict) for item in self.schema_jsonld
        ):
            return
        raise ValueError("schema_jsonld must be dict, list[dict], or None")
