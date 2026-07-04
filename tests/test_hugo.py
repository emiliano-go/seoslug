"""Tests for seoslug.contrib.hugo."""

from __future__ import annotations

from pathlib import Path

import pytest

from seoslug import SEOConfig, URLPolicy
from seoslug.contrib.hugo import HugoBuilder, build_hugo

_DUMMY_CONFIG = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com/",
    url_policy=URLPolicy(),
)


@pytest.fixture
def hugo_site(tmp_path: Path) -> Path:
    src = tmp_path / "content"
    src.mkdir()
    (src / "_index.md").write_text(
        "---\ntitle: Home\n---\n\nWelcome to the homepage.\n"
    )
    (src / "about.md").write_text(
        "+++\ntitle = \"About\"\ndescription = \"About this site\"\n+++\n\nAbout content.\n"
    )
    blog = src / "blog"
    blog.mkdir()
    (blog / "first.md").write_text(
        "---\ntitle: First Post\ndescription: My first post\n---\n\nPost content.\n"
    )
    return tmp_path


class TestHugoBuilder:
    def test_build_injects_seo_html(self, hugo_site: Path):
        count = build_hugo(
            content_dir=hugo_site / "content",
            site_url="https://example.com",
            site_name="Example",
        )
        assert count == 3

        for f in ["_index.md", "about.md", "blog/first.md"]:
            content = (hugo_site / "content" / f).read_text()
            assert "og:title" in content
            assert "twitter:card" in content

    def test_idempotent(self, hugo_site: Path):
        b = HugoBuilder(
            content_dir=hugo_site / "content",
            site_url="https://example.com",
            site_name="Example",
        )
        assert b.build() == 3
        assert b.build() == 0

    def test_dry_run_does_not_write(self, hugo_site: Path):
        b = HugoBuilder(
            content_dir=hugo_site / "content",
            site_url="https://example.com",
            site_name="Example",
            dry_run=True,
        )
        count = b.build()
        assert count == 3

        for md_file in (hugo_site / "content").rglob("*.md"):
            assert "seo_html:" not in md_file.read_text()

    def test_content_dir_not_found(self, tmp_path: Path):
        b = HugoBuilder(
            content_dir=tmp_path / "nonexistent",
            site_url="https://example.com",
            site_name="Example",
        )
        count = b.build()
        assert count == 0

    def test_toml_frontmatter_preserved_as_yaml(self, hugo_site: Path):
        about = hugo_site / "content" / "about.md"
        before = about.read_text()
        assert before.startswith("+++")

        build_hugo(
            content_dir=hugo_site / "content",
            site_url="https://example.com",
            site_name="Example",
        )

        after = about.read_text()
        assert after.startswith("---")
        assert "title: About" in after

    def test_no_title_falls_back_to_site_name(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "index.md").write_text("---\n---\n\nNo heading here.\n")

        build_hugo(
            content_dir=src,
            site_url="https://example.com",
            site_name="MyTest",
        )
        content = (src / "index.md").read_text()
        assert ': "<title>MyTest | MyTest</title>' in content

    def test_first_heading_used_when_no_title_in_frontmatter(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "page.md").write_text("---\n---\n\n# Hello World\n\nBody text.\n")

        build_hugo(
            content_dir=src,
            site_url="https://example.com",
            site_name="Test",
        )
        content = (src / "page.md").read_text()
        assert '<title>Hello World | Test</title>' in content

    def _seo_html(self, filepath: Path) -> str:
        text = filepath.read_text()
        parts = text.split("---", 2)
        if len(parts) < 3:
            return ""
        for line in parts[1].splitlines():
            if line.startswith("seo_html:"):
                val = line.partition(":")[2].strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                return val.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\')
        return ""

    def test_homepage_route(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "_index.md").write_text(
            "---\ntitle: Home\n---\n\nWelcome.\n"
        )

        b = HugoBuilder(
            content_dir=src,
            site_url="https://example.com",
            site_name="Test",
        )
        b.build()
        content = (src / "_index.md").read_text()
        assert "example.com/" in content

    def test_custom_seo_config(self, tmp_path: Path):
        from seoslug import SEOConfig, URLPolicy, Robots

        src = tmp_path / "content"
        src.mkdir()
        (src / "page.md").write_text(
            "---\ntitle: Custom\n---\n\nContent.\n"
        )

        config = SEOConfig(
            canonical_host="custom.example.com",
            public_base_url="https://custom.example.com/",
            url_policy=URLPolicy(trailing_slash="always"),
            site_name="Custom Site",
            title_template="{title} - Custom",
            default_robots=Robots(index=False, follow=False),
            auto_generate_schema=False,
        )

        build_hugo(
            content_dir=src,
            site_url="https://custom.example.com",
            site_name="Custom Site",
            config=config,
        )
        content = (src / "page.md").read_text()
        assert "Custom Site" in content
        assert "noindex,nofollow" in content


