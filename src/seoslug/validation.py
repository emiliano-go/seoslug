"""Validation helpers for SEO payloads and JSON-LD."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .exceptions import SEOEntityError, SEOPayloadError

if TYPE_CHECKING:
    from .config import SEOConfig


_ABSOLUTE_PREFIXES = ("http://", "https://")


def validate_payload(payload: dict, config: SEOConfig) -> list[str]:
    """Validate a resolved SEO payload and return warning strings."""
    warnings: list[str] = []

    title = payload.get("title", "")
    if len(title) > 60:
        warnings.append(f"Title exceeds 60 characters ({len(title)} chars)")

    description = payload.get("description") or ""
    if len(description) > 160:
        warnings.append(f"Description exceeds 160 characters ({len(description)} chars)")

    canonical = payload.get("canonical", "")
    if canonical and not canonical.startswith(_ABSOLUTE_PREFIXES):
        warnings.append(f"Canonical URL is not absolute: {canonical}")

    og_image = _nested_get(payload, ("og", "image"), "")
    if og_image and not og_image.startswith(_ABSOLUTE_PREFIXES):
        warnings.append(f"OG image URL is not absolute: {og_image}")

    robots = payload.get("robots", "")
    if robots and not _valid_robots_format(robots):
        warnings.append(f"Robots directive may be malformed: {robots}")

    schema_jsonld = payload.get("schema_jsonld")
    if schema_jsonld is not None:
        warnings.extend(validate_schema_jsonld(schema_jsonld))

    return warnings


def validate_schema_jsonld(
    schema_jsonld: dict | list[dict] | None,
    strict: bool = False,
) -> list[str]:
    """Validate JSON-LD shape and return non-fatal warnings.

    Structural issues raise :class:`SEOEntityError` immediately. Missing
    recommended fields are warnings by default and become errors when
    ``strict`` is ``True``.
    """
    if schema_jsonld is None:
        return []

    nodes = _coerce_schema_nodes(schema_jsonld)
    warnings: list[str] = []
    for index, node in enumerate(nodes, start=1):
        warnings.extend(_validate_schema_node(node, path=f"schema_jsonld[{index}]"))

    if strict and warnings:
        raise SEOEntityError("; ".join(warnings))
    return warnings


def _coerce_schema_nodes(schema_jsonld: dict | list[dict]) -> list[dict]:
    if isinstance(schema_jsonld, dict):
        return [schema_jsonld]
    if isinstance(schema_jsonld, list) and all(isinstance(item, dict) for item in schema_jsonld):
        return list(schema_jsonld)
    raise SEOEntityError("schema_jsonld must be dict, list[dict], or None")


def _validate_schema_node(node: dict, path: str) -> list[str]:
    warnings: list[str] = []

    node_type = node.get("@type")
    if node_type is not None and not _is_valid_schema_type(node_type):
        raise SEOEntityError(f"{path}: @type must be a string or list[str]")

    context = node.get("@context")
    if context is None:
        warnings.append(f"{path}: missing @context")
    elif not isinstance(context, str):
        raise SEOEntityError(f"{path}: @context must be a string when present")

    graph = node.get("@graph")
    if graph is not None:
        if not isinstance(graph, list) or not all(isinstance(item, dict) for item in graph):
            raise SEOEntityError(f"{path}: @graph must be a list[dict]")
        for index, child in enumerate(graph, start=1):
            warnings.extend(_validate_schema_node(child, f"{path}[@graph][{index}]"))

    # Light-touch recommendations for common SEO nodes.
    if _is_article_type(node_type) and not node.get("headline"):
        warnings.append(f"{path}: recommended headline is missing")
    if _is_name_expected(node_type) and not node.get("name"):
        warnings.append(f"{path}: recommended name is missing")
    if node_type is not None and not node.get("description"):
        warnings.append(f"{path}: recommended description is missing")

    return warnings


def _is_valid_schema_type(value: object) -> bool:
    if isinstance(value, str):
        return bool(value.strip())
    if isinstance(value, list):
        return bool(value) and all(isinstance(item, str) and item.strip() for item in value)
    return False


def _is_article_type(value: object) -> bool:
    if isinstance(value, str):
        return value in {"Article", "BlogPosting", "NewsArticle"}
    if isinstance(value, list):
        return any(item in {"Article", "BlogPosting", "NewsArticle"} for item in value if isinstance(item, str))
    return False


def _is_name_expected(value: object) -> bool:
    if isinstance(value, str):
        return value in {"WebPage", "CollectionPage", "SearchResultsPage", "Product", "FAQPage", "Organization", "LocalBusiness", "BreadcrumbList"}
    if isinstance(value, list):
        return any(
            item in {"WebPage", "CollectionPage", "SearchResultsPage", "Product", "FAQPage", "Organization", "LocalBusiness", "BreadcrumbList"}
            for item in value
            if isinstance(item, str)
        )
    return False


def _nested_get(d: dict, keys: tuple[str, ...], default: str = "") -> str:
    for key in keys:
        if not isinstance(d, dict):
            return default
        d = d.get(key, {})  # type: ignore[assignment]
    return d if isinstance(d, str) else default


def _valid_robots_format(robots: str) -> bool:
    if not robots:
        return False
    directives = robots.split(",")
    for directive in directives:
        d = directive.strip()
        if not d:
            return False
        if ":" in d:
            name, _, value = d.partition(":")
            if not name.strip() or not value.strip():
                return False
        else:
            if d not in {"index", "noindex", "follow", "nofollow", "none", "all"}:
                return False
    return True


def validate_html_jsonld(html: str, strict: bool = False) -> list[str]:
    """Validate rendered HTML for JSON-LD duplication."""
    if not isinstance(html, str) or not html.strip():
        raise SEOPayloadError("html must be a non-empty string")

    from .html_validation import extract_jsonld_blocks

    blocks = extract_jsonld_blocks(html)
    warnings: list[str] = []
    seen: dict[str, int] = {}
    for index, block in enumerate(blocks, start=1):
        count = seen.get(block, 0) + 1
        seen[block] = count
        if count > 1:
            warnings.append(f"Duplicate JSON-LD block detected at index {index}")

    if strict and warnings:
        raise SEOPayloadError("; ".join(warnings))
    return warnings
