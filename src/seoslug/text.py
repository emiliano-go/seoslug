"""Text extraction utilities for seoslug."""

import re
from typing import Protocol


from .exceptions import SEOPayloadError

_WS_RE = re.compile(r"\s+")

_LXML_AVAILABLE: bool = False
_lxml_fromstring = None
_lxml_xpath = None
_lxml_drop_tree = None


def _try_import_lxml() -> None:
    global _LXML_AVAILABLE, _lxml_fromstring, _lxml_xpath, _lxml_drop_tree
    try:
        import lxml.html
        _lxml_fromstring = lxml.html.fromstring
        _LXML_AVAILABLE = True
    except ImportError:
        _LXML_AVAILABLE = False


class TextExtractor(Protocol):
    def extract(self, html: str) -> str: ...


_extractor: TextExtractor | None = None


def set_text_extractor(extractor: TextExtractor | None) -> None:
    global _extractor
    _extractor = extractor


def _html_to_text_lxml(html: str) -> str:
    doc = _lxml_fromstring(html)
    for elem in doc.xpath("//script | //style"):
        _lxml_drop_tree(elem) if _lxml_drop_tree else elem.drop_tree()
    parts = [t.strip() for t in doc.itertext() if t.strip()]
    return _WS_RE.sub(" ", " ".join(parts)).strip()


# Common block-level tags that naturally separate text
_BLOCK_TAGS = frozenset({
    "p", "div", "h1", "h2", "h3", "h4", "h5", "h6",
    "li", "blockquote", "section", "article", "header", "footer",
    "br", "tr", "td", "table", "ul", "ol", "dl", "dd", "dt",
})
_SCRIPT_STYLE_RE = re.compile(r'<script[^>]*>.*?</script>|<style[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r'<[^>]*>')


def _html_to_text_pure(html: str) -> str:
    stripped = _SCRIPT_STYLE_RE.sub("", html)
    stripped = stripped.replace("&nbsp;", " ")
    stripped = stripped.replace("&amp;", "&")
    stripped = stripped.replace("&lt;", "<")
    stripped = stripped.replace("&gt;", ">")
    stripped = stripped.replace("&quot;", '"')
    stripped = stripped.replace("&#39;", "'")
    stripped = _TAG_RE.sub(" ", stripped)
    stripped = _WS_RE.sub(" ", stripped)
    return stripped.strip()


def html_to_text(html: str | None) -> str:
    if html is None:
        return ""
    if not isinstance(html, str):
        raise SEOPayloadError("html must be a string or None")
    if not html:
        return ""
    if _extractor is not None:
        try:
            return _extractor.extract(html)
        except Exception:
            return ""
    if _lxml_fromstring is not None or _LXML_AVAILABLE:
        if _lxml_fromstring is None:
            _try_import_lxml()
        if _lxml_fromstring is not None:
            try:
                return _html_to_text_lxml(html)
            except Exception:
                return ""
    try:
        return _html_to_text_pure(html)
    except Exception:
        return ""


def build_description_snippet(body_html: str | None, max_length: int = 160) -> str:
    if not isinstance(max_length, int) or max_length <= 0:
        raise SEOPayloadError("max_length must be a positive integer")
    text = html_to_text(body_html).rstrip()
    if len(text) <= max_length:
        return text
    if max_length <= 3:
        return "." * max_length
    return text[: max_length - 3] + "..."
