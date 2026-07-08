"""Tests for HTML JSON-LD extraction."""

from seoslug.html_validation import extract_jsonld_blocks


def test_extract_jsonld_blocks_ignores_non_jsonld_scripts() -> None:
    html = """
    <html><head>
    <script>console.log('x')</script>
    <script type="application/ld+json">{"@type":"WebPage"}</script>
    <script type="application/json">{"ok":true}</script>
    </head></html>
    """
    assert extract_jsonld_blocks(html) == ['{"@type":"WebPage"}']
