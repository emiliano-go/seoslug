---
seo:
  title: Astro integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/astro/
  robots: index,follow
  og:
    type: website
    title: Astro integration - seoslug
    description: Astrohttps://astro.build is a modern static site generator that ships
      zero JavaScript by default. Use seoslug at build time to generate SEO metadata,
      then...
    url: https://seoslug.emiliano-go.com/integrations/astro/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Astro integration - seoslug
    description: Astrohttps://astro.build is a modern static site generator that ships
      zero JavaScript by default. Use seoslug at build time to generate SEO metadata,
      then...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: Astrohttps://astro.build is a modern static site generator that ships
    zero JavaScript by default. Use seoslug at build time to generate SEO metadata,
    then...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Astro integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/astro/
    description: Astrohttps://astro.build is a modern static site generator that ships
      zero JavaScript by default. Use seoslug at build time to generate SEO metadata,
      then...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Astro integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Astrohttps://astro.build is a modern static site generator that ships\
  \ zero JavaScript by default. Use seoslug at build time to generate SEO metadata,\
  \ then...\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/astro/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Astro integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Astrohttps://astro.build is a modern\
  \ static site generator that ships zero JavaScript by default. Use seoslug at build\
  \ time to generate SEO metadata, then...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/astro/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Astro integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Astrohttps://astro.build is a modern static\
  \ site generator that ships zero JavaScript by default. Use seoslug at build time\
  \ to generate SEO metadata, then...\">\n<meta name=\"twitter:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta name=\"twitter:image:alt\"\
  \ content=\"seoslug documentation\">\n<meta name=\"twitter:site\" content=\"@emiliano_gando\"\
  >\n<script type=\"application/ld+json\">\n{\n  \"@context\": \"https://schema.org\"\
  ,\n  \"@type\": \"WebPage\",\n  \"name\": \"Astro integration - seoslug\",\n  \"\
  url\": \"https://seoslug.emiliano-go.com/integrations/astro/\",\n  \"description\"\
  : \"Astrohttps://astro.build is a modern static site generator that ships zero JavaScript\
  \ by default. Use seoslug at build time to generate SEO metadata, then...\",\n \
  \ \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\",\n \
  \ \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano Gandini\
  \ Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Astro integration

[Astro](https://astro.build) is a modern static site generator that ships zero JavaScript by default. Use seoslug at build time to generate SEO metadata, then render it via an Astro component in your layout.

## How it works

A pre-build Python script generates a JSON manifest of SEO payloads for all routes. A reusable `<Seo />` Astro component reads the manifest at build time and injects the tags into `<head>`. Place the component in your base layout and every page gets full SEO coverage with zero runtime overhead.

## Setup

### 1. Write the SEO generation script

Create `scripts/generate_seo.py`. This script walks your `src/content/` or `src/pages/` directory, builds an SEO payload per route, and writes a JSON manifest:

```python
"""Pre-build: generates SEO JSON manifest for Astro."""
from __future__ import annotations

import json
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
CONTENT_DIR = PROJECT_ROOT / "src" / "content"
PAGES_DIR = PROJECT_ROOT / "src" / "pages"
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
    rel = filepath.relative_to(PAGES_DIR)
    parts = list(rel.parts)
    if parts[-1] in ("index.md", "_index.md"):
        parts.pop()
        if not parts:
            return "/"
        return "/" + "/".join(parts) + "/"
    stem = Path(*parts).with_suffix("")
    return "/" + str(stem) + "/"


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


def main() -> int:
    manifest: dict[str, dict] = {}
    sources = []
    if CONTENT_DIR.exists():
        sources.extend(CONTENT_DIR.rglob("*.md"))
    if PAGES_DIR.exists():
        sources.extend(PAGES_DIR.rglob("*.md"))
        sources.extend(PAGES_DIR.rglob("*.mdx"))
        sources.extend(PAGES_DIR.rglob("*.astro"))

    for f in sorted(sources):
        route = route_path_from_file(f)
        text = f.read_text(encoding="utf-8")
        meta: dict = {}
        body = text
        if text.startswith("---"):
            m = FM_RE.match(text)
            if m:
                try:
                    parsed = yaml.safe_load(m.group(1))
                    if isinstance(parsed, dict):
                        meta = parsed
                except Exception:
                    pass
                body = text[m.end():].lstrip("\n")

        title = meta.get("title") or ""
        if not title:
            m = re.search(r"^#\s+(.+)", body, re.MULTILINE)
            if m:
                title = re.sub(r"[`*_]", "", m.group(1).strip())
        description = meta.get("description") or extract_excerpt(body)

        entity = SEOEntity(
            entity_type="page",
            title=title or SITE_NAME,
            excerpt=description or None,
        )
        payload = build_seo_payload(entity, route, SEO_CONFIG)
        if payload is None:
            continue
        manifest[route] = payload.to_dict()

    output = PROJECT_ROOT / "public" / "seo-manifest.json"
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Written {output} ({len(manifest)} routes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 2. Create the `<Seo />` component

Create `src/components/Seo.astro` that loads the manifest and renders the tags for the current route:

```astro
---
import seoManifest from "../../public/seo-manifest.json";

export interface Props {
  route?: string;
  fallbackTitle?: string;
}

const { route = Astro.url.pathname, fallbackTitle = "Default Title" } = Astro.props;
const seo = seoManifest[route];
---

{seo ? (
  <>
    <title>{seo.title}</title>
    <link rel="canonical" href={seo.canonical} />
    <meta name="robots" content={seo.robots} />
    <meta property="og:type" content={seo.og.type} />
    <meta property="og:title" content={seo.og.title} />
    <meta property="og:description" content={seo.og.description} />
    <meta property="og:url" content={seo.og.url} />
    <meta property="og:image" content={seo.og.image} />
    <meta property="og:site_name" content={seo.og.site_name} />
    <meta property="og:locale" content={seo.og.locale} />
    <meta name="twitter:card" content={seo.twitter.card} />
    <meta name="twitter:title" content={seo.twitter.title} />
    <meta name="twitter:description" content={seo.twitter.description} />
    <meta name="twitter:image" content={seo.twitter.image} />
    {seo.schema_jsonld && (
      <script type="application/ld+json" set:html={JSON.stringify(seo.schema_jsonld)} />
    )}
  </>
) : (
  <>
    <title>{fallbackTitle}</title>
    <meta name="robots" content="index,follow" />
  </>
)}
```

### 3. Use in your layout

Place `<Seo />` in your base layout so every page inherits the SEO tags:

```astro
---
import Seo from "../components/Seo.astro";
---
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width" />
    <Seo route={Astro.url.pathname} />
  </head>
  <body>
    <slot />
  </body>
</html>
```

For content routes with `getStaticPaths`, pass the route explicitly:

```astro
---
import Seo from "../../components/Seo.astro";
export async function getStaticPaths() {
  return [
    { params: { slug: "hello" } },
    { params: { slug: "world" } },
  ];
}
const { slug } = Astro.params;
---
<Seo route={`/${slug}/`} />
```

## CI/CD

Add the generation step before the Astro build:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.x"
- run: pip install "seoslug>=2.0.1" pyyaml
- run: python scripts/generate_seo.py
- run: npm ci
- run: npm run build
```
