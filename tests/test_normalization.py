"""Tests for URL normalization."""

from seoslug import SEOConfig, URLPolicy, normalize_path, normalize_public_url
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


def test_malformed_url_raises_value_error() -> None:
    config = _config()
    with pytest.raises(ValueError):
        normalize_public_url("https:///broken", config)
