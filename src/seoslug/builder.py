"""SEO payload builder for seoslug.

Precedence (highest to lowest) for every resolved field:

    title:       SEOOverrides.meta_title > SEOEntity.title > "Untitled"
                 then title_template applied unless skip_title_template

    description: SEOOverrides.meta_description > SEOEntity.excerpt
                 > build_description_snippet(SEOEntity.body_html) > ""

    canonical:   SEOOverrides.canonical_url
                 > normalize_public_url(route_path, config)

    robots:      SEOOverrides.robots > entity-derived default*
                 > config.default_robots > "index,follow"
                 *entity default: "noindex,follow" for search,
                  config.default_robots for non-published,
                  "index,follow" for published

    og:type:     SEOEntity.entity_type mapped ("post"/"video" -> "article")

    og:title:    SEOOverrides.og_title > resolved title
    og:desc:     SEOOverrides.og_description > resolved description

    og:image:    SEOOverrides.og_image > SEOEntity.featured_image
                 > SEOConfig.default_og_image > None

    twitter:card:SEOOverrides.twitter_card > "summary_large_image"
    twitter:title:SEOOverrides.twitter_title > og:title
    twitter:desc: SEOOverrides.twitter_description > og:description
    twitter:image:SEOOverrides.twitter_image > resolved og:image

    schema:      SEOOverrides.omit_schema -> None
                 > SEOOverrides.schema_jsonld (normalised)
                 > auto_generate_schema (via build_schema)
                 + entity.breadcrumbs appended as BreadcrumbList

Each field is resolved explicitly in `build_seo_payload()` below.
The ``_pick()`` and ``_pick_image()`` helpers return the first
non-None, non-empty value from the ordered list.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from .config import SEOConfig
from .hooks import run as run_hooks
from .jsonld import build_breadcrumb_list, build_schema, normalize_schema_jsonld
from .normalization import normalize_public_url
from .payload import OGPayload, SEOPayload, TwitterPayload
from .schemas import OGImage, Robots, SEOEntity, SEOOverrides
from .text import build_description_snippet

if TYPE_CHECKING:
    from .payload import SEOPayloadTypedDict


_LazyValue = str | None | Callable[[], str | None]


def _pick(*values: _LazyValue) -> str | None:
    for value in values:
        if callable(value):
            value = value()
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _pick_image(*values: str | OGImage | None) -> str | OGImage | None:
    for value in values:
        if value is not None:
            if isinstance(value, str):
                stripped = value.strip()
                if stripped:
                    return stripped
            else:
                return value
    return None


def _resolve_image_parts(
    value: str | OGImage | None,
) -> tuple[str | None, int | None, int | None, str | None]:
    if value is None:
        return (None, None, None, None)
    if isinstance(value, str):
        return (value, None, None, None)
    return (value.url, value.width, value.height, value.alt)


def _entity_default_robots(entity: SEOEntity, config: SEOConfig) -> str | Robots:
    if entity.entity_type == "search":
        return config.search_robots
    if (entity.status or "").lower() == "published":
        return "index,follow"
    return config.default_robots


def _og_type(entity: SEOEntity) -> str:
    if entity.entity_type in {"post", "video"}:
        return "article"
    return "website"


_SENTINEL = SEOOverrides()


def build_seo_payload(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
) -> SEOPayload:
    ov = overrides if overrides is not None else _SENTINEL

    title = _pick(ov.meta_title, entity.title, "Untitled")
    if config.title_template and not ov.skip_title_template:
        title = config.title_template.format(title=title)

    description = _pick(
        ov.meta_description,
        entity.excerpt,
        lambda: build_description_snippet(entity.body_html),
        "",
    )

    canonical = _pick(ov.canonical_url, normalize_public_url(route_path, config))

    # Robots — handle both str and Robots
    _raw_robots = ov.robots if ov.robots is not None else _entity_default_robots(entity, config)
    robots: str = _raw_robots.serialize() if isinstance(_raw_robots, Robots) else _raw_robots

    # OG / Twitter images — handle both str and OGImage
    og_image = _pick_image(ov.og_image, entity.featured_image, config.default_og_image)
    og_img_url, og_img_w, og_img_h, og_img_alt = _resolve_image_parts(og_image)

    twitter_image = _pick_image(ov.twitter_image, og_image)
    tw_img_url, tw_img_w, tw_img_h, tw_img_alt = _resolve_image_parts(twitter_image)

    og_title = _pick(ov.og_title, title)
    og_description = _pick(ov.og_description, description)

    twitter_title = _pick(ov.twitter_title, og_title)
    twitter_description = _pick(ov.twitter_description, og_description)
    twitter_card = _pick(ov.twitter_card, "summary_large_image")

    # OG dataclass
    og = OGPayload(
        type=_og_type(entity),
        title=og_title,
        description=og_description,
        url=canonical,
        image=og_img_url,
        image_width=og_img_w,
        image_height=og_img_h,
        image_alt=og_img_alt,
        site_name=config.site_name,
        locale=config.locale,
        locale_alternate=config.locale_alternate,
        audio=ov.og_audio,
        video=ov.og_video,
    )

    # Twitter dataclass
    twitter = TwitterPayload(
        card=twitter_card,
        title=twitter_title,
        description=twitter_description,
        image=tw_img_url,
        image_alt=tw_img_alt,
        site=config.twitter_site,
        creator=ov.twitter_creator,
    )

    payload = SEOPayload(
        title=title,
        description=description,
        canonical=canonical,
        robots=robots,
        og=og,
        twitter=twitter,
    )

    # Schema JSON-LD (main + optional breadcrumbs)
    schemas: list[dict] = []

    if ov.omit_schema:
        pass
    elif ov.schema_jsonld is not None:
        override = normalize_schema_jsonld(ov.schema_jsonld)
        if isinstance(override, dict):
            schemas.append(override)
        else:
            schemas.extend(override)
    elif config.auto_generate_schema:
        main_schema = build_schema(
            entity=entity,
            config=config,
            canonical=canonical,
            title=title,
            description=description,
            og_image=og_img_url,
        )
        if main_schema is not None:
            schemas.append(main_schema)

    if entity.breadcrumbs:
        schemas.append(build_breadcrumb_list(entity.breadcrumbs, config))

    if len(schemas) == 1:
        payload.schema_jsonld = schemas[0]
    elif len(schemas) > 1:
        payload.schema_jsonld = schemas

    # Validation warnings
    if config.emit_warnings:
        from .validation import validate_payload
        import warnings as _warnings
        for warning in validate_payload(payload.to_dict(), config):
            _warnings.warn(warning)

    payload = run_hooks("post_process", payload, entity, config)
    return payload


def build_seo_payload_dict(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
) -> dict:
    """Same as ``build_seo_payload`` but returns a plain dict.

    Convenience wrapper for template engines and JSON serialization
    that expect a raw dictionary.
    """
    return build_seo_payload(entity, route_path, config, overrides).to_dict()
