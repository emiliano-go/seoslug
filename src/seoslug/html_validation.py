"""HTML validation helpers for rendered SEO output."""

from __future__ import annotations

from html.parser import HTMLParser


class _JSONLDExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.blocks: list[str] = []
        self._in_script = False
        self._script_type: str | None = None
        self._buffer: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.lower() != "script":
            return
        attrs_map = {name.lower(): (value or "") for name, value in attrs}
        self._in_script = True
        self._script_type = attrs_map.get("type", "")
        self._buffer = []

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self._buffer.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() != "script" or not self._in_script:
            return
        if self._script_type and self._script_type.split(";", 1)[0].strip().lower() == "application/ld+json":
            self.blocks.append("".join(self._buffer).strip())
        self._in_script = False
        self._script_type = None
        self._buffer = []


def extract_jsonld_blocks(html: str) -> list[str]:
    """Extract raw JSON-LD script contents from HTML."""
    parser = _JSONLDExtractor()
    parser.feed(html)
    parser.close()
    return parser.blocks
