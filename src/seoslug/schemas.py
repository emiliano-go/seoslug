"""Input schemas for seoslug."""

from dataclasses import dataclass
from typing import Literal

from .exceptions import SEOEntityError


_ENTITY_TYPES = {
    "home", "post", "page", "video", "taxonomy", "search", "other",
    "product", "organization", "local_business", "faq",
}


def _normalize_optional_string(value: object, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise SEOEntityError(f"{field_name} must be a string or None")
    normalized = value.strip()
    return normalized or None


# -- New value types -----------------------------------------------------------

@dataclass(slots=True)
class OGImage:
    """Structured Open Graph image with optional dimensions and alt text."""
    url: str
    width: int | None = None
    height: int | None = None
    alt: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.url, str) or not self.url.strip():
            raise ValueError("OGImage.url must be a non-empty string")


@dataclass(slots=True)
class Breadcrumb:
    """A single breadcrumb trail entry."""
    name: str
    url: str

    def __post_init__(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Breadcrumb.name must be a non-empty string")
        if not isinstance(self.url, str) or not self.url.strip():
            raise ValueError("Breadcrumb.url must be a non-empty string")


@dataclass(slots=True)
class FAQItem:
    """A single FAQ question-and-answer pair."""
    question: str
    answer: str

    def __post_init__(self) -> None:
        if not isinstance(self.question, str) or not self.question.strip():
            raise ValueError("FAQItem.question must be a non-empty string")
        if not isinstance(self.answer, str) or not self.answer.strip():
            raise ValueError("FAQItem.answer must be a non-empty string")


@dataclass(slots=True)
class Robots:
    """Structured robots directive.

    Serializes to the standard robots meta content string.
    """
    index: bool = True
    follow: bool = True
    max_snippet: int | None = None
    max_image_preview: str | None = None
    max_video_preview: int | None = None

    def serialize(self) -> str:
        parts: list[str] = [
            "index" if self.index else "noindex",
            "follow" if self.follow else "nofollow",
        ]
        if self.max_snippet is not None:
            parts.append(f"max-snippet:{self.max_snippet}")
        if self.max_image_preview is not None:
            parts.append(f"max-image-preview:{self.max_image_preview}")
        if self.max_video_preview is not None:
            parts.append(f"max-video-preview:{self.max_video_preview}")
        return ",".join(parts)


# -- Normalization helpers for polymorphic fields ------------------------------

def _normalize_image(value: object, field_name: str) -> str | OGImage | None:
    if value is None:
        return None
    if isinstance(value, OGImage):
        if not value.url.strip():
            raise ValueError(f"{field_name} OGImage.url must be non-empty")
        return value
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    raise ValueError(f"{field_name} must be a string, OGImage, or None")


def _normalize_robots(value: object, field_name: str) -> str | Robots | None:
    if value is None:
        return None
    if isinstance(value, Robots):
        return value
    if isinstance(value, str):
        normalized = value.strip()
        return normalized or None
    raise ValueError(f"{field_name} must be a string, Robots, or None")


def _normalize_string_list(value: object, field_name: str) -> list[str] | None:
    if value is None:
        return None
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list or None")
    cleaned: list[str] = []
    for item in value:
        if isinstance(item, str) and item.strip():
            cleaned.append(item.strip())
    return cleaned or None


# -- Main entity ---------------------------------------------------------------

@dataclass(slots=True)
class SEOEntity:
    """Input data for a content entity.

    Fields used in meta tags + JSON-LD:
        entity_type, title, excerpt, body_html, status, featured_image

    Fields used only in JSON-LD schema (not <meta> tags):
        published_at, updated_at, author_name,
        breadcrumbs, sku, price, price_currency, availability,
        same_as, address, faq_items

    Field used only as metadata (not in output):
        slug
    """
    entity_type: Literal[
        "home", "post", "page", "video", "taxonomy", "search", "other",
        "product", "organization", "local_business", "faq",
    ]
    slug: str | None = None
    title: str | None = None
    excerpt: str | None = None
    body_html: str | None = None
    status: str | None = None
    featured_image: str | OGImage | None = None
    published_at: str | None = None
    updated_at: str | None = None
    author_name: str | None = None
    breadcrumbs: list[Breadcrumb] | None = None
    sku: str | None = None
    price: str | None = None
    price_currency: str | None = None
    availability: str | None = None
    same_as: list[str] | None = None
    address: str | None = None
    faq_items: list[FAQItem] | None = None

    def __post_init__(self) -> None:
        if self.entity_type not in _ENTITY_TYPES:
            raise SEOEntityError(
                "entity_type must be one of home/post/page/video/taxonomy/"
                "search/other/product/organization/local_business/faq"
            )

        self.slug = _normalize_optional_string(self.slug, "slug")
        self.title = _normalize_optional_string(self.title, "title")
        self.excerpt = _normalize_optional_string(self.excerpt, "excerpt")
        self.body_html = _normalize_optional_string(self.body_html, "body_html")
        self.status = _normalize_optional_string(self.status, "status")
        self.featured_image = _normalize_image(self.featured_image, "featured_image")
        self.published_at = _normalize_optional_string(self.published_at, "published_at")
        self.updated_at = _normalize_optional_string(self.updated_at, "updated_at")
        self.author_name = _normalize_optional_string(self.author_name, "author_name")
        self.sku = _normalize_optional_string(self.sku, "sku")
        self.price = _normalize_optional_string(self.price, "price")
        self.price_currency = _normalize_optional_string(self.price_currency, "price_currency")
        self.availability = _normalize_optional_string(self.availability, "availability")
        self.same_as = _normalize_string_list(self.same_as, "same_as")
        self.address = _normalize_optional_string(self.address, "address")


# -- Per-entity overrides ------------------------------------------------------

@dataclass(slots=True)
class SEOOverrides:
    """Per-entity overrides for SEO metadata.

    Set skip_title_template=True to bypass the config-level title_template
    for a specific entity (useful when providing a fully-formatted meta_title).
    """
    meta_title: str | None = None
    meta_description: str | None = None
    canonical_url: str | None = None
    robots: str | Robots | None = None
    og_title: str | None = None
    og_description: str | None = None
    og_image: str | OGImage | None = None
    twitter_card: str | None = None
    twitter_title: str | None = None
    twitter_description: str | None = None
    twitter_image: str | OGImage | None = None
    schema_jsonld: dict | list[dict] | None = None
    omit_schema: bool = False
    skip_title_template: bool = False
    twitter_creator: str | None = None
    og_audio: str | None = None
    og_video: str | None = None

    def __post_init__(self) -> None:
        self.meta_title = _normalize_optional_string(self.meta_title, "meta_title")
        self.meta_description = _normalize_optional_string(
            self.meta_description, "meta_description"
        )
        self.canonical_url = _normalize_optional_string(self.canonical_url, "canonical_url")
        self.robots = _normalize_robots(self.robots, "robots")
        self.og_title = _normalize_optional_string(self.og_title, "og_title")
        self.og_description = _normalize_optional_string(
            self.og_description, "og_description"
        )
        self.og_image = _normalize_image(self.og_image, "og_image")
        self.twitter_card = _normalize_optional_string(self.twitter_card, "twitter_card")
        self.twitter_title = _normalize_optional_string(self.twitter_title, "twitter_title")
        self.twitter_description = _normalize_optional_string(
            self.twitter_description, "twitter_description"
        )
        self.twitter_image = _normalize_image(self.twitter_image, "twitter_image")
        self.twitter_creator = _normalize_optional_string(self.twitter_creator, "twitter_creator")
        self.og_audio = _normalize_optional_string(self.og_audio, "og_audio")
        self.og_video = _normalize_optional_string(self.og_video, "og_video")

        if self.schema_jsonld is None:
            return
        if isinstance(self.schema_jsonld, dict):
            return
        if isinstance(self.schema_jsonld, list) and all(
            isinstance(item, dict) for item in self.schema_jsonld
        ):
            return
        raise SEOEntityError("schema_jsonld must be dict, list[dict], or None")


class SEOEntityBuilder:
    """Fluent builder for :class:`SEOEntity`.

    Example::

        entity = (
            SEOEntityBuilder()
            .entity_type("product")
            .title("Widget")
            .price(29.99)
            .availability("InStock")
            .build()
        )
    """

    def __init__(self) -> None:
        self._kwargs: dict = {}

    def entity_type(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["entity_type"] = value
        return self

    def slug(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["slug"] = value
        return self

    def title(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["title"] = value
        return self

    def excerpt(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["excerpt"] = value
        return self

    def body_html(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["body_html"] = value
        return self

    def status(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["status"] = value
        return self

    def featured_image(self, value: str | OGImage) -> "SEOEntityBuilder":
        self._kwargs["featured_image"] = value
        return self

    def published_at(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["published_at"] = value
        return self

    def updated_at(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["updated_at"] = value
        return self

    def author_name(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["author_name"] = value
        return self

    def breadcrumbs(self, value: list[Breadcrumb]) -> "SEOEntityBuilder":
        self._kwargs["breadcrumbs"] = value
        return self

    def sku(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["sku"] = value
        return self

    def price(self, value: str | float) -> "SEOEntityBuilder":
        self._kwargs["price"] = str(value) if isinstance(value, (int, float)) else value
        return self

    def price_currency(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["price_currency"] = value
        return self

    def availability(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["availability"] = value
        return self

    def same_as(self, value: list[str]) -> "SEOEntityBuilder":
        self._kwargs["same_as"] = value
        return self

    def address(self, value: str) -> "SEOEntityBuilder":
        self._kwargs["address"] = value
        return self

    def faq_items(self, value: list[FAQItem]) -> "SEOEntityBuilder":
        self._kwargs["faq_items"] = value
        return self

    def build(self) -> SEOEntity:
        if "entity_type" not in self._kwargs:
            raise ValueError("entity_type is required")
        return SEOEntity(**self._kwargs)
