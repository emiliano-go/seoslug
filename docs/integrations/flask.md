---
seo:
  title: Flask integration - seoslug
  canonical: https://seoslug.emiliano-go.com/integrations/flask/
  robots: index,follow
  og:
    type: website
    title: Flask integration - seoslug
    description: Call buildseopayload in your route and pass the result as template
      context. Flask's synchronous request handling maps directly to seoslug's synchronous
      builder.
    url: https://seoslug.emiliano-go.com/integrations/flask/
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:width: 1408
    image:height: 768
    image:alt: seoslug documentation
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Flask integration - seoslug
    description: Call buildseopayload in your route and pass the result as template
      context. Flask's synchronous request handling maps directly to seoslug's synchronous
      builder.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    image:alt: seoslug documentation
    site: '@emiliano_gando'
  description: Call buildseopayload in your route and pass the result as template
    context. Flask's synchronous request handling maps directly to seoslug's synchronous
    builder.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Flask integration - seoslug
    url: https://seoslug.emiliano-go.com/integrations/flask/
    description: Call buildseopayload in your route and pass the result as template
      context. Flask's synchronous request handling maps directly to seoslug's synchronous
      builder.
    image: https://seoslug.emiliano-go.com/assets/images/og-image.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
      logo: https://seoslug.emiliano-go.com/assets/images/og-image.png
seo_html: "<title>Flask integration - seoslug</title>\n<meta name=\"description\"\
  \ content=\"Call buildseopayload in your route and pass the result as template context.\
  \ Flask&#x27;s synchronous request handling maps directly to seoslug&#x27;s synchronous\
  \ builder.\">\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/integrations/flask/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Flask integration - seoslug\"\
  >\n<meta property=\"og:description\" content=\"Call buildseopayload in your route\
  \ and pass the result as template context. Flask&#x27;s synchronous request handling\
  \ maps directly to seoslug&#x27;s synchronous builder.\">\n<meta property=\"og:url\"\
  \ content=\"https://seoslug.emiliano-go.com/integrations/flask/\">\n<meta property=\"\
  og:image\" content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  >\n<meta property=\"og:image:width\" content=\"1408\">\n<meta property=\"og:image:height\"\
  \ content=\"768\">\n<meta property=\"og:image:alt\" content=\"seoslug documentation\"\
  >\n<meta property=\"og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\"\
  \ content=\"en_US\">\n<meta name=\"twitter:card\" content=\"summary_large_image\"\
  >\n<meta name=\"twitter:title\" content=\"Flask integration - seoslug\">\n<meta\
  \ name=\"twitter:description\" content=\"Call buildseopayload in your route and\
  \ pass the result as template context. Flask&#x27;s synchronous request handling\
  \ maps directly to seoslug&#x27;s synchronous builder.\">\n<meta name=\"twitter:image\"\
  \ content=\"https://seoslug.emiliano-go.com/assets/images/og-image.png\">\n<meta\
  \ name=\"twitter:image:alt\" content=\"seoslug documentation\">\n<meta name=\"twitter:site\"\
  \ content=\"@emiliano_gando\">\n<script type=\"application/ld+json\">\n{\n  \"@context\"\
  : \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\": \"Flask integration\
  \ - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/integrations/flask/\"\
  ,\n  \"description\": \"Call buildseopayload in your route and pass the result as\
  \ template context. Flask's synchronous request handling maps directly to seoslug's\
  \ synchronous builder.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\",\n    \"logo\": \"https://seoslug.emiliano-go.com/assets/images/og-image.png\"\
  \n  }\n}\n</script>\n"
---

# Flask integration

Call `build_seo_payload` in your route and pass the result as template context. Flask's synchronous request handling maps directly to seoslug's synchronous builder.

## Basic route

```python
from flask import Flask, render_template, request
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

app = Flask(__name__)

SEO_CONFIG = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)


@app.route("/")
def home():
    entity = SEOEntity(
        entity_type="home",
        title="My Blog",
        excerpt="A blog about things.",
        status="published",
    )
    payload = build_seo_payload(entity, "/", SEO_CONFIG)

    return render_template("home.html", seo=payload)
```

## Post detail route

```python
from flask import Flask, render_template, abort
from seoslug import SEOConfig, URLPolicy, SEOEntity, Breadcrumb, build_seo_payload

app = Flask(__name__)

SEO_CONFIG = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)


@app.route("/<slug>/")
def post_detail(slug):
    post = get_post_by_slug(slug)
    if post is None:
        abort(404)

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
        published_at=post.published_at.isoformat(),
        updated_at=post.updated_at.isoformat() if post.updated_at else None,
        author_name=post.author,
        featured_image=post.cover_url,
        breadcrumbs=[
            Breadcrumb(name="Blog", url="/"),
            Breadcrumb(name=post.title, url=f"/{slug}/"),
        ],
    )
    payload = build_seo_payload(entity, f"/{slug}/", SEO_CONFIG)

    return render_template("post.html", post=post, seo=payload)
```

