"""Tests for text extraction utilities."""

from seoslug.text import build_description_snippet, html_to_text


def test_html_to_text_strips_tags_and_script_content() -> None:
    html = "<h1>Hello</h1><script>alert('x')</script><p>World</p>"
    assert html_to_text(html) == "Hello World"


def test_snippet_truncation() -> None:
    text = "<p>" + ("a" * 200) + "</p>"
    snippet = build_description_snippet(text, max_length=20)
    assert snippet.endswith("...")
    assert len(snippet) == 20
