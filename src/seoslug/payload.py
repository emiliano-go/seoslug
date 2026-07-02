"""SEO payload return types — dataclass + dict-compatible."""

from __future__ import annotations

import hashlib
import html as _html
import json
from dataclasses import dataclass, fields
from typing import TypedDict


# -- Key mappings (attribute name → colon-separated dict key) --

_OG_KEY_MAP: dict[str, str] = {
    "image_width": "image:width",
    "image_height": "image:height",
    "image_alt": "image:alt",
    "locale_alternate": "locale:alternate",
}

_TW_KEY_MAP: dict[str, str] = {
    "image_alt": "image:alt",
}

_REV_OG_KEY_MAP: dict[str, str] = {v: k for k, v in _OG_KEY_MAP.items()}
_REV_TW_KEY_MAP: dict[str, str] = {v: k for k, v in _TW_KEY_MAP.items()}


# -- Mixin for dict-compatible dataclass access --

class _DictCompatMixin:
    _KEY_MAP: dict[str, str] = {}

    def __getitem__(self, key: str):
        if hasattr(self, key):
            return getattr(self, key)
        rev = {v: k for k, v in self._KEY_MAP.items()}
        if key in rev:
            return getattr(self, rev[key])
        raise KeyError(key)

    def __setitem__(self, key: str, value):
        if hasattr(self, key):
            setattr(self, key, value)
            return
        rev = {v: k for k, v in self._KEY_MAP.items()}
        if key in rev:
            setattr(self, rev[key], value)
            return
        raise KeyError(key)

    def __contains__(self, key: str) -> bool:
        try:
            val = self[key]
            return val is not None
        except KeyError:
            return False

    def get(self, key: str, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        seen: set[str] = set()
        for f in fields(self):
            val = getattr(self, f.name)
            mapped = self._KEY_MAP.get(f.name, f.name)
            if val is not None and mapped not in seen:
                seen.add(mapped)
                yield mapped

    def __eq__(self, other):
        if isinstance(other, dict):
            return self.to_dict() == other
        if isinstance(other, type(self)):
            return all(
                getattr(self, f.name) == getattr(other, f.name)
                for f in fields(self)
            )
        return NotImplemented


# -- Concrete dataclasses --

@dataclass(eq=False)
class OGPayload(_DictCompatMixin):
    _KEY_MAP = _OG_KEY_MAP
    type: str
    title: str | None
    description: str | None
    url: str | None
    image: str | None
    image_width: int | None = None
    image_height: int | None = None
    image_alt: str | None = None
    site_name: str | None = None
    locale: str | None = None
    locale_alternate: list[str] | None = None
    audio: str | None = None
    video: str | None = None

    def to_dict(self) -> dict:
        result: dict = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if val is not None:
                result[self._KEY_MAP.get(f.name, f.name)] = val
        return result


@dataclass(eq=False)
class TwitterPayload(_DictCompatMixin):
    _KEY_MAP = _TW_KEY_MAP
    card: str
    title: str | None
    description: str | None
    image: str | None
    image_alt: str | None = None
    site: str | None = None
    creator: str | None = None

    def to_dict(self) -> dict:
        result: dict = {}
        for f in fields(self):
            val = getattr(self, f.name)
            if val is not None:
                result[self._KEY_MAP.get(f.name, f.name)] = val
        return result


@dataclass(eq=False)
class SEOPayload(_DictCompatMixin):
    _KEY_MAP = {}
    title: str
    description: str
    canonical: str
    robots: str
    og: OGPayload
    twitter: TwitterPayload
    schema_jsonld: dict | list[dict] | None = None

    def to_dict(self) -> dict:
        result: dict = {
            "title": self.title,
            "canonical": self.canonical,
            "robots": self.robots,
            "og": self.og.to_dict(),
            "twitter": self.twitter.to_dict(),
        }
        if self.description is not None and self.description != "":
            result["description"] = self.description
        if self.schema_jsonld is not None:
            result["schema_jsonld"] = self.schema_jsonld
        return result

    def render_html(self) -> str:
        """Render the full SEO payload as an HTML snippet for ``<head>``.

        Returns a string of ``<title>``, ``<meta>``, ``<link>``, and
        ``<script>`` tags separated by newlines.  Ready to inject into
        your page template with ``{{ payload.render_html()|safe }}``.
        """
        lines: list[str] = []
        e = _html.escape

        lines.append(f"<title>{e(self.title)}</title>")

        if self.description:
            lines.append(f'<meta name="description" content="{e(self.description)}">')

        lines.append(f'<link rel="canonical" href="{e(self.canonical)}">')
        lines.append(f'<meta name="robots" content="{e(self.robots)}">')

        for key, val in self.og.to_dict().items():
            if isinstance(val, list):
                for v in val:
                    lines.append(f'<meta property="og:{e(key)}" content="{e(str(v))}">')
            else:
                lines.append(f'<meta property="og:{e(key)}" content="{e(str(val))}">')

        for key, val in self.twitter.to_dict().items():
            if isinstance(val, list):
                for v in val:
                    lines.append(f'<meta name="twitter:{e(key)}" content="{e(str(v))}">')
            else:
                lines.append(f'<meta name="twitter:{e(key)}" content="{e(str(val))}">')

        if self.schema_jsonld is not None:
            schema_str = json.dumps(self.schema_jsonld, indent=2, ensure_ascii=False)
            lines.append(f"<script type=\"application/ld+json\">\n{schema_str}\n</script>")

        return "\n".join(lines) + "\n"

    def hash(self) -> str:
        """Deterministic SHA-256 hex digest of the serialised payload.

        Two calls with identical input always return the same hash.
        Useful for caching keys, content-addressed storage, and
        CI comparison snapshots.
        """
        raw = json.dumps(self.to_dict(), sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    def etag(self) -> str:
        """HTTP ETag header value derived from the payload hash.

        Returns a quoted hex string suitable for an ``ETag`` header:
        ``'"abc123..."'``.
        """
        return f'"{self.hash()}"'


# -- TypedDict variants for type-checking (backward compat) --

class OGPayloadTypedDict(TypedDict, total=False):
    type: str
    title: str | None
    description: str | None
    url: str | None
    image: str | None
    image_width: int | None
    image_height: int | None
    image_alt: str | None
    site_name: str | None
    locale: str | None
    locale_alternate: list[str] | None
    audio: str | None
    video: str | None


class TwitterPayloadTypedDict(TypedDict, total=False):
    card: str
    title: str | None
    description: str | None
    image: str | None
    image_alt: str | None
    site: str | None
    creator: str | None


class SEOPayloadTypedDict(TypedDict, total=False):
    title: str
    description: str
    canonical: str
    robots: str
    og: OGPayloadTypedDict
    twitter: TwitterPayloadTypedDict
    schema_jsonld: dict | list[dict] | None
