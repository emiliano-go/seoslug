"""Tests for text extraction utilities."""

import pytest

from seoslug import SEOPayloadError
from seoslug.text import build_description_snippet, html_to_text


def test_html_to_text_strips_tags_and_script_content() -> None:
    html = "<h1>Hello</h1><script>alert('x')</script><p>World</p>"
    assert html_to_text(html) == "Hello World"


def test_snippet_truncation() -> None:
    text = "<p>" + ("a" * 200) + "</p>"
    snippet = build_description_snippet(text, max_length=20)
    assert snippet.endswith("...")
    assert len(snippet) == 20


def test_html_to_text_normalizes_whitespace_and_style() -> None:
    html = "<style>.x{color:red;}</style><p> Hello\n\tWorld </p>"
    assert html_to_text(html) == "Hello World"


def test_invalid_inputs_raise_error() -> None:
    with pytest.raises(SEOPayloadError):
        html_to_text(123)  # type: ignore[arg-type]
    with pytest.raises(SEOPayloadError):
        build_description_snippet("<p>ok</p>", max_length=0)


# --- Malformed HTML resilience (issue #3 / #11) ---

def test_malformed_html_unclosed_tags() -> None:
    assert html_to_text("<p>Hello<div>World") == "Hello World"


def test_malformed_html_invalid_entity() -> None:
    result = html_to_text("<p>&bogus;</p>")
    assert isinstance(result, str)


def test_malformed_html_garbage() -> None:
    result = html_to_text("<><>><")
    assert isinstance(result, str)


def test_malformed_html_empty_after_strip() -> None:
    result = html_to_text("<script>alert(1)</script>")
    assert result == ""


# --- Snippet truncation edge cases (issue #4) ---

def test_snippet_trailing_whitespace_normalized_by_html_to_text() -> None:
    snippet = build_description_snippet("<p>Hello World      </p>", max_length=20)
    assert snippet == "Hello World"


def test_snippet_exact_length_no_truncation() -> None:
    text = "a" * 20
    snippet = build_description_snippet(f"<p>{text}</p>", max_length=20)
    assert snippet == text
    assert len(snippet) == 20


def test_snippet_short_input() -> None:
    snippet = build_description_snippet("<p>Hi</p>", max_length=20)
    assert snippet == "Hi"


# --- Pure-Python extractor fallback ---

def test_pure_html_extractor_basic() -> None:
    from seoslug.text import _html_to_text_pure
    result = _html_to_text_pure("<h1>Hello</h1><p>World</p>")
    assert "Hello" in result
    assert "World" in result


def test_pure_html_extractor_strips_scripts() -> None:
    from seoslug.text import _html_to_text_pure
    result = _html_to_text_pure("<p>Hi</p><script>alert(1)</script><p>There</p>")
    assert "Hi" in result
    assert "There" in result
    assert "alert" not in result


def test_pure_html_extractor_strips_styles() -> None:
    from seoslug.text import _html_to_text_pure
    result = _html_to_text_pure("<style>.x{color:red;}</style><p>Hello</p>")
    assert result == "Hello"


def test_pure_html_extractor_handles_entities() -> None:
    from seoslug.text import _html_to_text_pure
    result = _html_to_text_pure("<p>Hello &amp; World</p>")
    assert result == "Hello & World"
