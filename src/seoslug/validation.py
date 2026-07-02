"""SEO payload validation with non-fatal warnings."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .config import SEOConfig


def validate_payload(payload: dict, config: SEOConfig) -> list[str]:
    """Validate a built SEO payload and return a list of warning strings.

    Call when ``config.emit_warnings`` is True.
    """
    warnings: list[str] = []

    title = payload.get("title", "")
    if len(title) > 60:
        warnings.append(f"Title exceeds 60 characters ({len(title)} chars)")

    description = payload.get("description") or ""
    if len(description) > 160:
        warnings.append(f"Description exceeds 160 characters ({len(description)} chars)")

    canonical = payload.get("canonical", "")
    if canonical and not canonical.startswith(("http://", "https://")):
        warnings.append(f"Canonical URL is not absolute: {canonical}")

    og_image = _nested_get(payload, ("og", "image"), "")
    if og_image and not og_image.startswith(("http://", "https://")):
        warnings.append(f"OG image URL is not absolute: {og_image}")

    robots = payload.get("robots", "")
    if robots and not _valid_robots_format(robots):
        warnings.append(f"Robots directive may be malformed: {robots}")

    return warnings


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
