---
seo:
  title: Hugo integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/hugo/
  robots: index,follow
  og:
    type: website
    title: Hugo integration - seoslug
    description: Hugohttps://gohugo.io is a fast static site generator written in
      Go. Use seoslug at build time to generate Open Graph, Twitter Card, JSON-LD,
      and robots...
    url: https://seoslug.emiliano-go.com/integrations/hugo/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Hugo integration - seoslug
    description: Hugohttps://gohugo.io is a fast static site generator written in
      Go. Use seoslug at build time to generate Open Graph, Twitter Card, JSON-LD,
      and robots...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Hugohttps://gohugo.io is a fast static site generator written in Go.
    Use seoslug at build time to generate Open Graph, Twitter Card, JSON-LD, and robots...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Hugo integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/hugo/
    description: Hugohttps://gohugo.io is a fast static site generator written in
      Go. Use seoslug at build time to generate Open Graph, Twitter Card, JSON-LD,
      and robots...
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Hugo integration - seoslug</title>\n<meta name=\"description\" content=\"\
  Hugohttps://gohugo.io is a fast static site generator written in Go. Use seoslug\
  \ at build time to generate Open Graph, Twitter Card, JSON-LD, and robots...\">\n\
  <link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/hugo/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Hugo integration - seoslug\">\n\
  <meta property=\"og:description\" content=\"Hugohttps://gohugo.io is a fast static\
  \ site generator written in Go. Use seoslug at build time to generate Open Graph,\
  \ Twitter Card, JSON-LD, and robots...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/hugo/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"\
  og:image:width\" content=\"225\">\n<meta property=\"og:image:height\" content=\"\
  225\">\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"\
  og:locale\" content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Hugo integration - seoslug\">\n<meta name=\"\
  twitter:description\" content=\"Hugohttps://gohugo.io is a fast static site generator\
  \ written in Go. Use seoslug at build time to generate Open Graph, Twitter Card,\
  \ JSON-LD, and robots...\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Hugo integration - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/hugo/\"\
  ,\n  \"description\": \"Hugohttps://gohugo.io is a fast static site generator written\
  \ in Go. Use seoslug at build time to generate Open Graph, Twitter Card, JSON-LD,\
  \ and robots...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Hugo integration

[Hugo](https://gohugo.io) is a fast static site generator written in Go. Use seoslug at build time to generate Open Graph, Twitter Card, JSON-LD, and robots metadata for every page, then inject it via a template override.

## Built-in builder (recommended)

seoslug ships a `HugoBuilder` class at `seoslug.contrib.hugo` that handles content scanning, frontmatter parsing (TOML and YAML), SEO payload building, and frontmatter injection in a single call:

```python
from seoslug.contrib.hugo import HugoBuilder

builder = HugoBuilder(
    content_dir="content",
    site_url="https://yoursite.com",
    site_name="Your Site",
)
builder.build()
```

The class accepts all `SEOConfig` fields as keyword arguments and exposes a `dry_run` mode for inspection.

See the `HugoBuilder` API reference for all options.

## Manual pre-build script (alternative)

If you prefer full control over the generation logic, write a custom script that imports seoslug directly.

### 1. Write the SEO generation script

Create `scripts/generate_seo.py`. This script reads each content file under `content/`, builds an SEO payload with seoslug, and injects the rendered HTML into the frontmatter:

```python
"""Pre-build: generates SEO frontmatter for Hugo content via seoslug."""

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
CONTENT_DIR = PROJECT_ROOT / "content"
SITE_URL = "https://yoursite.com"
SITE_NAME = "Your Site"

SEO_CONFIG = SEOConfig(
    canonical_host="yoursite.com",
    public_base_url=SITE_URL,
    url_policy=URLPolicy(
        enforce_https=True,
        lowercase_paths=True,
        trailing_slash="never",
    ),
    site_name=SITE_NAME,
    default_og_image=OGImage(
        url=f"{SITE_URL}/images/default-og.png",
        width=1200,
        height=630,
    ),
    publisher_name="Your Name",
    title_template="{title} | Your Site",
    default_robots=Robots(index=True, follow=True),
    locale="en_US",
    twitter_site="@yourhandle",
)

FM_RE = re.compile(
    r"^-{3}[ \r\t]*?\n(.*?\r?\n)(?:\.{3}|-{3})[ \r\t]*\n",
    re.UNICODE | re.DOTALL,
)


def route_path_from_file(filepath: Path) -> str:
    rel = filepath.relative_to(CONTENT_DIR)
    parts = list(rel.parts)
    if parts[-1] == "_index.md":
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
    return re.sub(r"[`*_]", "", match.group(1).strip())


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
    for md_file in sorted(CONTENT_DIR.rglob("*.md")):
        rel_path = md_file.relative_to(PROJECT_ROOT)
        meta, body = read_meta_and_body(md_file)
        route = route_path_from_file(md_file)

        title = meta.get("title") or first_heading(body) or SITE_NAME
        description = meta.get("description") or extract_excerpt(body)
        entity_type = "post" if route != "/" and meta.get("entity_type") == "post" else "page"

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

### 2. Override the head partial

Create `layouts/_partials/head.html` in your project. This mirrors the default Hugo theme's head but checks for `seo_html` first:

```jinja
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1">

{{ if .Params.seo_html }}
  {{ .Params.seo_html | safeHTML }}
{{ else }}
  <title>{{ if .IsHome }}{{ site.Title }}{{ else }}{{ .Title }} | {{ site.Title }}{{ end }}</title>
  <meta name="description" content="{{ .Description | default site.Params.description }}">
  <link rel="canonical" href="{{ .Permalink }}">
  <meta name="robots" content="index,follow">

  {{ template "_internal/opengraph.html" . }}
  {{ template "_internal/twitter_cards.html" . }}

  {{ if eq .IsHome true }}
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "WebSite",
    "name": "{{ site.Title }}",
    "url": "{{ site.BaseURL }}"
  }
  </script>
  {{ end }}
{{ end }}
```

When a page has `seo_html` in its frontmatter, seoslug provides the complete set of tags (title, description, canonical, robots, Open Graph, Twitter Card, JSON-LD). Pages without it fall back to Hugo's built-in SEO partials.

### 3. Update the CI workflow

Add seoslug and the pre-build script to your deployment pipeline:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.x'
- run: pip install "seoslug>=2.0.1" pyyaml
- run: python scripts/generate_seo.py
- uses: peaceiris/actions-hugo@v3
  with:
    hugo-version: 'latest'
- run: hugo --minify
- uses: peaceiris/actions-gh-pages@v4
  with:
    github_token: ${{ secrets.GITHUB_TOKEN }}
    publish_dir: ./public
```

## Theme-specific: PaperMod

If you use the [PaperMod](https://github.com/adityatelange/hugo-PaperMod) theme, you can override `layouts/_partials/extend_head.html` instead of replacing `head.html` entirely. This keeps the theme's base structure and only appends seoslug tags:

```jinja
{{ if .Params.seo_html }}
  {{ .Params.seo_html | safeHTML }}
{{ end }}
```

Note that PaperMod's default `head.html` also generates Open Graph and Twitter Card tags inside a `{{ if hugo.IsProduction }}` guard. Using `extend_head.html` produces duplicate tags. For a clean integration, override `head.html` as shown above, or modify the theme's production guard by copying its `head.html` into `layouts/_partials/head.html` and adding the seoslug check.
