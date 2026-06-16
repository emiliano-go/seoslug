"""SEO payload builder for seoslug."""

from collections.abc import Callable

from .config import SEOConfig
from .hooks import run as run_hooks
from .jsonld import build_schema, normalize_schema_jsonld
from .normalization import normalize_public_url
from .schemas import SEOEntity, SEOOverrides
from .text import build_description_snippet


_LazyValue = str | None | Callable[[], str | None]


def _pick(*values: _LazyValue) -> str | None:
    for value in values:
        if callable(value):
            value = value()
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _entity_default_robots(entity: SEOEntity, config: SEOConfig) -> str:
    if entity.entity_type == "search":
        return config.search_robots
    if (entity.status or "").lower() == "published":
        return "index,follow"
    return config.default_robots


def _og_type(entity: SEOEntity) -> str:
    if entity.entity_type in {"post", "video"}:
        return "article"
    return "website"


def build_seo_payload(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
) -> dict:
    ov = overrides or SEOOverrides()

    title = _pick(ov.meta_title, entity.title, "Untitled")
    if config.title_template:
        title = config.title_template.format(title=title)

    description = _pick(
        ov.meta_description,
        entity.excerpt,
        lambda: build_description_snippet(entity.body_html),
        "",
    )

    canonical = _pick(ov.canonical_url, normalize_public_url(route_path, config))
    robots = _pick(ov.robots, _entity_default_robots(entity, config))

    og_title = _pick(ov.og_title, title)
    og_description = _pick(ov.og_description, description)
    og_image = _pick(ov.og_image, entity.featured_image, config.default_og_image)

    twitter_title = _pick(ov.twitter_title, og_title)
    twitter_description = _pick(ov.twitter_description, og_description)
    twitter_image = _pick(ov.twitter_image, og_image)
    twitter_card = _pick(ov.twitter_card, "summary_large_image")

    og: dict = {
        "type": _og_type(entity),
        "title": og_title,
        "description": og_description,
        "url": canonical,
        "image": og_image,
    }
    if config.site_name:
        og["site_name"] = config.site_name

    payload: dict = {
        "title": title,
        "description": description,
        "canonical": canonical,
        "robots": robots,
        "og": og,
        "twitter": {
            "card": twitter_card,
            "title": twitter_title,
            "description": twitter_description,
            "image": twitter_image,
        },
    }

    if ov.omit_schema:
        pass
    elif ov.schema_jsonld is not None:
        payload["schema_jsonld"] = normalize_schema_jsonld(ov.schema_jsonld)
    elif config.auto_generate_schema:
        schema = build_schema(
            entity=entity,
            config=config,
            canonical=canonical,
            title=title,
            description=description,
            og_image=og_image,
        )
        if schema is not None:
            payload["schema_jsonld"] = schema

    payload = run_hooks("post_process", payload, entity, config)
    return payload
