"""Tests for URL normalization."""

from seoslug import SEOConfig, SEOPayloadError, URLPolicy, normalize_path, normalize_public_url
import pytest


def _config(policy: URLPolicy | None = None) -> SEOConfig:
    return SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="https://portal.example.com",
        url_policy=policy or URLPolicy(),
    )


def test_normalize_path_lowercase_and_slashes() -> None:
    policy = URLPolicy(lowercase_paths=True, collapse_duplicate_slashes=True)
    assert normalize_path("//Blog//My-Post//", policy) == "/blog/my-post"


def test_trailing_slash_modes() -> None:
    assert normalize_path("/blog/post", URLPolicy(trailing_slash="always")) == "/blog/post/"
    assert normalize_path("/blog/post/", URLPolicy(trailing_slash="never")) == "/blog/post"
    assert normalize_path("/blog/post/", URLPolicy(trailing_slash="preserve")) == "/blog/post/"


def test_normalize_public_url_enforces_host_https_and_query_rules() -> None:
    config = _config(URLPolicy(allowed_query_params=["page", "q"]))
    url = "http://other.example.com//Blog/Post?utm_source=x&gclid=1&page=2&q=abc&bad=1"
    assert (
        normalize_public_url(url, config)
        == "https://portal.example.com/blog/post?page=2&q=abc"
    )


def test_normalize_public_url_idempotent() -> None:
    config = _config()
    first = normalize_public_url("/A//B/?utm_campaign=x", config)
    second = normalize_public_url(first, config)
    assert first == second


def test_accepts_relative_path_with_query() -> None:
    config = _config()
    assert (
        normalize_public_url("posts/My-Post?fbclid=123&page=1", config)
        == "https://portal.example.com/posts/my-post?page=1"
    )


def test_enforce_https_toggle_uses_public_base_scheme() -> None:
    config = SEOConfig(
        canonical_host="portal.example.com",
        public_base_url="http://portal.example.com",
        url_policy=URLPolicy(enforce_https=False),
    )
    assert normalize_public_url("https://other.example.com/a", config) == "http://portal.example.com/a"


def test_tracking_strip_toggle() -> None:
    config = _config(URLPolicy(strip_tracking_params=False))
    assert (
        normalize_public_url("/p?utm_source=x&gclid=1&fbclid=2", config)
        == "https://portal.example.com/p?utm_source=x&gclid=1&fbclid=2"
    )


def test_no_allowlist_keeps_non_tracking_params() -> None:
    config = _config(URLPolicy())
    assert normalize_public_url("/p?a=1&b=2&utm_campaign=x", config) == "https://portal.example.com/p?a=1&b=2"


def test_malformed_url_raises_error() -> None:
    config = _config()
    with pytest.raises(SEOPayloadError):
        normalize_public_url("https:///broken", config)


def test_host_is_always_enforced_for_absolute_input() -> None:
    config = _config()
    normalized = normalize_public_url("https://evil.example.org/path", config)
    assert normalized == "https://portal.example.com/path"


def test_can_disable_duplicate_slash_collapse_and_lowercase() -> None:
    policy = URLPolicy(collapse_duplicate_slashes=False, lowercase_paths=False, trailing_slash="preserve")
    assert normalize_path("//Blog//Post//", policy) == "//Blog//Post//"


# --- Sub-path public_base_url tests (issue #1 / #9) ---

def _subpath_config(**kwargs) -> SEOConfig:
    defaults = dict(
        canonical_host="example.com",
        public_base_url="https://example.com/blog",
        url_policy=URLPolicy(),
    )
    defaults.update(kwargs)
    return SEOConfig(**defaults)


def test_subpath_prepends_base_path() -> None:
    config = _subpath_config()
    assert normalize_public_url("/page", config) == "https://example.com/blog/page"


def test_subpath_root_route() -> None:
    config = _subpath_config()
    assert normalize_public_url("/", config) == "https://example.com/blog"


def test_subpath_trailing_slash_always() -> None:
    config = _subpath_config(url_policy=URLPolicy(trailing_slash="always"))
    assert normalize_public_url("/page", config) == "https://example.com/blog/page/"


def test_subpath_preserves_base_path_with_absolute_input() -> None:
    config = _subpath_config()
    assert normalize_public_url("https://evil.org/path?q=1", config) == "https://example.com/blog/path?q=1"


def test_subpath_idempotent() -> None:
    config = _subpath_config()
    first = normalize_public_url("/A//B/", config)
    second = normalize_public_url(first, config)
    assert first == second


