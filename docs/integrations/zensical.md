---
seo:
  title: Zensical integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/zensical/
  robots: index,follow
  og:
    type: website
    title: Zensical integration - seoslug
    description: Zensicalhttps://zensical.com is a modern static site generator with
      a Rust core and Python Markdown rendering. Use seoslug at build time to inject
      Open Graph,...
    url: https://seoslug.emiliano-go.com/integrations/zensical/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Zensical integration - seoslug
    description: Zensicalhttps://zensical.com is a modern static site generator with
      a Rust core and Python Markdown rendering. Use seoslug at build time to inject
      Open Graph,...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: Zensicalhttps://zensical.com is a modern static site generator with
    a Rust core and Python Markdown rendering. Use seoslug at build time to inject
    Open Graph,...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Zensical integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/zensical/
    description: Zensicalhttps://zensical.com is a modern static site generator with
      a Rust core and Python Markdown rendering. Use seoslug at build time to inject
      Open Graph,...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Zensical integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Zensicalhttps://zensical.com is a modern static site generator with\
  \ a Rust core and Python Markdown rendering. Use seoslug at build time to inject\
  \ Open Graph,...\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/zensical/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Zensical integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Zensicalhttps://zensical.com is a\
  \ modern static site generator with a Rust core and Python Markdown rendering. Use\
  \ seoslug at build time to inject Open Graph,...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/zensical/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Zensical integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Zensicalhttps://zensical.com is a modern\
  \ static site generator with a Rust core and Python Markdown rendering. Use seoslug\
  \ at build time to inject Open Graph,...\">\n<meta name=\"twitter:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta name=\"twitter:image:alt\"\
  \ content=\"seoslug documentation\">\n<meta name=\"twitter:site\" content=\"@emiliano_gando\"\
  >\n<script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\"\
  ,\n  \"@type\": \"WebPage\",\n  \"name\": \"Zensical integration - seoslug\",\n\
  \  \"url\": \"https://seoslug.emiliano-go.com/integrations/zensical/\",\n  \"description\"\
  : \"Zensicalhttps://zensical.com is a modern static site generator with a Rust core\
  \ and Python Markdown rendering. Use seoslug at build time to inject Open Graph,...\"\
  ,\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n\
  \  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Zensical integration

