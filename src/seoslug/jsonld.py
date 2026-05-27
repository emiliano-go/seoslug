"""JSON-LD helpers for seoslug."""


def normalize_schema_jsonld(value: dict | list[dict] | None) -> dict | list[dict]:
    if value is None:
        return {}
    return value
