"""URL normalization functions for seoslug."""

import re
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .config import SEOConfig, URLPolicy
from .exceptions import SEOPayloadError, URLPolicyError

_DETRACK_AVAILABLE: bool = False
_detrack_clean_query = None

# Tracking parameters to strip (built-in fallback when detrack is not available)
_TRACKING_PARAM_RE = re.compile(
    r'^(utm_source|utm_medium|utm_campaign|utm_term|utm_content'
    r'|fbclid|gclid|gclsrc|dclid'
    r'|msclkid|twclid|igclid'
    r'|ref|source|mc_cid|mc_eid'
    r'|_ga|_gl|_gac|_gu|_kx)$',
    re.IGNORECASE,
)


def _try_import_detrack() -> bool:
    global _DETRACK_AVAILABLE, _detrack_clean_query
    if not _DETRACK_AVAILABLE:
        try:
            import detrack
            _detrack_clean_query = detrack.clean_query
            _DETRACK_AVAILABLE = True
        except ImportError:
            _DETRACK_AVAILABLE = False
    return _DETRACK_AVAILABLE


def _clean_query_builtin(query: str) -> str:
    if not query:
        return ""
    pairs = parse_qsl(query, keep_blank_values=True)
    filtered = [(k, v) for k, v in pairs if not _TRACKING_PARAM_RE.match(k)]
    return urlencode(filtered, doseq=True) if filtered else ""


def _clean_query(query: str) -> str:
    if _DETRACK_AVAILABLE and _detrack_clean_query is not None:
        return _detrack_clean_query(query)
    if _try_import_detrack() and _detrack_clean_query is not None:
        return _detrack_clean_query(query)
    return _clean_query_builtin(query)


def _collapse_duplicate_slashes(path: str) -> str:
    out: list[str] = []
    prev_slash = False
    for char in path:
        if char == "/":
            if prev_slash:
                continue
            prev_slash = True
            out.append(char)
        else:
            prev_slash = False
            out.append(char)
    return "".join(out)


def _apply_trailing_slash(path: str, mode: str) -> str:
    if mode == "preserve":
        return path
    if path == "/":
        return path
    if mode == "always":
        return path if path.endswith("/") else path + "/"
    return path.rstrip("/") or "/"


def normalize_path(path: str, policy: URLPolicy) -> str:
    if not isinstance(path, str):
        raise URLPolicyError("path must be a string")
    value = path.strip() or "/"
    if not value.startswith("/"):
        value = "/" + value
    if policy.collapse_duplicate_slashes:
        value = _collapse_duplicate_slashes(value)
    if policy.lowercase_paths:
        value = value.lower()
    value = _apply_trailing_slash(value, policy.trailing_slash)
    return value


def _filter_query(query: str, policy: URLPolicy) -> str:
    if policy.strip_tracking_params:
        query = _clean_query(query)
    if policy.allowed_query_params:
        pairs = parse_qsl(query, keep_blank_values=True)
        allowlist = set(policy.allowed_query_params)
        filtered = [(k, v) for k, v in pairs if k in allowlist]
        query = urlencode(filtered, doseq=True)
    return query


def normalize_public_url(url_or_path: str, config: SEOConfig) -> str:
    if not isinstance(url_or_path, str) or not url_or_path.strip():
        raise SEOPayloadError("url_or_path must be a non-empty string")

    value = url_or_path.strip()
    parsed_input = urlsplit(value)
    parsed_base = urlsplit(config.public_base_url)

    if parsed_input.scheme and not parsed_input.netloc:
        raise SEOPayloadError("Malformed URL input")

    path = parsed_input.path
    query = parsed_input.query
    if not parsed_input.scheme and not parsed_input.netloc:
        path = value.split("?", 1)[0]
        query = value.split("?", 1)[1] if "?" in value else ""

    base_path = parsed_base.path.rstrip("/")
    if base_path:
        route = path or "/"
        if not route.startswith(base_path + "/") and route != base_path:
            path = base_path + route if route.startswith("/") else base_path + "/" + route

    normalized_path = normalize_path(path or "/", config.url_policy)
    normalized_query = _filter_query(query, config.url_policy)

    scheme = "https" if config.url_policy.enforce_https else (parsed_base.scheme or "https")
    netloc = config.canonical_host
    return urlunsplit((scheme, netloc, normalized_path, normalized_query, ""))