[Zensical](https://zensical.com) is a modern static site generator with a Rust core and Python Markdown rendering. Use seoslug at build time to inject Open Graph, Twitter Card, JSON-LD, canonical, and robots metadata into every page.

The seoslug documentation site itself uses this integration. The source is available in the [seoslug repository](https://github.com/emiliano-go/seoslug).

## How it works

seoslug ships a built-in Zensical Markdown extension at `seoslug.contrib.zensical`. Register it in your `zensical.toml` and it runs during Zensical's Markdown rendering pipeline. No pre-build step, no files modified on disk, no extra CI commands.

A custom template override (`overrides/main.html`) intercepts the `site_meta` block and outputs the seoslug-rendered HTML directly, replacing the default `<title>`, `<meta>`, `<link>`, and `<script>` tags.

The pattern works with any MkDocs-compatible theme because the block override lives in your own `overrides/` directory.

## Setup (inline extension)

This is the recommended approach. The extension runs during `zensical build` with no pre-build step.

### 1. Register the extension

Add `seoslug.contrib.zensical` to your `zensical.toml` under `[project.markdown_extensions]`:

```toml
[project.markdown_extensions]
tables = {}
"seoslug.contrib.zensical" = {
  canonical_host = "yoursite.com",
  public_base_url = "https://yoursite.com/",
  site_name = "Your Site",
  title_template = "{title} - Your Site",
  default_og_image = "https://yoursite.com/icon.png",
  publisher_name = "Your Name",
  locale = "en_US",
  twitter_site = "@yourhandle",
  auto_generate_schema = true,
  debug_dir = ".seo-debug",
}
```

The extension accepts these configuration keys:

| Key | Required | Default | Description |
|-----|----------|---------|-------------|
| `canonical_host` | Yes | -- | Hostname for canonical URLs (no scheme) |
| `public_base_url` | Yes | -- | Full deployment URL with scheme |
| `site_name` | No | `None` | Open Graph site name |
| `title_template` | No | `"{title}"` | Title template with `{title}` placeholder |
| `default_og_image` | No | `None` | Default OG image URL |
| `publisher_name` | No | `None` | Publisher name for JSON-LD |
| `locale` | No | `None` | Content locale (e.g. `en_US`) |
| `twitter_site` | No | `None` | Twitter handle for `twitter:site` |
| `auto_generate_schema` | No | `true` | Auto-generate JSON-LD schema |
| `debug_dir` | No | `None` | Directory for debug JSON files |

### 2. Create the template override

Create `overrides/main.html` that extends the base template and overrides the `site_meta` block:

```jinja
{% extends "base.html" %}

{% block site_meta %}
{% if page.meta and page.meta._seo_head %}
{{ page.meta._seo_head | safe }}
{% else %}
{{ super() }}
{% endif %}
{% endblock %}
```

The extension stores the rendered HTML in `page.meta["_seo_head"]`. The template outputs it when present and falls back to the theme's default otherwise.

### 3. Configure the theme directory

Add `custom_dir` to your theme in `zensical.toml`:

```toml
[project.theme]
variant = "modern"
custom_dir = "overrides"
```

### 4. Build

That is all. Run `zensical build` as normal:

```yaml
# .github/workflows/deploy-docs.yml
- run: pip install "seoslug>=2.0.1" zensical
- run: zensical build --clean
```

No pre-build script, no frontmatter injection, no extra CI step.

### Debug output

When `debug_dir` is set, the extension writes one JSON file per page with the full payload as `payload.to_dict()`:

```json
{
  "title": "Getting Started - Your Site",
  "canonical": "https://yoursite.com/getting-started/",
  "robots": "index,follow",
  "og": { "type": "website", "title": "...", ... },
  "twitter": { "card": "summary_large_image", ... },
  "schema_jsonld": { "@context": "https://schema.org", ... }
}
```

Add `.seo-debug/` to your `.gitignore`; these files are for local inspection, not committed.

## Alternative: pre-build script

If you prefer persisted frontmatter or need to inspect the SEO data before the build, use the pre-build script approach instead of the inline extension.

### 1. Write the SEO generation script

Create `scripts/generate_seo.py`:

```python
"""Pre-build: generates SEO frontmatter for docs pages via seoslug."""

from __future__ import annotations

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
SITE_URL = "https://yoursite.com"
SITE_NAME = "Your Site"

SEO_CONFIG = SEOConfig(
    canonical_host="yoursite.com",
    public_base_url=SITE_URL,
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="always",
    ),
    site_name=SITE_NAME,
    default_og_image=OGImage(
        url=f"{SITE_URL}/assets/icon.png",
        width=128,
        height=128,
    ),
    publisher_name="Your Name",
    title_template="{title} - Your Site",
    default_robots=Robots(index=True, follow=True),
    locale="en_US",
    twitter_site="@yourhandle",
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
                parsed = yaml.safe_load(match.group(1))
                if isinstance(parsed, dict):
                    meta = parsed
            except Exception:
                pass
            body = text[match.end():].lstrip("\n")
    return meta, body


def main() -> int:
    changed = 0
    for md_file in sorted(DOCS_DIR.rglob("*.md")):
        rel_path = md_file.relative_to(PROJECT_ROOT)
        meta, body = read_meta_and_body(md_file)
        route = route_path_from_file(md_file)

        title = meta.get("title") or first_heading(body) or SITE_NAME
        description = meta.get("description") or extract_excerpt(body)
        entity_type = "home" if route == "/" else "page"

        entity = SEOEntity(
            entity_type=entity_type,
            title=title,
            excerpt=description or None,
        )
        payload = build_seo_payload(entity, route, SEO_CONFIG)
        if payload is None:
            continue

        new_html = payload.render_html()
        old_html = meta.get("seo_html", "")
        if new_html == old_html:
            continue

        meta["seo_html"] = new_html
        fm_dump = yaml.dump(meta, default_flow_style=False, allow_unicode=True, sort_keys=False)
        md_file.write_text(f"---\n{fm_dump}---\n\n{body}", encoding="utf-8")
        print(f"  WRITE {rel_path}")
        changed += 1

    print(f"\nDone: {changed} changed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 2. Create the template override

Create `overrides/main.html` that extends the Zensical base template and overrides the `site_meta` block:

```jinja
{% extends "base.html" %}

{% block site_meta %}
{% if page.meta and page.meta.seo_html %}
{{ page.meta.seo_html | safe }}
{% else %}
{{ super() }}
{% endif %}
{% endblock %}
```

### 3. Configure Zensical

Add `custom_dir` to your theme in `zensical.toml`:

```toml
[project.theme]
variant = "modern"
custom_dir = "overrides"
```

### 4. Update the CI workflow

Add seoslug and the pre-build script to your deployment pipeline:

```yaml
- run: pip install "seoslug>=2.0.1" zensical
- run: python scripts/generate_seo.py
- run: zensical build --clean
```

The script runs before `zensical build`, so the frontmatter is already populated when Zensical renders the site.

## How it looks in the frontmatter

After the script runs, each Markdown file has a `seo_html` key in its frontmatter:

```yaml
---
title: Getting Started
description: How to install and configure seoslug.
seo_html: "<title>Getting Started - Your Site</title>\n<meta name=\"description\" ...>"
---
```

The template override injects this HTML into the `<head>` at build time. No runtime overhead, no JavaScript, no extra dependencies.
