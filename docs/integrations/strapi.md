# Strapi integration

[Strapi](https://strapi.io) is an open-source headless CMS built with Node.js. Use seoslug in a custom plugin or middleware to enrich your API responses with Open Graph, Twitter Card, JSON-LD, canonical, and robots metadata.

## How it works

A custom Strapi middleware intercepts responses for content types that include seoslug fields. It reads the content title, excerpt, and metadata from the entity, builds an SEO payload with seoslug, and appends a `seo` key to the response body. The frontend receives structured SEO data alongside the content with zero extra requests.

## Setup

### 1. Create the seoslug middleware

Run `npm run strapi generate -- middleware seoslug` or create `src/middlewares/seoslug.js`:

```javascript
"use strict";

const { SEOConfig, SEOEntity, build_seo_payload_dict } = require("seoslug");

const CONFIG = new SEOConfig({
  canonical_host: "yoursite.com",
  public_base_url: "https://yoursite.com/",
  site_name: "Your Site",
  title_template: "{title} | Your Site",
  default_og_image: "https://yoursite.com/images/default-og.png",
  publisher_name: "Your Name",
  locale: "en_US",
  twitter_site: "@yourhandle",
});

module.exports = (config, { strapi }) => {
  return async (ctx, next) => {
    await next();

    const { response } = ctx;
    if (!response.body || typeof response.body !== "object") return;

    const data = response.body.data || response.body;
    const entities = Array.isArray(data) ? data : [data];

    for (const entity of entities) {
      const attrs = entity.attributes || entity;
      const title =
        attrs.seoTitle || attrs.title || attrs.name || ctx.request.path;
      const description =
        attrs.seoDescription || attrs.description || attrs.excerpt || "";

      const seoEntity = new SEOEntity({
        entity_type: "page",
        title,
        excerpt: description || undefined,
      });

      const seo = build_seo_payload_dict(
        seoEntity,
        ctx.request.path,
        CONFIG,
      );

      if (seo) {
        attrs.seo = seo;
      }
    }
  };
};
```

### 2. Enable the middleware

Register the middleware in `config/middlewares.js`:

```javascript
module.exports = [
  "strapi::logger",
  "strapi::errors",
  "strapi::security",
  "strapi::cors",
  "strapi::poweredBy",
  "strapi::query",
  "strapi::body",
  "strapi::session",
  "strapi::favicon",
  "strapi::public",
  {
    name: "global::seoslug",
    config: {},
  },
];
```

### 3. Custom plugin (alternative)

For more control, create a plugin instead. Run `npm run strapi generate -- plugin seoslug` and edit `src/plugins/seoslug/server/services/seoslug-service.js`:

```javascript
"use strict";

const { SEOConfig, SEOEntity, build_seo_payload_dict } = require("seoslug");

module.exports = ({ strapi }) => ({
  getConfig() {
    return new SEOConfig({
      canonical_host: strapi.config.get("server.host"),
      public_base_url: `${strapi.config.get("server.protocol")}://${strapi.config.get("server.host")}:${strapi.config.get("server.port")}/`,
      site_name: strapi.config.get("custom.seo.siteName", "Your Site"),
      title_template: "{title} | Your Site",
      publisher_name: strapi.config.get("custom.seo.publisherName", ""),
      locale: strapi.config.get("custom.seo.locale", "en_US"),
    });
  },

  buildSeo(entity, route) {
    const attrs = entity.attributes || entity;
    const title = attrs.seoTitle || attrs.title || attrs.name || "Page";
    const description = attrs.seoDescription || attrs.description || "";

    const seoEntity = new SEOEntity({
      entity_type: attrs.seoType || "page",
      title,
      excerpt: description || undefined,
      image: attrs.image?.url
        ? { url: attrs.image.url, width: 1200, height: 630 }
        : undefined,
      published_time: attrs.publishedAt || attrs.createdAt,
      modified_time: attrs.updatedAt,
    });

    return build_seo_payload_dict(seoEntity, route, this.getConfig());
  },
});
```

Then use the service in a controller or lifecycle hook:

```javascript
module.exports = ({ strapi }) => ({
  async find(ctx) {
    const entities = await strapi.entityService.findMany(ctx.query);
    const route = ctx.request.path;

    const enriched = entities.map((entity) => {
      const seo = strapi
        .plugin("seoslug")
        .service("seoslugService")
        .buildSeo(entity, route);
      return { ...entity, seo };
    });

    return enriched;
  },
});
```

### 4. Add SEO fields to content types

In the Strapi admin panel, add these fields to your content types:

| Field | Type | Description |
|-------|------|-------------|
| `seoTitle` | Text | Override for the page title (falls back to `title`) |
| `seoDescription` | Text | Override for the meta description (falls back to `description`) |
| `seoType` | Enumeration | Entity type for JSON-LD: `page`, `article`, `product` |

For per-content-type SEO, create a repeatable component called `seo` with these fields and reuse it across your collection types.

### 5. Frontend consumption

The enriched response includes a `seo` key on every entity:

```json
{
  "id": 1,
  "attributes": {
    "title": "Hello World",
    "seoTitle": "Hello World",
    "seoDescription": "A brief introduction",
    "seo": {
      "title": "Hello World | Your Site",
      "canonical": "https://yoursite.com/api/posts/1",
      "robots": "index,follow",
      "og": {
        "type": "website",
        "title": "Hello World | Your Site",
        "description": "A brief introduction",
        "url": "https://yoursite.com/api/posts/1",
        "image": "https://yoursite.com/images/default-og.png",
        "site_name": "Your Site",
        "locale": "en_US"
      },
      "twitter": {
        "card": "summary_large_image",
        "title": "Hello World | Your Site",
        "description": "A brief introduction",
        "image": "https://yoursite.com/images/default-og.png"
      },
      "schema_jsonld": {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "name": "Hello World | Your Site",
        "url": "https://yoursite.com/api/posts/1",
        "description": "A brief introduction",
        "publisher": { "@type": "Organization", "name": "Your Name" }
      }
    }
  }
}
```

Your frontend reads `entity.attributes.seo` and renders the tags using the framework's head API (Next.js Head, Gatsby Head API, SvelteKit `<svelte:head>`, etc.).

## Deploy

Install seoslug in your Strapi deployment:

```yaml
# Dockerfile or CI
RUN pip install "seoslug>=2.0.1"
```

Or if using npm:

```yaml
RUN npm install seoslug
```

Install seoslug as a runtime dependency in your deployment environment.