## Template usage

Pass the payload to your Jinja2 template. Use `render_html()` for the complete `<head>` block, or granular render methods for partial injection:

```jinja
<!doctype html>
<html>
  <head>
    {{ seo.render_html()|safe }}
  </head>
  <body>
    <h1>{{ post.title }}</h1>
    {{ post.content|safe }}
  </body>
</html>
```

For custom template composition:

```jinja
<head>
  <title>{{ seo.title }}</title>
  <meta name="description" content="{{ seo.description }}">
  <link rel="canonical" href="{{ seo.canonical }}">
  <meta name="robots" content="{{ seo.robots }}">
  {{ seo.render_opengraph()|safe }}
  {{ seo.render_twitter()|safe }}
  {{ seo.render_jsonld()|safe }}
</head>
```

## JSON API

Use `build_seo_payload_dict` or `payload.to_dict()` when returning JSON:

```python
from flask import Flask, jsonify
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload_dict

app = Flask(__name__)

SEO_CONFIG = SEOConfig(
    canonical_host="api.example.com",
    public_base_url="https://api.example.com",
    url_policy=URLPolicy(),
)


@app.route("/api/seo/<slug>")
def seo_json(slug):
    post = get_post_by_slug(slug)
    if post is None:
        return {"error": "not found"}, 404

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
    )
    payload = build_seo_payload_dict(entity, f"/{slug}/", SEO_CONFIG)

    return jsonify(payload)
```

## Blueprint pattern

For larger apps, create the config once and share it via `current_app` or a factory:

```python
# seo.py
from seoslug import SEOConfig, URLPolicy

def create_seo_config():
    return SEOConfig(
        canonical_host="blog.example.com",
        public_base_url="https://blog.example.com",
        url_policy=URLPolicy(),
    )


# views.py
from flask import Blueprint, render_template, current_app
from seoslug import SEOEntity, build_seo_payload

blog = Blueprint("blog", __name__)


@blog.route("/")
def home():
    entity = SEOEntity(
        entity_type="home",
        title="My Blog",
        excerpt="A blog about things.",
        status="published",
    )
    config = current_app.config["SEO_CONFIG"]
    payload = build_seo_payload(entity, "/", config)

    return render_template("home.html", seo=payload)


# app.py
from flask import Flask
from seo import create_seo_config

app = Flask(__name__)
app.config["SEO_CONFIG"] = create_seo_config()
app.register_blueprint(blog)
```

## Extension pattern

Wrap config creation and payload building into a Flask extension:

```python
# ext/seoslug.py
from flask import current_app
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

class Seoslug:
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault("SEO_CANONICAL_HOST", "blog.example.com")
        app.config.setdefault("SEO_PUBLIC_URL", "https://blog.example.com")
        app.extensions["seoslug"] = self

    @property
    def config(self):
        return SEOConfig(
            canonical_host=current_app.config["SEO_CANONICAL_HOST"],
            public_base_url=current_app.config["SEO_PUBLIC_URL"],
            url_policy=URLPolicy(),
        )

    def build(self, entity, route):
        return build_seo_payload(entity, route, self.config)


# app.py
from flask import Flask
from ext.seoslug import Seoslug

app = Flask(__name__)
seoslug = Seoslug(app)


# views.py
from flask import Blueprint, render_template, current_app
from seoslug import SEOEntity

blog = Blueprint("blog", __name__)


@blog.route("/")
def home():
    entity = SEOEntity(
        entity_type="home",
        title="My Blog",
        excerpt="A blog about things.",
        status="published",
    )
    payload = current_app.extensions["seoslug"].build(entity, "/")
    return render_template("home.html", seo=payload)
```

## ETag caching

Flask can combine seoslug's ETag with conditional response handling:

```python
from flask import Flask, render_template, request
from seoslug import SEOConfig, URLPolicy, SEOEntity, build_seo_payload

app = Flask(__name__)

SEO_CONFIG = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
)


@app.route("/<slug>/")
def post_detail(slug):
    post = get_post_by_slug(slug)
    if post is None:
        abort(404)

    entity = SEOEntity(
        entity_type="post",
        title=post.title,
        excerpt=post.excerpt,
        status="published",
    )
    payload = build_seo_payload(entity, f"/{slug}/", SEO_CONFIG)
    etag = payload.etag()

    if request.if_none_match and etag in request.if_none_match:
        return "", 304

    html = render_template("post.html", post=post, seo=payload)
    response = app.make_response(html)
    response.set_etag(etag)
    return response
```
