"""Pre-build: generates SEO frontmatter for docs pages via seoslug.

Run before ``zensical build`` to inject per-page SEO metadata (Open Graph,
Twitter Cards, JSON-LD, canonical, robots) into each Markdown file's YAML
frontmatter.  Idempotent: skips writing if the computed payload matches
what's already in the file.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml
from seoslug import (
    SEOConfig,
    URLPolicy,
    SEOEntity,
    OGImage,
    Robots,
    build_seo_payload,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = PROJECT_ROOT / "docs"
SITE_URL = "https://seoslug.emiliano-go.com"
SITE_NAME = "seoslug"

SEO_CONFIG = SEOConfig(
    canonical_host="seoslug.emiliano-go.com",
    public_base_url=SITE_URL,
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="always",
    ),
    site_name=SITE_NAME,
    default_og_image=OGImage(
        url=f"{SITE_URL}/assets/images/og-image.png",
        width=1408,
        height=768,
        alt="seoslug documentation",
    ),
    publisher_name="Emiliano Gandini Outeda",
    publisher_logo=f"{SITE_URL}/assets/images/og-image.png",
    title_template="{title} - seoslug",
    default_robots=Robots(index=True, follow=True),
    locale="en_US",
    twitter_site="@emiliano_gando",
    emit_warnings=True,
)

FM_RE = re.compile(
    r"^-{3}[ \r\t]*?\n(.*?\r?\n)(?:\.{3}|-{3})[ \r\t]*\n",
    re.UNICODE | re.DOTALL,
)


def route_path_from_file(filepath: Path) -> str:
    rel = filepath.relative_to(DOCS_DIR)
    parts = list(rel.parts)
    if parts[-1] == "index.md":
        parts.pop()
        if not parts:
            return "/"
        return "/" + "/".join(parts) + "/"
    stem = Path(*parts).with_suffix("")
    return "/" + str(stem) + "/"


def first_heading(text: str) -> str | None:
    match = re.search(r"^#\s+(.+)", text, re.MULTILINE)
    if not match:
        return None
    title = match.group(1).strip()
    title = re.sub(r"[`*_]", "", title)
    return title


def extract_excerpt(body: str, max_chars: int = 160) -> str:
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


def read_meta_and_body(filepath: Path) -> tuple[dict, str]:
    text = filepath.read_text(encoding="utf-8")
    meta: dict = {}
    body = text
    if text.startswith("---"):
        match = FM_RE.match(text)
        if match:
            try:
                parsed = yaml.load(match.group(1), yaml.SafeLoader)
                if isinstance(parsed, dict):
                    meta = parsed
            except Exception:
                pass
            body = text[match.end():].lstrip("\n")
    return meta, body


def build_seo_frontmatter(meta: dict, body: str, route_path: str) -> dict | None:
    title = meta.get("title") or first_heading(body) or SITE_NAME
    description = meta.get("description") or extract_excerpt(body)
    entity_type = "home" if route_path == "/" else "page"

    entity = SEOEntity(
        entity_type=entity_type,
        title=title,
        excerpt=description or None,
    )
    payload = build_seo_payload(entity, route_path, SEO_CONFIG)

    if payload is None:
        return None

    return {
        "seo_html": payload.render_html(),
        "seo": payload.to_dict(),
    }


def main() -> int:
    changed = 0
    skipped = 0
    errors = 0

    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        rel_path = md_file.relative_to(PROJECT_ROOT)
        meta, body = read_meta_and_body(md_file)
        route = route_path_from_file(md_file)
        result = build_seo_frontmatter(meta, body, route)

        if result is None:
            print(f"  SKIP  {rel_path}  (no payload generated)")
            skipped += 1
            continue

        new_seo = result["seo"]
        new_seo_html = result["seo_html"]

        existing_seo = meta.get("seo", {})
        existing_seo_html = meta.get("seo_html")

        new_dumped = yaml.dump(new_seo, sort_keys=True)
        existing_dumped = yaml.dump(existing_seo, sort_keys=True)

        if new_dumped == existing_dumped and new_seo_html == existing_seo_html:
            skipped += 1
            continue

        meta["seo"] = new_seo
        meta["seo_html"] = new_seo_html
        fm_dump = yaml.dump(
            meta,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        fm_text = f"---\n{fm_dump}---\n\n{body}"
        md_file.write_text(fm_text, encoding="utf-8")
        print(f"  WRITE {rel_path}")
        changed += 1

    print(f"\nDone: {changed} changed, {skipped} skipped, {errors} errors")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
