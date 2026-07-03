---
seo:
  title: Quartz integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/quartz/
  robots: index,follow
  og:
    type: website
    title: Quartz integration - seoslug
    description: Quartzhttps://quartz.jzhao.xyz is a static site generator for Obsidian
      vaults, built with TypeScript and Preact. Use seoslug at build time to add JSON-LD...
    url: https://seoslug.emiliano-go.com/integrations/quartz/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Quartz integration - seoslug
    description: Quartzhttps://quartz.jzhao.xyz is a static site generator for Obsidian
      vaults, built with TypeScript and Preact. Use seoslug at build time to add JSON-LD...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: Quartzhttps://quartz.jzhao.xyz is a static site generator for Obsidian
    vaults, built with TypeScript and Preact. Use seoslug at build time to add JSON-LD...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Quartz integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/quartz/
    description: Quartzhttps://quartz.jzhao.xyz is a static site generator for Obsidian
      vaults, built with TypeScript and Preact. Use seoslug at build time to add JSON-LD...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Quartz integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Quartzhttps://quartz.jzhao.xyz is a static site generator for Obsidian\
  \ vaults, built with TypeScript and Preact. Use seoslug at build time to add JSON-LD...\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/quartz/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Quartz integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Quartzhttps://quartz.jzhao.xyz is\
  \ a static site generator for Obsidian vaults, built with TypeScript and Preact.\
  \ Use seoslug at build time to add JSON-LD...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/quartz/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Quartz integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Quartzhttps://quartz.jzhao.xyz is a static\
  \ site generator for Obsidian vaults, built with TypeScript and Preact. Use seoslug\
  \ at build time to add JSON-LD...\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Quartz integration - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/quartz/\"\
  ,\n  \"description\": \"Quartzhttps://quartz.jzhao.xyz is a static site generator\
  \ for Obsidian vaults, built with TypeScript and Preact. Use seoslug at build time\
  \ to add JSON-LD...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Quartz integration

[Quartz](https://quartz.jzhao.xyz) is a static site generator for Obsidian vaults, built with TypeScript and Preact. Use seoslug at build time to add JSON-LD structured data, Open Graph, Twitter Card, canonical, and robots metadata to every page.

## Built-in builder (recommended)

seoslug ships a `QuartzBuilder` class at `seoslug.contrib.quartz` that handles content scanning, YAML frontmatter parsing, SEO payload building, and frontmatter injection in a single call:

```python
from seoslug.contrib.quartz import QuartzBuilder

builder = QuartzBuilder(
    content_dir="content",
    site_url="https://yoursite.com",
    site_name="Your Site",
)
builder.build()
```

The class accepts all `SEOConfig` fields as keyword arguments and exposes `dry_run` and `debug_dir` modes. The `debug_dir` option (e.g. `debug_dir=".seo-debug"`) writes a per-page JSON file with the SEO payload dict, matching the Zensical extension behaviour.

See the `QuartzBuilder` API reference for all options.

## Manual pre-build script (alternative)

If you prefer full control over the generation logic, write a custom script that imports seoslug directly.

### How it works

A pre-build Python script iterates all Markdown files in your vault, builds an SEO payload for each page using seoslug, and writes the rendered HTML into the file's frontmatter under a `seo_html` key. A small modification to Quartz's `Head.tsx` component checks for this key and injects the tags when present, falling back to Quartz's built-in generation otherwise.

### Setup

#### 1. Write the SEO generation script

Create `scripts/generate_seo.py`. This script handles Obsidian-flavored Markdown (frontmatter delimited with `---`) and maps file paths to page URLs:

```python
"""Pre-build: generates SEO frontmatter for Quartz content via seoslug."""

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
        trailing_slash="always",
    ),
    site_name=SITE_NAME,
    default_og_image=OGImage(
        url=f"{SITE_URL}/static/og-image.png",
        width=1200,
        height=630,
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
    rel = filepath.relative_to(CONTENT_DIR)
    stem = Path(*rel.parts).with_suffix("")
    if stem.name == "index":
        stem = stem.parent
    if not str(stem):
        return "/"
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
        description = meta.get("description") or meta.get("socialDescription") or extract_excerpt(body)
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

#### 2. Modify the Head component

Edit `quartz/components/Head.tsx` to check for `seo_html` in the page frontmatter. When present, inject it directly. Otherwise, fall back to the default Quartz head logic:

```tsx
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

export default (() => {
  const Head: QuartzComponent = ({ fileData, externalResources, cfg }: QuartzComponentProps) => {
    const { frontmatter } = fileData
    const baseDir = cfg.baseUrl ?? ""

    // If seoslug has pre-rendered the full SEO block, inject it directly
    if (frontmatter?.seo_html) {
      return (
        <head>
          <meta charSet="utf-8" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <base href={baseDir} />
          <style>{cfg.theme?.cdnCaching ? "" : ""}</style>
          <dangerouslySetInnerHTML html={frontmatter.seo_html} />
          {externalResources.map((resource) => {
            if (resource.css) {
              return <link rel="stylesheet" href={resource.css} />
            }
            if (resource.js) {
              return <script src={resource.js} />
            }
            if (resource.additionalHead) {
              return <>{resource.additionalHead}</>
            }
          })}
        </head>
      )
    }

    // Fall through to default Quartz head generation
    const title = frontmatter?.title ?? "Untitled"
    const description = frontmatter?.socialDescription ?? frontmatter?.description ?? ""
    const socialUrl = frontmatter?.permalink ?? `https://${baseDir}${fileData.slug!}`

    return (
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>{title}</title>
        <meta name="og:site_name" content={cfg.pageTitle} />
        <meta property="og:title" content={title} />
        <meta property="og:type" content="website" />
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={title} />
        <meta name="twitter:description" content={description} />
        <meta property="og:description" content={description} />
        <meta property="og:image:alt" content={description} />
        <meta property="twitter:domain" content={baseDir} />
        <meta property="og:url" content={socialUrl} />
        <meta property="twitter:url" content={socialUrl} />
        <meta name="description" content={description} />
        <base href={baseDir} />
        {externalResources.map((resource) => {
          if (resource.css) {
            return <link rel="stylesheet" href={resource.css} />
          }
          if (resource.js) {
            return <script src={resource.js} />
          }
          if (resource.additionalHead) {
            return <>{resource.additionalHead}</>
          }
        })}
      </head>
    )
  }

  return Head
}) satisfies QuartzComponentConstructor
```

When `frontmatter.seo_html` is present, seoslug provides the complete set of tags (title, description, canonical, robots, Open Graph, Twitter Card, JSON-LD). Pages without it use Quartz's default generation.

#### 3. Add to package.json

Add the pre-build step to your `package.json` scripts:

```json
{
  "scripts": {
    "build:seo": "python scripts/generate_seo.py",
    "build": "npm run build:seo && quartz build",
    "serve": "npm run build:seo && quartz build --serve"
  }
}
```

#### 4. Update the CI workflow

Add the Python setup and seoslug install to your deployment pipeline:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: '3.x'
- run: pip install "seoslug>=2.0.1" pyyaml
- run: python scripts/generate_seo.py
- run: npm ci
- run: npm run build
```

## What gets added

Quartz generates Open Graph and Twitter Card tags natively. seoslug adds:

- `<link rel="canonical">` for canonical URL normalization
- `<meta name="robots">` with index/follow directives
- `<script type="application/ld+json">` with schema.org structured data (WebPage, Organization, BreadcrumbList)
- `<meta name="twitter:site">` for the Twitter handle
- `<meta property="og:locale">` for the content locale
- Consistent URL normalization through `SEOConfig.url_policy`
