"""Plugin/hook system for seoslug.

Register callback functions that transform the SEO payload after it is built.
Hooks are identified by name and run in registration order.

Usage:

    from seoslug import hook, register_hook

    @hook("post_process")
    def add_breadcrumb(payload, entity, config):
        payload["breadcrumb"] = {...}
        return payload

    # Or programmatically:
    def my_hook(payload, entity, config):
        return payload

    register_hook("post_process", my_hook)

Built-in hook points:

    - ``post_process``: called at the end of ``build_seo_payload()``.
      Receives (payload: dict, entity: SEOEntity, config: SEOConfig).
      Must return the (possibly modified) payload dict.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import TYPE_CHECKING

from .exceptions import SEOPayloadError

if TYPE_CHECKING:
    from .config import SEOConfig
    from .schemas import SEOEntity

HookFunc = Callable[[dict, "SEOEntity", "SEOConfig"], dict]

_hooks: dict[str, list[HookFunc]] = {}


def register(name: str, fn: HookFunc) -> None:
    if not isinstance(name, str) or not name.strip():
        raise SEOPayloadError("hook name must be a non-empty string")
    if not callable(fn):
        raise SEOPayloadError("hook function must be callable")
    _hooks.setdefault(name, []).append(fn)


def hook(name: str) -> Callable[[HookFunc], HookFunc]:
    """Decorator that registers a function as a hook."""
    def decorator(fn: HookFunc) -> HookFunc:
        register(name, fn)

        @functools.wraps(fn)
        def wrapper(
            payload: dict, entity: SEOEntity, config: SEOConfig
        ) -> dict:
            return fn(payload, entity, config)

        return wrapper

    return decorator


def run(
    name: str,
    payload: dict,
    entity: "SEOEntity",
    config: "SEOConfig",
) -> dict:
    """Run all hooks registered under *name* in order."""
    for fn in _hooks.get(name, []):
        payload = fn(payload, entity, config)
    return payload


def clear(name: str | None = None) -> None:
    """Remove all hooks, or only those under *name*."""
    if name is not None:
        _hooks.pop(name, None)
    else:
        _hooks.clear()


def get_registered() -> dict[str, list[HookFunc]]:
    """Return a copy of all registered hooks (for inspection / testing)."""
    return {k: list(v) for k, v in _hooks.items()}
