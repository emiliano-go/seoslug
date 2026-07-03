---
seo:
  title: Contributing - seoslug
  canonical: https://seoslug.emiliano-go.com/contributing/
  robots: index,follow
  og:
    type: website
    title: Contributing - seoslug
    description: Contributions are welcome. seoslug is pure Python with minimal core
      dependencies.
    url: https://seoslug.emiliano-go.com/contributing/
    image: https://seoslug.emiliano-go.com/assets/icon.png
    image:width: 225
    image:height: 225
    site_name: seoslug
    locale: en_US
  twitter:
    card: summary_large_image
    title: Contributing - seoslug
    description: Contributions are welcome. seoslug is pure Python with minimal core
      dependencies.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    site: '@emiliano_gando'
  description: Contributions are welcome. seoslug is pure Python with minimal core
    dependencies.
  schema_jsonld:
    '@context': https://schema.org
    '@type': WebPage
    name: Contributing - seoslug
    url: https://seoslug.emiliano-go.com/contributing/
    description: Contributions are welcome. seoslug is pure Python with minimal core
      dependencies.
    image: https://seoslug.emiliano-go.com/assets/icon.png
    publisher:
      '@type': Organization
      name: Emiliano Gandini Outeda
seo_html: "<title>Contributing - seoslug</title>\n<meta name=\"description\" content=\"\
  Contributions are welcome. seoslug is pure Python with minimal core dependencies.\"\
  >\n<link rel=\"canonical\" href=\"https://seoslug.emiliano-go.com/contributing/\"\
  >\n<meta name=\"robots\" content=\"index,follow\">\n<meta property=\"og:type\" content=\"\
  website\">\n<meta property=\"og:title\" content=\"Contributing - seoslug\">\n<meta\
  \ property=\"og:description\" content=\"Contributions are welcome. seoslug is pure\
  \ Python with minimal core dependencies.\">\n<meta property=\"og:url\" content=\"\
  https://seoslug.emiliano-go.com/contributing/\">\n<meta property=\"og:image\" content=\"\
  https://seoslug.emiliano-go.com/assets/icon.png\">\n<meta property=\"og:image:width\"\
  \ content=\"225\">\n<meta property=\"og:image:height\" content=\"225\">\n<meta property=\"\
  og:site_name\" content=\"seoslug\">\n<meta property=\"og:locale\" content=\"en_US\"\
  >\n<meta name=\"twitter:card\" content=\"summary_large_image\">\n<meta name=\"twitter:title\"\
  \ content=\"Contributing - seoslug\">\n<meta name=\"twitter:description\" content=\"\
  Contributions are welcome. seoslug is pure Python with minimal core dependencies.\"\
  >\n<meta name=\"twitter:image\" content=\"https://seoslug.emiliano-go.com/assets/icon.png\"\
  >\n<meta name=\"twitter:site\" content=\"@emiliano_gando\">\n<script type=\"application/ld+json\"\
  >\n{\n  \"@context\": \"https://schema.org\",\n  \"@type\": \"WebPage\",\n  \"name\"\
  : \"Contributing - seoslug\",\n  \"url\": \"https://seoslug.emiliano-go.com/contributing/\"\
  ,\n  \"description\": \"Contributions are welcome. seoslug is pure Python with minimal\
  \ core dependencies.\",\n  \"image\": \"https://seoslug.emiliano-go.com/assets/icon.png\"\
  ,\n  \"publisher\": {\n    \"@type\": \"Organization\",\n    \"name\": \"Emiliano\
  \ Gandini Outeda\"\n  }\n}\n</script>\n"
---

# Contributing

Contributions are welcome. seoslug is pure Python with minimal core dependencies.

## Setup

```bash
git clone https://github.com/emiliano-go/seoslug.git
cd seoslug
pip install -e ".[test,fast]"  # or ".[test,light]" for minimal
```

The `[fast]` extras install lxml and detrack (recommended for development).
Use `pip install -e ".[test,light]"` for a minimal dev environment. All tests
pass with either extra.

## Running tests

```bash
python -m pytest -q
```

Run tests with coverage:

```bash
python -m pytest --cov=seoslug
```

All tests must pass before you submit changes.

## Code style

Follow PEP 8. Keep functions small and focused. Use descriptive names.

The project uses type hints throughout. Run `mypy` on the source if you make type changes.

```bash
pip install mypy
mypy src/seoslug/
```

## Adding features

- Add tests for new features alongside the implementation.
- Update documentation for any user-facing changes.
- Keep the public API minimal. Export only what users need from `__init__.py`.
- New entity types need entries in `_ENTITY_TYPES`, `schema_type_map`, and a JSON-LD builder in `jsonld.py`.
- New dataclasses should follow the `_DictCompatMixin` pattern for dict compatibility.

## Submitting changes

Open a pull request on GitHub. Use a short description of what changed and why.

Maintainers will review within one week.

## Documentation

Documentation uses Markdown. Follow the writing guide for tone and style. Update or add pages in the `docs/` directory.

Pages are written in the dbwarden style:
- Professional, developer-empowering tone
- Short paragraphs (2-3 sentences max)
- Bullet lists over prose blocks
- Code blocks for almost every section
- Tables for parameter/field references
- Short punchlines
- No em dashes
