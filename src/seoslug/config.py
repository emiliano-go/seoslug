"""Configuration models for seoslug."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Literal
from urllib.parse import urlparse

from .exceptions import SEOConfigError, URLPolicyError

if TYPE_CHECKING:
    from .hooks import HookRegistry
    from .registry import SchemaRegistry

from .schemas import OGImage, Robots


@dataclass(slots=True)
class URLPolicy:
    enforce_https: bool = True
    lowercase_paths: bool = True
    trailing_slash: Literal["always", "never", "preserve"] = "never"
    collapse_duplicate_slashes: bool = True
    strip_tracking_params: bool = True
    allowed_query_params: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if self.trailing_slash not in {"always", "never", "preserve"}:
            raise URLPolicyError(
                "trailing_slash must be one of: 'always', 'never', 'preserve'"
            )

        cleaned_params: list[str] = []
        seen: set[str] = set()
        for param in self.allowed_query_params:
            if not isinstance(param, str):
                raise URLPolicyError("allowed_query_params must contain only strings")
            normalized = param.strip()
            if not normalized:
                continue
            if normalized not in seen:
                seen.add(normalized)
                cleaned_params.append(normalized)
        self.allowed_query_params = cleaned_params


@dataclass(slots=True)
class SEOConfig:
    """Configuration for SEO metadata generation.

    canonical_host -- hostname used for all output canonical URLs (host-only, no scheme/path/port)
    public_base_url -- full absolute URL of the deployment; its path is used as the base path
                       for canonical URLs (e.g. "/blog/" for sub-path deployments)
    """
    canonical_host: str
    public_base_url: str
    url_policy: URLPolicy
    default_robots: str | Robots = "index,follow"
    default_og_image: str | OGImage | None = None
    site_name: str | None = None
    title_template: str | None = "{title}"
    search_robots: str | Robots = "noindex,follow"
    schema_type_map: dict[str, str | None] = field(default_factory=lambda: {
        "post": "Article",
        "page": "WebPage",
        "video": "VideoObject",
        "home": "WebPage",
        "taxonomy": "CollectionPage",
        "search": "SearchResultsPage",
        "product": "Product",
        "organization": "Organization",
        "local_business": "LocalBusiness",
        "faq": "FAQPage",
    })
    auto_generate_schema: bool = True
    publisher_name: str | None = None
    publisher_logo: str | None = None
    locale: str | None = None
    locale_alternate: list[str] | None = None
    twitter_site: str | None = None
    schema_registry: SchemaRegistry | None = None
    hooks: HookRegistry | None = None
    emit_warnings: bool = False

    def __post_init__(self) -> None:
        self.canonical_host = _validate_canonical_host(self.canonical_host)
        self.public_base_url = _validate_public_base_url(self.public_base_url)

        if not isinstance(self.url_policy, URLPolicy):
            raise SEOConfigError("url_policy must be a URLPolicy instance")

        self.default_robots = _validate_robots_config(self.default_robots, "default_robots")
        self.search_robots = _validate_robots_config(self.search_robots, "search_robots")

        self.default_og_image = _validate_image_config(self.default_og_image, "default_og_image")

        if self.site_name is not None and not _is_nonempty_string(self.site_name):
            raise SEOConfigError("site_name must be a non-empty string when set")

        if self.title_template is not None:
            if not _is_nonempty_string(self.title_template):
                raise SEOConfigError("title_template must be a non-empty string when set")
            if "{title}" not in self.title_template:
                raise SEOConfigError("title_template must include '{title}' placeholder")

        if self.locale is not None and not _is_nonempty_string(self.locale):
            raise ValueError("locale must be a non-empty string when set")

        if self.twitter_site is not None and not _is_nonempty_string(self.twitter_site):
            raise ValueError("twitter_site must be a non-empty string when set")


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_robots_config(value: str | Robots, field_name: str) -> str | Robots:
    if isinstance(value, Robots):
        return value
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise ValueError(f"{field_name} must be a non-empty string or Robots instance")


def _validate_image_config(value: str | OGImage | None, field_name: str) -> str | OGImage | None:
    if value is None:
        return None
    if isinstance(value, OGImage):
        return value
    if isinstance(value, str) and value.strip():
        return value.strip()
    raise ValueError(f"{field_name} must be a non-empty string, OGImage, or None")


def _validate_canonical_host(canonical_host: str) -> str:
    if not _is_nonempty_string(canonical_host):
        raise SEOConfigError("canonical_host must be a non-empty string")

    value = canonical_host.strip().lower()
    if "://" in value or "/" in value or "?" in value or "#" in value:
        raise SEOConfigError("canonical_host must be host-only (no scheme/path/query)")

    if value.endswith("."):
        raise ValueError("canonical_host must not have a trailing dot")
    if "[" in value or "]" in value:
        raise ValueError("canonical_host must be host-only (IPv6 not supported)")
    if ":" in value:
        raise ValueError("canonical_host must be host-only (no port)")
    return value


def _validate_public_base_url(public_base_url: str) -> str:
    if not _is_nonempty_string(public_base_url):
        raise SEOConfigError("public_base_url must be a non-empty string")

    value = public_base_url.strip()
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise SEOConfigError("public_base_url must be an absolute http(s) URL")
    return value
