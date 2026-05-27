"""URL normalization functions for seoslug."""

from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from .config import SEOConfig, URLPolicy

_TRACKING_KEYS = {"gclid", "fbclid"}


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
        raise ValueError("path must be a string")
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
    pairs = parse_qsl(query, keep_blank_values=True)
    filtered: list[tuple[str, str]] = []
    allowlist = set(policy.allowed_query_params)
    for key, value in pairs:
        k = key.lower()
        if policy.strip_tracking_params and (k.startswith("utm_") or k in _TRACKING_KEYS):
            continue
        if allowlist and key not in allowlist:
            continue
        filtered.append((key, value))
    return urlencode(filtered, doseq=True)


def normalize_public_url(url_or_path: str, config: SEOConfig) -> str:
    if not isinstance(url_or_path, str) or not url_or_path.strip():
        raise ValueError("url_or_path must be a non-empty string")

    value = url_or_path.strip()
    parsed_input = urlsplit(value)
    parsed_base = urlsplit(config.public_base_url)

    if parsed_input.scheme and not parsed_input.netloc:
        raise ValueError("Malformed URL input")

    path = parsed_input.path
    query = parsed_input.query
    if not parsed_input.scheme and not parsed_input.netloc:
        path = value.split("?", 1)[0]
        query = value.split("?", 1)[1] if "?" in value else ""

    normalized_path = normalize_path(path or "/", config.url_policy)
    normalized_query = _filter_query(query, config.url_policy)

    scheme = "https" if config.url_policy.enforce_https else (parsed_base.scheme or "https")
    netloc = config.canonical_host
    return urlunsplit((scheme, netloc, normalized_path, normalized_query, ""))
