---
{}
---

# Next.js integration

[Next.js](https://nextjs.org) is a React framework for production. Use seoslug at build time with the Pages Router or at render time with the App Router to inject Open Graph, Twitter Card, JSON-LD, canonical, and robots metadata into every page.

## How it works

Next.js supports two routing models. For static export (Pages Router with `getStaticProps`), a pre-build Python script generates SEO payloads and writes them to a JSON manifest. Your page component imports the manifest and renders tags via `next/head`. For the App Router, call seoslug inside `generateMetadata` or a Server Component.

## Pages Router (static export)

### 1. Write the SEO generation script

Create `scripts/generate_seo.py`. This script walks your content or pages directory, builds an SEO payload for each route, and writes a single JSON manifest:

```python
"""Pre-build: generates SEO JSON manifest for Next.js."""
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
    for md_file in sorted(CONTENT_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
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

        route = route_path_from_file(md_file)
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

### 2. Load the manifest in `getStaticProps`

In your page component, import the manifest and select the entry for the current route:

```jsx
import seoManifest from "../../public/seo-manifest.json";

export async function getStaticProps({ params }) {
  const route = `/${params.slug}/`;
  const seo = seoManifest[route] || null;
  return { props: { seo } };
}
```

### 3. Render tags with `next/head`

Use `next/head` in your layout or page component to render the SEO tags:

```jsx
import Head from "next/head";

export default function Page({ seo, children }) {
  return (
    <>
      <Head>
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
              <script
                type="application/ld+json"
                dangerouslySetInnerHTML={{
                  __html: JSON.stringify(seo.schema_jsonld),
                }}
              />
            )}
          </>
        ) : (
          <>
            <title>Default title</title>
            <meta name="robots" content="index,follow" />
          </>
        )}
      </Head>
      {children}
    </>
  );
}
```

For repeated usage, extract the `Head` block into a reusable `<SeoHead seo={seo} />` component.

## App Router (runtime)

In the App Router, use `generateMetadata` to set metadata per route:

```typescript
import type { Metadata } from "next";
import { SEOConfig, SEOEntity, build_seo_payload } from "seoslug";

const SEO_CONFIG = new SEOConfig({
  canonical_host: "yoursite.com",
  public_base_url: "https://yoursite.com/",
  site_name: "Your Site",
  title_template: "{title} | Your Site",
});

export async function generateMetadata({ params }): Promise<Metadata> {
  const entity = new SEOEntity({
    entity_type: "page",
    title: "Page Title",
    excerpt: "Page description...",
  });
  const payload = build_seo_payload(entity, `/${params.slug}/`, SEO_CONFIG);
  if (!payload) return {};

  return {
    title: payload.title,
    description: payload.description,
    robots: payload.robots,
    openGraph: payload.og,
    twitter: payload.twitter,
    other: {
      "application/ld+json": JSON.stringify(payload.schema_jsonld),
    },
  };
}
```

The canonical link tag is rendered automatically by Next.js when you set `alternates.canonical`.

## CI/CD

Add the pre-build script to your deployment pipeline:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.x"
- run: pip install "seoslug>=2.0.1" pyyaml
- run: python scripts/generate_seo.py
- run: npm ci
- run: npm run build
```

For the App Router approach with runtime calls, install seoslug as a regular dependency (`npm install seoslug` or `pip install seoslug` in your Dockerfile) and import it directly in your Next.js API routes or Server Components.
