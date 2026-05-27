"""JSON-LD helpers for seoslug."""

from copy import deepcopy


def normalize_schema_jsonld(value: dict | list[dict] | None) -> dict | list[dict] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return deepcopy(value)
    if isinstance(value, list) and all(isinstance(item, dict) for item in value):
        return deepcopy(value)
    raise ValueError("schema_jsonld must be dict, list[dict], or None")
