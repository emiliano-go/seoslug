"""JSON-LD helpers for seoslug."""

from __future__ import annotations

from copy import deepcopy
from typing import TYPE_CHECKING, Callable

from .normalization import normalize_public_url

from .exceptions import SEOEntityError

if TYPE_CHECKING:
    from .config import SEOConfig
    from .schemas import SEOEntity, Breadcrumb


# -- Public helpers ------------------------------------------------------------

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

    # Check registry before built-in builders
    if config.schema_registry:
        generator = config.schema_registry.get(schema_type)
        if generator is not None:
            return generator(
                entity=entity,
                config=config,
                canonical=canonical,
                title=title,
                description=description,
                og_image=og_image,
            )

    # Built-in schema builders
    builder = _SCHEMA_BUILDERS.get(schema_type)
    if builder is not None:
        return builder(
            entity=entity,
            config=config,
            canonical=canonical,
            title=title,
            description=description,
            og_image=og_image,
        )

    # Generic fallback for any other schema.org type
    return _build_generic(
        schema_type, entity, config, canonical, title, description, og_image,
    )


def build_breadcrumb_list(
    breadcrumbs: list[Breadcrumb],
    config: SEOConfig,
) -> dict:
    """Build a BreadcrumbList JSON-LD dict from breadcrumb items."""
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": bc.name,
                "item": normalize_public_url(bc.url, config),
            }
            for i, bc in enumerate(breadcrumbs)
        ],
    }


# -- Generic builder (Article, WebPage, VideoObject, CollectionPage, etc.) -----

def _build_generic(
    schema_type: str,
    entity: SEOEntity,
    config: SEOConfig,
    canonical: str,
    title: str,
    description: str | None,
    og_image: str | None,
) -> dict:
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


# -- Type-specific builders ----------------------------------------------------

def _build_product(
    entity: SEOEntity,
    config: SEOConfig,
    canonical: str,
    title: str,
    description: str | None,
    og_image: str | None,
) -> dict:
    schema = _build_generic(
        "Product", entity, config, canonical, title, description, og_image,
    )

    if entity.sku:
        schema["sku"] = entity.sku

    if entity.price or entity.price_currency or entity.availability:
        offer: dict = {"@type": "Offer"}
        if entity.price:
            offer["price"] = entity.price
        if entity.price_currency:
            offer["priceCurrency"] = entity.price_currency
        if entity.availability:
            offer["availability"] = f"https://schema.org/{entity.availability}"
        schema["offers"] = offer

    return schema


def _build_organization(
    entity: SEOEntity,
    config: SEOConfig,
    canonical: str,
    title: str,
    description: str | None,
    og_image: str | None,
) -> dict:
    schema = _build_generic(
        "Organization", entity, config, canonical, title, description, og_image,
    )

    if entity.same_as:
        schema["sameAs"] = entity.same_as
    if config.publisher_logo:
        schema["logo"] = config.publisher_logo

    return schema


def _build_local_business(
    entity: SEOEntity,
    config: SEOConfig,
    canonical: str,
    title: str,
    description: str | None,
    og_image: str | None,
) -> dict:
    schema = _build_organization(
        entity, config, canonical, title, description, og_image,
    )
    schema["@type"] = "LocalBusiness"

    if entity.address:
        schema["address"] = {"@type": "PostalAddress", "streetAddress": entity.address}

    return schema


def _build_faq_page(
    entity: SEOEntity,
    config: SEOConfig,
    canonical: str,
    title: str,
    description: str | None,
    og_image: str | None,
) -> dict:
    schema = _build_generic(
        "FAQPage", entity, config, canonical, title, description, og_image,
    )

    if entity.faq_items:
        schema["mainEntity"] = [
            {
                "@type": "Question",
                "name": item.question,
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item.answer,
                },
            }
            for item in entity.faq_items
        ]

    return schema


# -- Builder registry (populated after all builder definitions) ----------------

_SCHEMA_BUILDERS: dict[str, Callable[..., dict | None]] = {
    "Product": _build_product,
    "Organization": _build_organization,
    "LocalBusiness": _build_local_business,
    "FAQPage": _build_faq_page,
}
