---
{}
---

# Nuxt integration

[Nuxt 3](https://nuxt.com) is a Vue.js framework with hybrid rendering, auto-imports, and a rich module ecosystem. Use seoslug during build or render time to populate Open Graph, Twitter Card, JSON-LD, canonical, and robots metadata via the `useHead` composable.

## How it works

Two approaches are available. For static sites, a pre-build Python script generates a JSON manifest that your Nuxt module reads at build time. For SSR/ISR, call seoslug directly inside `asyncData`, `useFetch`, or a server route. Both approaches use `useHead` to inject the tags into `<head>`.

## Static export (pre-build manifest)

### 1. Write the SEO generation script

Create `scripts/generate_seo.py`. This script walks your `content/` directory, builds an SEO payload per route, and writes a JSON manifest to `public/seo-manifest.json`:

```python
"""Pre-build: generates SEO JSON manifest for Nuxt."""
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

### 2. Create a composable

Create `composables/useSeo.ts` that loads the manifest and returns `useHead` calls:

```typescript
import seoManifest from "../public/seo-manifest.json";

export function useSeo(route?: string) {
  const path = route || useRoute().path;
  const seo = (seoManifest as Record<string, any>)[path];

  if (!seo) return;

  useHead({
    title: seo.title,
    meta: [
      { name: "robots", content: seo.robots },
      { property: "og:type", content: seo.og.type },
      { property: "og:title", content: seo.og.title },
      { property: "og:description", content: seo.og.description },
      { property: "og:url", content: seo.og.url },
      { property: "og:image", content: seo.og.image },
      { property: "og:site_name", content: seo.og.site_name },
      { property: "og:locale", content: seo.og.locale },
      { name: "twitter:card", content: seo.twitter.card },
      { name: "twitter:title", content: seo.twitter.title },
      { name: "twitter:description", content: seo.twitter.description },
      { name: "twitter:image", content: seo.twitter.image },
    ],
    link: [{ rel: "canonical", href: seo.canonical }],
    script: seo.schema_jsonld
      ? [
          {
            type: "application/ld+json",
            children: JSON.stringify(seo.schema_jsonld),
          },
        ]
      : [],
  });
}
```

### 3. Call the composable in a page

In any page or layout, call `useSeo`:

```vue
<script setup>
useSeo();
</script>

<template>
  <div>
    <h1>My Page</h1>
  </div>
</template>
```

For dynamic routes where the manifest key differs from the URL, pass the route explicitly:

```vue
<script setup>
const { slug } = useRoute().params;
const { data } = await useFetch(`/api/posts/${slug}`);
useSeo(`/blog/${slug}/`);
</script>
```

### 4. Nuxt module (optional)

For a reusable integration, wrap the logic in a Nuxt module. Create `modules/seo.ts`:

```typescript
import { defineNuxtModule, addImports } from "@nuxt/kit";

export default defineNuxtModule({
  meta: { name: "seoslug", version: "1.0.0" },
  setup() {
    addImports({ name: "useSeo", from: "./composables/useSeo" });
  },
});
```

Register it in `nuxt.config.ts`:

```typescript
export default defineNuxtConfig({
  modules: ["./modules/seo"],
});
```

## Runtime approach (SSR/ISR)

For dynamic content, call seoslug directly inside `asyncData` or a server route:

```python
# server/api/seo.py
from seoslug import SEOConfig, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="yoursite.com",
    public_base_url="https://yoursite.com/",
    site_name="Your Site",
    title_template="{title} | Your Site",
)

def get_page_seo(title: str, description: str, route: str) -> dict:
    entity = SEOEntity(entity_type="page", title=title, excerpt=description)
    payload = build_seo_payload(entity, route, config)
    return payload.to_dict() if payload else {}
```

Then call it from a Nitro server route or `asyncData` and pass the result to `useHead`.

## CI/CD

For the static manifest approach:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.x"
- run: pip install "seoslug>=2.0.1" pyyaml
- run: python scripts/generate_seo.py
- run: npm ci
- run: npm run generate
```

For SSR, install seoslug in your deployment image and import directly.
