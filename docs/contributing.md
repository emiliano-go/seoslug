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
