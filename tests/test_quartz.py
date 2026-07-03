"""Tests for seoslug.contrib.quartz."""

from __future__ import annotations

from pathlib import Path

import pytest

from seoslug.contrib.quartz import QuartzBuilder, build_quartz


@pytest.fixture
def quartz_site(tmp_path: Path) -> Path:
    src = tmp_path / "content"
    src.mkdir()
    (src / "index.md").write_text(
        "---\ntitle: Home\n---\n\nWelcome to the homepage.\n"
    )
    (src / "about.md").write_text(
        "---\ntitle: About\ndescription: About this site\n---\n\nAbout content.\n"
    )
    blog = src / "blog"
    blog.mkdir()
    (blog / "index.md").write_text(
        "---\ntitle: Blog\n---\n\nBlog listing.\n"
    )
    (blog / "first-post.md").write_text(
        "---\ntitle: First Post\n---\n\nPost content.\n"
    )
    return tmp_path


class TestQuartzBuilder:
    def test_build_injects_seo_html(self, quartz_site: Path):
        count = build_quartz(
            content_dir=quartz_site / "content",
            site_url="https://example.com",
            site_name="Example",
        )
        assert count == 4

        for f in ["index.md", "about.md", "blog/index.md", "blog/first-post.md"]:
            content = (quartz_site / "content" / f).read_text()
            assert "og:title" in content
            assert "twitter:card" in content

    def test_idempotent(self, quartz_site: Path):
        b = QuartzBuilder(
            content_dir=quartz_site / "content",
            site_url="https://example.com",
            site_name="Example",
        )
        assert b.build() == 4
        assert b.build() == 0

    def test_dry_run_does_not_write(self, quartz_site: Path):
        b = QuartzBuilder(
            content_dir=quartz_site / "content",
            site_url="https://example.com",
            site_name="Example",
            dry_run=True,
        )
        count = b.build()
        assert count == 4

        for md_file in (quartz_site / "content").rglob("*.md"):
            assert "seo_html:" not in md_file.read_text()

    def test_content_dir_not_found(self, tmp_path: Path):
        b = QuartzBuilder(
            content_dir=tmp_path / "nonexistent",
            site_url="https://example.com",
            site_name="Example",
        )
        count = b.build()
        assert count == 0

    def test_route_derivation(self, quartz_site: Path):
        b = QuartzBuilder(
            content_dir=quartz_site / "content",
            site_url="https://example.com",
            site_name="Example",
        )
        b.build()

        index = (quartz_site / "content" / "index.md").read_text()
        assert "example.com/" in index

        about = (quartz_site / "content" / "about.md").read_text()
        assert "example.com/about/" in about

        blog_index = (quartz_site / "content" / "blog" / "index.md").read_text()
        assert "example.com/blog/" in blog_index

        first = (quartz_site / "content" / "blog" / "first-post.md").read_text()
        assert "example.com/blog/first-post/" in first

    def test_social_description_fallback(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "page.md").write_text(
            "---\ntitle: Page\nsocialDescription: Social desc\n---\n\nBody.\n"
        )

        b = QuartzBuilder(
            content_dir=src,
            site_url="https://example.com",
            site_name="Test",
        )
        b.build()
        content = (src / "page.md").read_text()
        assert "Social desc" in content

    def test_no_title_falls_back_to_site_name(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "index.md").write_text("---\n---\n\nNo heading here.\n")

        build_quartz(
            content_dir=src,
            site_url="https://example.com",
            site_name="MySite",
        )
        content = (src / "index.md").read_text()
        assert ": \"<title>MySite - MySite</title>" in content

    def test_first_heading_used_when_no_title_in_frontmatter(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "page.md").write_text("---\n---\n\n# Hello World\n\nBody text.\n")

        build_quartz(
            content_dir=src,
            site_url="https://example.com",
            site_name="Test",
        )
        content = (src / "page.md").read_text()
        assert '<title>Hello World - Test</title>' in content

    def test_homepage_route(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "index.md").write_text(
            "---\ntitle: Home\n---\n\nWelcome.\n"
        )

        b = QuartzBuilder(
            content_dir=src,
            site_url="https://example.com",
            site_name="Test",
        )
        b.build()
        content = (src / "index.md").read_text()
        assert "example.com/" in content

    def test_debug_dir_writes_json(self, tmp_path: Path):
        src = tmp_path / "content"
        src.mkdir()
        (src / "index.md").write_text(
            "---\ntitle: Home\n---\n\nWelcome.\n"
        )
        (src / "about.md").write_text(
            "---\ntitle: About\n---\n\nAbout page.\n"
        )

        build_quartz(
            content_dir=src,
            site_url="https://example.com",
            site_name="Test",
            debug_dir=".seo-debug",
        )
        debug_root = tmp_path / ".seo-debug"
        assert (debug_root / "index.json").exists()
        assert (debug_root / "about.json").exists()

        import json
        data = json.loads((debug_root / "about.json").read_text())
        assert data["title"] == "About - Test"

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

        build_quartz(
            content_dir=src,
            site_url="https://custom.example.com",
            site_name="Custom Site",
            config=config,
        )
        content = (src / "page.md").read_text()
        assert "Custom Site" in content
        assert "noindex,nofollow" in content
