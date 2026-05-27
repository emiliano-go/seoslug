# Development

## Tests

Run the full test suite:

```bash
python -m pytest -q
```

What tests cover:

- URL normalization rules, host/scheme enforcement, trailing slash modes, query filtering, idempotency.
- Payload fallback precedence, robots logic, OG/Twitter behavior, schema passthrough.
- Regression fixtures for representative entity types.

If you change core logic, add or update tests in `tests/` before opening a PR.

## Contributing

Small and focused contributions are preferred.

1. Fork and create a feature branch.
2. Make changes with tests.
3. Run `python -m pytest -q`.
4. Open a PR with a short description of what changed and why.

Please keep public API changes explicit, and document behavior changes in docs.
