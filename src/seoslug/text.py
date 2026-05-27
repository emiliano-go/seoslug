"""Text extraction utilities for seoslug."""

import re

from lxml.html import fromstring

_WS_RE = re.compile(r"\s+")


def html_to_text(html: str | None) -> str:
    if html is None:
        return ""
    if not isinstance(html, str):
        raise ValueError("html must be a string or None")
    if not html:
        return ""
    doc = fromstring(html)
    for elem in doc.xpath("//script | //style"):
        elem.drop_tree()
    parts = [t.strip() for t in doc.itertext() if t.strip()]
    return _WS_RE.sub(" ", " ".join(parts)).strip()


def build_description_snippet(body_html: str | None, max_length: int = 160) -> str:
    if not isinstance(max_length, int) or max_length <= 0:
        raise ValueError("max_length must be a positive integer")
    text = html_to_text(body_html)
    if len(text) <= max_length:
        return text
    if max_length <= 3:
        return "." * max_length
    return text[: max_length - 3].rstrip() + "..."
