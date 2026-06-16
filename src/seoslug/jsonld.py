"""JSON-LD helpers for seoslug."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING

from .exceptions import SEOEntityError

if TYPE_CHECKING:
    from .config import SEOConfig
    from .schemas import SEOEntity


def normalize_schema_jsonld(value: dict | list[dict] | None) -> dict | list[dict] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return deepcopy(value)
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return deepcopy(value)
    raise SEOEntityError("schema_jsonld must be dict, list[dict], or None")


def build_schema(
    entity: SEOEntity,
    config: SEOConfig,
    canonical: str,
    title: str,
    description: str | None,
    og_image: str | None,
) -> dict | None:
    schema_type = config.schema_type_map.get(entity.entity_type)
    if schema_type is None:
        return None

    schema: dict = {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": title,
        "url": canonical,
    }

    if description:
        schema["description"] = description
    if og_image:
        schema["image"] = og_image
    if entity.published_at:
        schema["datePublished"] = entity.published_at
    if entity.updated_at:
        schema["dateModified"] = entity.updated_at

    if schema_type in {"Article", "BlogPosting", "NewsArticle"}:
        schema["mainEntityOfPage"] = {"@id": canonical}

    if entity.author_name:
        schema["author"] = {"@type": "Person", "name": entity.author_name}

    if config.publisher_name:
        publisher: dict = {"@type": "Organization", "name": config.publisher_name}
        if config.publisher_logo:
            publisher["logo"] = config.publisher_logo
        schema["publisher"] = publisher

    return schema