def test_subpath_with_trailing_slash_in_public_base_url() -> None:
    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com/blog/",
        url_policy=URLPolicy(),
    )
    assert normalize_public_url("/page", config) == "https://example.com/blog/page"


def test_subpath_relative_path() -> None:
    config = _subpath_config()
    assert normalize_public_url("page", config) == "https://example.com/blog/page"


def test_subpath_double_slash_input_preserves_netloc() -> None:
    config = _subpath_config()
    assert normalize_public_url("//Page//Sub", config) == "https://example.com/blog/sub"


# --- Property-based normalization tests (issue #10) ---

def test_idempotency_multiple_inputs() -> None:
    config = _config()
    inputs = [
        "/A//B/?utm_campaign=x",
        "https://evil.com/Path/?fbclid=1&q=2",
        "/",
        "relative/path?gclid=abc",
    ]
    for url in inputs:
        first = normalize_public_url(url, config)
        second = normalize_public_url(first, config)
        assert first == second, f"Idempotency failed for {url}"


def test_scheme_uniformity_enforce_https() -> None:
    config = _config()
    inputs = [
        "http://other.com/a",
        "https://other.com/b",
        "/c",
        "//d",
    ]
    for url in inputs:
        result = normalize_public_url(url, config)
        assert result.startswith("https://"), f"Scheme not https for {url}: {result}"


def test_host_always_enforced() -> None:
    config = _config()
    inputs = [
        "https://evil.com/path",
        "http://malicious.org/other",
        "/relative",
    ]
    for url in inputs:
        result = normalize_public_url(url, config)
        assert result.startswith("https://portal.example.com/"), f"Host not enforced for {url}: {result}"


# ── Edge-case coverage ─────────────────────────────────────────────────────


def test_normalize_path_non_string_raises_error() -> None:
    import pytest
    from seoslug import URLPolicyError
    with pytest.raises(URLPolicyError, match="path must be a string"):
        normalize_path(123, URLPolicy())  # type: ignore[arg-type]


def test_normalize_public_url_non_string_raises_error() -> None:
    import pytest
    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )
    with pytest.raises(SEOPayloadError, match="url_or_path must be a non-empty string"):
        normalize_public_url("", config)


# ── Detrack integration tests ──────────────────────────────────────────────


def test_try_import_detrack_succeeds(monkeypatch) -> None:
    import seoslug.normalization as norm
    monkeypatch.setattr(norm, "_DETRACK_AVAILABLE", False)
    monkeypatch.setattr(norm, "_detrack_clean_query", None)
    assert norm._try_import_detrack() is True
    assert norm._DETRACK_AVAILABLE is True
    assert norm._detrack_clean_query is not None


def test_try_import_detrack_fails(monkeypatch) -> None:
    import seoslug.normalization as norm
    monkeypatch.setattr(norm, "_DETRACK_AVAILABLE", False)
    monkeypatch.setattr(norm, "_detrack_clean_query", None)
    import builtins
    original_import = builtins.__import__

    def _mock_import(name, *args, **kwargs):
        if name == "detrack":
            raise ImportError("mock: detrack not available")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _mock_import)
    assert norm._try_import_detrack() is False
    assert norm._DETRACK_AVAILABLE is False


def test_clean_query_detrack_path(monkeypatch) -> None:
    import seoslug.normalization as norm
    monkeypatch.setattr(norm, "_DETRACK_AVAILABLE", False)
    monkeypatch.setattr(norm, "_detrack_clean_query", None)
    result = norm._clean_query("utm_source=x&keep=1")
    assert "utm_source" not in result
    assert "keep=1" in result


def test_clean_query_builtin_empty_string() -> None:
    import seoslug.normalization as norm
    assert norm._clean_query_builtin("") == ""


def test_clean_query_builtin_filters_tracking() -> None:
    import seoslug.normalization as norm
    result = norm._clean_query_builtin("utm_source=x&keep=1&gclid=abc")
    assert "utm_source" not in result
    assert "gclid" not in result
    assert "keep=1" in result


def test_clean_query_fallback_path(monkeypatch) -> None:
    import seoslug.normalization as norm
    monkeypatch.setattr(norm, "_DETRACK_AVAILABLE", False)
    monkeypatch.setattr(norm, "_detrack_clean_query", None)
    import builtins
    original_import = builtins.__import__

    def _mock_import(name, *args, **kwargs):
        if name == "detrack":
            raise ImportError("mock: detrack not available")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", _mock_import)
    result = norm._clean_query("fbclid=xyz&keep=2")
    assert "fbclid" not in result
    assert "keep=2" in result