class TestHugoBuilderEdgeCases:
    def test_no_site_url(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        builder.site_url = ""
        assert builder._canonical_host() == "yoursite.com"

    def test_site_url_no_name_derives_from_host(self):
        builder = HugoBuilder(
            content_dir="/tmp/does-not-exist",
            site_url="https://example.com",
            config=_DUMMY_CONFIG,
        )
        assert builder._derive_site_name() == "Example"

    def test_parse_frontmatter_malformed_toml(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        text = "+++\n[[[\n+++\n\nBody.\n"
        meta, body = builder._parse_frontmatter(text)
        assert meta == {}
        assert body == "Body.\n"

    def test_parse_frontmatter_malformed_yaml(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        text = "---\n: invalid\n---\n\nBody.\n"
        meta, body = builder._parse_frontmatter(text)
        assert meta == {}
        assert body == "Body.\n"

    def test_first_heading_no_h1(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        assert builder._first_heading("Just some text.\n\nNo headings.\n") == ""

    def test_extract_excerpt_short(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        text = "Short text under limit."
        assert builder._extract_excerpt(text, max_chars=160) == "Short text under limit."

    def test_extract_excerpt_empty(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        assert builder._extract_excerpt("") == ""

    def test_extract_excerpt_break_at_boundary(self):
        builder = HugoBuilder(content_dir="/tmp/does-not-exist", config=_DUMMY_CONFIG)
        text = "This is a long text that should be broken at a word boundary since it exceeds the maximum character limit."
        result = builder._extract_excerpt(text, max_chars=40)
        assert result.endswith("...")
        assert len(result[:-3]) <= 40

    def test_no_title_no_h1_falls_back_to_site_name(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "page.md").write_text("---\n---\n\nNo heading here.\n")
        build_hugo(content_dir=src, site_url="https://example.com", site_name="SiteName")
        content = (src / "page.md").read_text()
        assert "SiteName" in content

    def test_build_hugo_convenience(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "index.md").write_text("---\ntitle: Test\n---\n\nBody.\n")
        count = build_hugo(content_dir=src, site_url="https://example.com", site_name="Example")
        assert count == 1
        content = (src / "index.md").read_text()
        assert "og:title" in content

    def test_build_payload_none(self, tmp_path: Path):
        import unittest.mock as mock
        src = tmp_path / "content"
        src.mkdir()
        (src / "page.md").write_text("---\ntitle: Test\n---\n\nBody.\n")
        builder = HugoBuilder(content_dir=src, site_url="https://example.com", site_name="Example")
        with mock.patch("seoslug.contrib.hugo.build_seo_payload", return_value=None):
            count = builder.build()
        assert count == 0

    def test_default_og_image(self):
        builder = HugoBuilder(
            content_dir="/tmp/does-not-exist",
            site_url="https://example.com",
            site_name="Example",
            default_og_image="https://example.com/image.png",
        )
        assert builder._config.default_og_image is not None
        assert builder._config.default_og_image.url == "https://example.com/image.png"
        assert builder._config.default_og_image.width == 1200
        assert builder._config.default_og_image.height == 630

    def test_constructor_derives_site_name_from_url(self):
        builder = HugoBuilder(
            content_dir="/tmp/does-not-exist",
            site_url="https://example.com",
        )
        assert builder._config.site_name == "Example"

    def test_derive_site_name_no_url(self):
        builder = HugoBuilder(
            content_dir="/tmp/does-not-exist",
            site_url="https://example.com",
            config=_DUMMY_CONFIG,
        )
        builder.site_url = ""
        assert builder._derive_site_name() == "My Site"

    def test_build_site_url_strips_trailing(self):
        builder = HugoBuilder(
            content_dir="/tmp/does-not-exist",
            site_url="https://example.com/",
        )
        assert builder._build_site_url() == "https://example.com"

    def test_route_from_path_index_in_subdir(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "posts" / "_index.md").parent.mkdir()
        (src / "posts" / "_index.md").write_text("")
        builder = HugoBuilder(content_dir=src, site_url="https://example.com", site_name="Example")
        route = builder._route_from_path(src / "posts" / "_index.md")
        assert route == "/posts"

