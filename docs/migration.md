# Migration guide

This guide covers breaking changes between seoslug versions.

## Upgrading from 0.1 to 0.2

Version 0.2 introduced auto generated JSON-LD by default.
Set `auto_generate_schema` to False to restore the old behavior.

```python
config = SEOConfig(
    canonical_host="blog.example.com",
    public_base_url="https://blog.example.com",
    url_policy=URLPolicy(),
    auto_generate_schema=False,
)
```

## Upgrading from 0.2 to 0.3

Version 0.3 replaced inline tracking logic with the detrack library.
The behavior is the same: tracking parameters are stripped by default.
No code changes are needed unless you relied on the specific set of stripped parameters.

The old implementation stripped utm_ prefixed parameters, gclid, and fbclid.
The new implementation uses detrack with 60+ patterns, including all previous ones.

## Upgrading from 0.3 to 1.0

Version 1.0 is the first stable release.
There are no breaking changes from 0.3.
All public APIs are stable and documented.

## Checking your version

```bash
pip show seoslug
```
