"""Configuration models for seoslug."""

from dataclasses import dataclass, field
from typing import Literal
from urllib.parse import urlparse


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
            raise ValueError(
                "trailing_slash must be one of: 'always', 'never', 'preserve'"
            )

        cleaned_params: list[str] = []
        seen: set[str] = set()
        for param in self.allowed_query_params:
            if not isinstance(param, str):
                raise ValueError("allowed_query_params must contain only strings")
            normalized = param.strip()
            if not normalized:
                continue
            if normalized not in seen:
                seen.add(normalized)
                cleaned_params.append(normalized)
        self.allowed_query_params = cleaned_params


@dataclass(slots=True)
class SEOConfig:
    canonical_host: str
    public_base_url: str
    url_policy: URLPolicy
    default_robots: str = "index,follow"
    default_og_image: str | None = None
    site_name: str | None = None
    title_template: str | None = "{title}"
    search_robots: str = "noindex,follow"
    schema_type_map: dict[str, str | None] = field(default_factory=lambda: {
        "post": "Article",
        "page": "WebPage",
        "video": "VideoObject",
        "home": "WebPage",
        "taxonomy": "CollectionPage",
        "search": "SearchResultsPage",
    })
    auto_generate_schema: bool = True
    publisher_name: str | None = None
    publisher_logo: str | None = None

    def __post_init__(self) -> None:
        self.canonical_host = _validate_canonical_host(self.canonical_host)
        self.public_base_url = _validate_public_base_url(self.public_base_url)

        if not isinstance(self.url_policy, URLPolicy):
            raise ValueError("url_policy must be a URLPolicy instance")

        if not _is_nonempty_string(self.default_robots):
            raise ValueError("default_robots must be a non-empty string")
        if not _is_nonempty_string(self.search_robots):
            raise ValueError("search_robots must be a non-empty string")

        if self.default_og_image is not None and not _is_nonempty_string(
            self.default_og_image
        ):
            raise ValueError("default_og_image must be a non-empty string when set")

        if self.site_name is not None and not _is_nonempty_string(self.site_name):
            raise ValueError("site_name must be a non-empty string when set")

        if self.title_template is not None:
            if not _is_nonempty_string(self.title_template):
                raise ValueError("title_template must be a non-empty string when set")
            if "{title}" not in self.title_template:
                raise ValueError("title_template must include '{title}' placeholder")


def _is_nonempty_string(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_canonical_host(canonical_host: str) -> str:
    if not _is_nonempty_string(canonical_host):
        raise ValueError("canonical_host must be a non-empty string")

    value = canonical_host.strip().lower()
    if "://" in value or "/" in value or "?" in value or "#" in value:
        raise ValueError("canonical_host must be host-only (no scheme/path/query)")
    return value


def _validate_public_base_url(public_base_url: str) -> str:
    if not _is_nonempty_string(public_base_url):
        raise ValueError("public_base_url must be a non-empty string")

    value = public_base_url.strip()
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("public_base_url must be an absolute http(s) URL")
    return value
