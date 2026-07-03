---
seo:
  title: SvelteKit integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/sveltekit/
  robots: index,follow
  og:
    type: website
    title: SvelteKit integration - seoslug
    description: SvelteKithttps://kit.svelte.dev is a framework for building Svelte
      applications with file-based routing, SSR, and static export. Use seoslug in
      your load...
    url: https://seoslug.emiliano-go.com/integrations/sveltekit/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: SvelteKit integration - seoslug
    description: SvelteKithttps://kit.svelte.dev is a framework for building Svelte
      applications with file-based routing, SSR, and static export. Use seoslug in
      your load...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: SvelteKithttps://kit.svelte.dev is a framework for building Svelte
    applications with file-based routing, SSR, and static export. Use seoslug in your
    load...
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: SvelteKit integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/sveltekit/
    description: SvelteKithttps://kit.svelte.dev is a framework for building Svelte
      applications with file-based routing, SSR, and static export. Use seoslug in
      your load...
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>SvelteKit integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"SvelteKithttps://kit.svelte.dev is a framework for building Svelte applications\
  \ with file-based routing, SSR, and static export. Use seoslug in your load...\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/sveltekit/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"SvelteKit integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"SvelteKithttps://kit.svelte.dev is\
  \ a framework for building Svelte applications with file-based routing, SSR, and\
  \ static export. Use seoslug in your load...\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/integrations/sveltekit/\">\n<meta property=\"og:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"SvelteKit integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"SvelteKithttps://kit.svelte.dev is a framework\
  \ for building Svelte applications with file-based routing, SSR, and static export.\
  \ Use seoslug in your load...\">\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"\
  twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"SvelteKit integration - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/sveltekit/\"\
  ,\n  \"description\": \"SvelteKithttps://kit.svelte.dev is a framework for building\
  \ Svelte applications with file-based routing, SSR, and static export. Use seoslug\
  \ in your load...\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# SvelteKit integration

[SvelteKit](https://kit.svelte.dev) is a framework for building Svelte applications with file-based routing, SSR, and static export. Use seoslug in your `load` functions to generate SEO metadata and render it via `<svelte:head>`.

## How it works

Two approaches are available. For SSG, a pre-build Python script generates a JSON manifest that your `+layout.js` load function reads and exposes as page data. For SSR, call seoslug directly in `+page.js` or `+page.server.js` and return the payload alongside your content data. Both use `<svelte:head>` in the page or layout component to render the tags.

## Setup

### 1. Write the SEO generation script (static export)

Create `scripts/generate_seo.py`. This script walks your `src/content/` or `src/routes/` directory, builds an SEO payload per route, and writes a JSON manifest:

```python
"""Pre-build: generates SEO JSON manifest for SvelteKit."""
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

    output = PROJECT_ROOT / "static" / "seo-manifest.json"
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Written {output} ({len(manifest)} routes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

### 2. Load the manifest in a layout

Create `src/routes/+layout.js` (or `+layout.server.js`) that imports the manifest and makes it available:

```javascript
import seoManifest from "$static/seo-manifest.json";

export function load({ url }) {
  const seo = seoManifest[url.pathname] || null;
  return { seo };
}
```

### 3. Render tags with `<svelte:head>`

In your layout component (`src/routes/+layout.svelte`), use `<svelte:head>` to inject the SEO tags:

```svelte
<script>
  export let data;
  $: seo = data.seo;
</script>

<svelte:head>
  {#if seo}
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
    {#if seo.schema_jsonld}
      <script type="application/ld+json">
        {JSON.stringify(seo.schema_jsonld)}
      </script>
    {/if}
  {:else}
    <title>Default Title</title>
    <meta name="robots" content="index,follow" />
  {/if}
</svelte:head>

<slot />
```

## Runtime approach (SSR)

For dynamic content, call seoslug directly inside a `+page.js` load function:

```python
# api/seo_builder.py
from seoslug import SEOConfig, SEOEntity, build_seo_payload

config = SEOConfig(
    canonical_host="yoursite.com",
    public_base_url="https://yoursite.com/",
    site_name="Your Site",
    title_template="{title} | Your Site",
)

def page_seo(title: str, description: str, route: str) -> dict:
    entity = SEOEntity(entity_type="page", title=title, excerpt=description)
    payload = build_seo_payload(entity, route, config)
    return payload.to_dict() if payload else {}
```

Then import it in `+page.server.js`:

```javascript
import { page_seo } from "$lib/seo_builder";

export async function load({ params, fetch }) {
  const post = await fetch(`/api/posts/${params.slug}`).then(r => r.json());
  const seo = page_seo(post.title, post.excerpt, `/blog/${params.slug}/`);
  return { post, seo };
}
```

The same `<svelte:head>` snippet renders the result in the page component.

## CI/CD

For the static manifest approach:

```yaml
- uses: actions/setup-python@v5
  with:
    python-version: "3.x"
- run: pip install "seoslug>=2.0.1" pyyaml
- run: python scripts/generate_seo.py
- run: npm ci
- run: npm run build
```

For SSR, install seoslug in your deployment image and import directly in `+page.server.js`.
