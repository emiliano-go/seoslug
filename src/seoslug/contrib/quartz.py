"""Quartz integration for seoslug.

Generates SEO metadata for Quartz content files at build time. Handles
YAML (``---``) frontmatter only.

Usage::

    from seoslug.contrib.quartz import QuartzBuilder

    builder = QuartzBuilder(
        content_dir="content",
        site_url="https://yoursite.com",
        site_name="Your Site",
    )
    count = builder.build()
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload
from seoslug.schemas import OGImage, Robots


_FM_YAML_RE = re.compile(
    r"^-{3}[ \r\t]*?\n(.*?\r?\n)(?:\.{3}|-{3})[ \r\t]*\n",
    re.UNICODE | re.DOTALL,
)
_H1_RE = re.compile(r"^#\s+(.+)", re.MULTILINE)


@dataclass
class QuartzConfig:
    """Configuration for :class:`QuartzBuilder`."""

    content_dir: Path = Path("content")
    site_url: str = ""
    site_name: str = ""
    title_template: str = "{title} - {site_name}"
    publisher_name: str | None = None
    default_og_image: str | None = None
    locale: str = "en_US"
    twitter_site: str | None = None
    trailing_slash: str = "always"
    dry_run: bool = False
    debug_dir: str | None = None


class QuartzBuilder:
    """Build SEO metadata for Quartz content files.

    Walks the Quartz content directory, parses YAML frontmatter, builds
    SEO payloads with seoslug, and injects the rendered HTML into each
    file's frontmatter under a ``seo_html`` key.

    Args:
        content_dir: Path to Quartz ``content/`` directory.
        site_url: Full deployment URL (e.g. ``https://yoursite.com``).
        site_name: Site name for Open Graph.
        config: Pre-built :class:`~seoslug.SEOConfig`. If omitted it
            is constructed from the other keyword arguments.
        title_template: Title template with ``{title}`` and
            ``{site_name}`` placeholders.
        publisher_name: Publisher name for JSON-LD.
        default_og_image: Default Open Graph image URL.
        locale: Content locale (e.g. ``en_US``).
        twitter_site: Twitter handle for ``twitter:site``.
        trailing_slash: URL trailing slash policy (default ``always``
            for Quartz).
        dry_run: When True, log changes but do not write files.
        debug_dir: When set, writes per-page ``{slug}.json`` with the
            SEO payload dict (matching the Zensical extension behaviour).

    Note:
        ``QuartzBuilder`` is a library class. Use it by importing and
        instantiating directly; there is no CLI entry point.
    """

    def __init__(
        self,
        content_dir: str | Path = "content",
        site_url: str = "",
        site_name: str = "",
        config: SEOConfig | None = None,
        title_template: str | None = None,
        publisher_name: str | None = None,
        default_og_image: str | None = None,
        locale: str = "en_US",
        twitter_site: str | None = None,
        trailing_slash: str = "always",
        dry_run: bool = False,
        debug_dir: str | None = None,
    ):
        self.content_dir = Path(content_dir).resolve()
        self.site_url = site_url.rstrip("/")
        self.site_name = site_name
        self.dry_run = dry_run
        self.debug_dir = debug_dir
        self._changed = 0

        if config is not None:
            self._config = config
        else:
            resolved_site_name = site_name or self._derive_site_name()
            resolved_title_template = (
                title_template or "{title} - " + resolved_site_name
            )
            og_image = None
            if default_og_image:
                og_image = (
                    OGImage(url=default_og_image, width=1200, height=630)
                    if isinstance(default_og_image, str)
                    else default_og_image
                )

            self._config = SEOConfig(
                canonical_host=self._canonical_host(),
                public_base_url=self.site_url + "/" if self.site_url else "",
                url_policy=URLPolicy(
                    enforce_https=True,
                    lowercase_paths=True,
                    trailing_slash=trailing_slash,
                ),
                site_name=resolved_site_name or None,
                title_template=resolved_title_template,
                default_og_image=og_image,
                publisher_name=publisher_name,
                locale=locale,
                twitter_site=twitter_site,
                default_robots=Robots(index=True, follow=True),
                auto_generate_schema=True,
            )

    def _canonical_host(self) -> str:
        if not self.site_url:
            return "yoursite.com"
        return self.site_url.split("://", 1)[-1].split("/")[0]

    def _derive_site_name(self) -> str:
        if self.site_url:
            host = self._canonical_host()
            return host.split(".")[0].title()
        return "My Site"

    def _parse_frontmatter(self, text: str) -> tuple[dict[str, Any], str]:
        """Parse YAML frontmatter (``---`` delimited).

        Returns ``(meta, body)`` where *body* excludes the frontmatter.
        """
        m = _FM_YAML_RE.match(text)
        if m:
            try:
                import yaml
                meta = yaml.safe_load(m.group(1))
            except Exception:
                meta = {}
            body = text[m.end():].lstrip("\n")
            return meta if isinstance(meta, dict) else {}, body
        return {}, text

    def _route_from_path(self, filepath: Path) -> str:
        rel = filepath.relative_to(self.content_dir)
        parts = list(rel.parts)
        if parts[-1] == "index.md":
            parts.pop()
        else:
            parts[-1] = Path(parts[-1]).stem
        if not parts:
            return "/"
        return "/" + "/".join(str(p) for p in parts) + "/"

    def _first_heading(self, body: str) -> str:
        m = _H1_RE.search(body)
        if m:
            return re.sub(r"[`*_]", "", m.group(1).strip())
        return ""

    def _extract_excerpt(self, body: str, max_chars: int = 160) -> str:
        body = re.sub(r"^#\s+.*\n?", "", body, count=1).strip()
        para = re.split(r"\n\s*\n", body, maxsplit=1)[0].strip()
        clean = re.sub(r"[`*_\[\]()>|#{}]", "", para)
        clean = re.sub(r"\s+", " ", clean).strip()
        if not clean:
            return ""
        if len(clean) <= max_chars:
            return clean
        break_at = clean.rfind(" ", 0, max_chars)
        return clean[:break_at] + "..." if break_at > 0 else clean[:max_chars] + "..."

    def _build_site_url(self) -> str:
        return self.site_url.rstrip("/")

    def _write_debug(self, slug: str, payload: Any) -> None:
        if not self.debug_dir:
            return
        debug_path = self.content_dir.parent.resolve() / self.debug_dir / f"{slug}.json"
        debug_path.parent.mkdir(parents=True, exist_ok=True)
        debug_path.write_text(
            json.dumps(payload.to_dict(), indent=2, ensure_ascii=False)
        )

    def build(self) -> int:
        """Walk content files, build SEO payloads, inject into frontmatter.

        Returns the number of files updated.
        """
        self._changed = 0
        for md_file in sorted(self.content_dir.rglob("*.md")):
            text = md_file.read_text(encoding="utf-8")
            meta, body = self._parse_frontmatter(text)

            route = self._route_from_path(md_file)
            title = meta.get("title", "") or ""
            if not title:
                title = self._first_heading(body)
            description = meta.get("description", "") or (
                meta.get("socialDescription", "") or (
                    self._extract_excerpt(body) if body else ""
                )
            )

            entity_type = "home" if route == "/" else "page"

            entity = SEOEntity(
                entity_type=entity_type,
                title=title or self.site_name or "Untitled",
                excerpt=description or None,
            )
            payload = build_seo_payload(
                entity,
                route,
                self._config,
            )
            if payload is None:
                continue

            new_html = payload.render_html()
            old_html = meta.get("seo_html", "")
            if new_html == old_html:
                continue

            if self.dry_run:
                rel = md_file.relative_to(self.content_dir.parent)
                print(f"  WOULD UPDATE {rel}")
                self._changed += 1
                continue

            if self.debug_dir:
                slug = route.strip("/").replace("/", "_") or "index"
                self._write_debug(slug, payload)

            meta["seo_html"] = new_html
            self._write_frontmatter(md_file, meta, body)
            rel = md_file.relative_to(self.content_dir.parent)
            print(f"  WRITE {rel}")
            self._changed += 1

        return self._changed

    def _write_frontmatter(self, filepath: Path, meta: dict, body: str) -> None:
        import yaml
        fm_dump = yaml.dump(
            meta,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        filepath.write_text(f"---\n{fm_dump}---\n\n{body}", encoding="utf-8")


def build_quartz(
    content_dir: str | Path = "content",
    site_url: str = "",
    site_name: str = "",
    **kwargs: Any,
) -> int:
    """Convenience function for one-shot Quartz SEO generation.

    Shortcut for creating a :class:`QuartzBuilder` and calling
    :meth:`QuartzBuilder.build`.

    Returns the number of files updated.
    """
    builder = QuartzBuilder(
        content_dir=content_dir,
        site_url=site_url,
        site_name=site_name,
        **kwargs,
    )
    return builder.build()
