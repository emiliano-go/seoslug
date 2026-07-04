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


# ---------------------------------------------------------------------------
# Additional coverage: html_to_text edge inputs
# ---------------------------------------------------------------------------


def test_html_to_text_none() -> None:
    assert html_to_text(None) == ""


def test_html_to_text_empty_string() -> None:
    assert html_to_text("") == ""


# ---------------------------------------------------------------------------
# set_text_extractor / custom extractor
# ---------------------------------------------------------------------------


def test_set_text_extractor_success() -> None:
    from seoslug.text import set_text_extractor

    class TestExtractor:
        def extract(self, html):
            return "custom result"

    set_text_extractor(TestExtractor())
    try:
        assert html_to_text("<p>ignored</p>") == "custom result"
    finally:
        set_text_extractor(None)


def test_set_text_extractor_exception_returns_empty() -> None:
    from seoslug.text import set_text_extractor

    class BrokenExtractor:
        def extract(self, html):
            raise ValueError("fail")

    set_text_extractor(BrokenExtractor())
    try:
        assert html_to_text("<p>ignored</p>") == ""
    finally:
        set_text_extractor(None)


def test_set_text_extractor_reset_none() -> None:
    from seoslug.text import set_text_extractor

    class TestExtractor:
        def extract(self, html):
            return "should not be used"

    set_text_extractor(TestExtractor())
    set_text_extractor(None)
    assert html_to_text("<p>Hello</p>") == "Hello"


# ---------------------------------------------------------------------------
# build_description_snippet: max_length <= 3
# ---------------------------------------------------------------------------


def test_build_description_snippet_max_length_three() -> None:
    snippet = build_description_snippet("<p>abcd</p>", max_length=3)
    assert snippet == "..."


def test_build_description_snippet_max_length_one() -> None:
    snippet = build_description_snippet("<p>abcd</p>", max_length=1)
    assert snippet == "."


def test_build_description_snippet_max_length_two() -> None:
    snippet = build_description_snippet("<p>abcd</p>", max_length=2)
    assert snippet == ".."


# ---------------------------------------------------------------------------
# _try_import_lxml
# ---------------------------------------------------------------------------


def test_try_import_lxml_success(monkeypatch) -> None:
    import seoslug.text as text_mod

    monkeypatch.setattr(text_mod, "_LXML_AVAILABLE", False)
    monkeypatch.setattr(text_mod, "_lxml_fromstring", None)
    text_mod._try_import_lxml()
    assert text_mod._LXML_AVAILABLE is True
    assert text_mod._lxml_fromstring is not None


def test_try_import_lxml_failure(monkeypatch) -> None:
    import builtins
    import seoslug.text as text_mod

    original_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "lxml.html":
            raise ImportError("mock: lxml not available")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    monkeypatch.setattr(text_mod, "_LXML_AVAILABLE", False)
    monkeypatch.setattr(text_mod, "_lxml_fromstring", None)
    text_mod._try_import_lxml()
    assert text_mod._LXML_AVAILABLE is False
    assert text_mod._lxml_fromstring is None


# ---------------------------------------------------------------------------
# _html_to_text_lxml
# ---------------------------------------------------------------------------


def test_html_to_text_lxml_direct(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    mock_doc = MagicMock()
    mock_doc.xpath.return_value = []
    mock_doc.itertext.return_value = ["Hello World"]

    mock_fromstring = MagicMock(return_value=mock_doc)
    monkeypatch.setattr(text_mod, "_lxml_fromstring", mock_fromstring)
    monkeypatch.setattr(text_mod, "_lxml_drop_tree", None)

    result = text_mod._html_to_text_lxml("<p>Hello World</p>")
    assert result == "Hello World"


def test_html_to_text_lxml_removes_script_style(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    script_mock = MagicMock()
    style_mock = MagicMock()
    mock_doc = MagicMock()
    mock_doc.xpath.return_value = [script_mock, style_mock]
    mock_doc.itertext.return_value = ["visible"]

    mock_fromstring = MagicMock(return_value=mock_doc)
    monkeypatch.setattr(text_mod, "_lxml_fromstring", mock_fromstring)
    monkeypatch.setattr(text_mod, "_lxml_drop_tree", None)

    result = text_mod._html_to_text_lxml("<script>bad</script><style>css</style><p>visible</p>")
    assert result == "visible"
    script_mock.drop_tree.assert_called_once()
    style_mock.drop_tree.assert_called_once()


def test_html_to_text_lxml_uses_drop_tree_callable(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    elem_mock = MagicMock()
    mock_doc = MagicMock()
    mock_doc.xpath.return_value = [elem_mock]
    mock_doc.itertext.return_value = ["text"]

    mock_fromstring = MagicMock(return_value=mock_doc)
    drop_tree_fn = MagicMock()

    monkeypatch.setattr(text_mod, "_lxml_fromstring", mock_fromstring)
    monkeypatch.setattr(text_mod, "_lxml_drop_tree", drop_tree_fn)

    text_mod._html_to_text_lxml("<script>x</script><p>text</p>")
    drop_tree_fn.assert_called_once_with(elem_mock)
    elem_mock.drop_tree.assert_not_called()


# ---------------------------------------------------------------------------
# html_to_text: lxml path
# ---------------------------------------------------------------------------


def test_html_to_text_lxml_path(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    mock_doc = MagicMock()
    mock_doc.xpath.return_value = []
    mock_doc.itertext.return_value = ["lxml result"]

    mock_fromstring = MagicMock(return_value=mock_doc)
    monkeypatch.setattr(text_mod, "_lxml_fromstring", mock_fromstring)

    result = html_to_text("<p>test</p>")
    assert result == "lxml result"


def test_html_to_text_lxml_exception_returns_empty(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    mock_fromstring = MagicMock(side_effect=Exception("parse error"))
    monkeypatch.setattr(text_mod, "_lxml_fromstring", mock_fromstring)

    result = html_to_text("<p>Hello World</p>")
    assert result == ""


def test_html_to_text_lxml_available_triggers_import(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    monkeypatch.setattr(text_mod, "_lxml_fromstring", None)
    monkeypatch.setattr(text_mod, "_LXML_AVAILABLE", True)

    mock_doc = MagicMock()
    mock_doc.xpath.return_value = []
    mock_doc.itertext.return_value = ["imported"]

    mock_fromstring = MagicMock(return_value=mock_doc)
    monkeypatch.setattr(text_mod, "_try_import_lxml", lambda: setattr(text_mod, "_lxml_fromstring", mock_fromstring))

    result = html_to_text("<p>test</p>")
    assert result == "imported"


# ---------------------------------------------------------------------------
# html_to_text: pure fallback exception
# ---------------------------------------------------------------------------


def test_html_to_text_pure_exception_returns_empty(monkeypatch) -> None:
    import seoslug.text as text_mod
    from unittest.mock import MagicMock

    monkeypatch.setattr(text_mod, "_lxml_fromstring", None)
    monkeypatch.setattr(text_mod, "_LXML_AVAILABLE", False)
    monkeypatch.setattr(text_mod, "_html_to_text_pure", MagicMock(side_effect=Exception("pure fail")))

    result = html_to_text("<p>Hello</p>")
    assert result == ""
