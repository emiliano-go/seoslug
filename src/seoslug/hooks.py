"""Plugin/hook system for seoslug.

Register callback functions that transform the SEO payload after it is built.
Hooks are identified by name and run in registration order.

Usage (global hooks -- recommended for single-config apps):

    from seoslug import hook, register_hook

    @hook("post_process")
    def add_breadcrumb(payload, entity, config):
        payload["breadcrumb"] = {...}
        return payload

    # Or programmatically:
    def my_hook(payload, entity, config):
        return payload

    register_hook("post_process", my_hook)

Usage (scoped hooks -- multi-config / multi-tenant apps):

    from seoslug import HookRegistry, SEOConfig

    registry = HookRegistry()
    registry.register("post_process", my_hook)
    config = SEOConfig(..., hooks=registry)

Global hooks run first, then scoped hooks.  Both must return the payload dict.

Built-in hook points:

    - ``post_process``: called at the end of ``build_seo_payload()``.
      Receives (payload: dict, entity: SEOEntity, config: SEOConfig).
      Must return the (possibly modified) payload dict.
"""

from __future__ import annotations

import functools
import threading
from collections.abc import Callable
from typing import TYPE_CHECKING

from .exceptions import SEOPayloadError

if TYPE_CHECKING:
    from .config import SEOConfig
    from .schemas import SEOEntity

HookFunc = Callable[[dict, "SEOEntity", "SEOConfig"], dict]


class HookRegistry:
    """Instance-scoped hook registry.

    Thread-safe for both reads and writes.  Useful in multi-config or
    multi-tenant applications where separate ``SEOConfig`` instances need
    independent hook chains.

    Global hooks (``register`` / ``hook``) run **before** scoped hooks.
    """

    def __init__(self) -> None:
        self._hooks: dict[str, list[HookFunc]] = {}
        self._lock = threading.Lock()

    def register(self, name: str, fn: HookFunc) -> None:
        """Register *fn* to run when hook *name* is triggered."""
        if not isinstance(name, str) or not name.strip():
            raise SEOPayloadError("hook name must be a non-empty string")
        if not callable(fn):
            raise SEOPayloadError("hook function must be callable")
        with self._lock:
            self._hooks.setdefault(name, []).append(fn)

    def hook(self, name: str) -> Callable[[HookFunc], HookFunc]:
        """Decorator that registers a function as a hook."""
        def decorator(fn: HookFunc) -> HookFunc:
            self.register(name, fn)

            @functools.wraps(fn)
            def wrapper(
                payload: dict, entity: SEOEntity, config: SEOConfig
            ) -> dict:
                return fn(payload, entity, config)

            return wrapper

        return decorator

    def run(
        self,
        name: str,
        payload: dict,
        entity: "SEOEntity",
        config: "SEOConfig",
    ) -> dict:
        """Run all hooks registered under *name* in registration order."""
        hooks = list(self._hooks.get(name, []))
        for fn in hooks:
            payload = fn(payload, entity, config)
        return payload

    def clear(self, name: str | None = None) -> None:
        """Remove all hooks, or only those under *name*."""
        with self._lock:
            if name is not None:
                self._hooks.pop(name, None)
            else:
                self._hooks.clear()

    def get_registered(self) -> dict[str, list[HookFunc]]:
        """Return a copy of all registered hooks (for inspection / testing)."""
        with self._lock:
            return {k: list(v) for k, v in self._hooks.items()}


# -- Module-level (global) registry -- #

_GLOBAL_REGISTRY: HookRegistry = HookRegistry()


def register(name: str, fn: HookFunc) -> None:
    """Register a global hook.  See ``HookRegistry.register``."""
    _GLOBAL_REGISTRY.register(name, fn)


def hook(name: str) -> Callable[[HookFunc], HookFunc]:
    """Decorator that registers a global hook.  See ``HookRegistry.hook``."""
    return _GLOBAL_REGISTRY.hook(name)


def run(
    name: str,
    payload: dict,
    entity: "SEOEntity",
    config: "SEOConfig",
) -> dict:
    """Run all hooks (global first, then scoped) under *name*.

    1. Global hooks registered via ``register`` / ``hook``.
    2. Scoped hooks on ``config.hooks`` (if set).

    Each hook receives ``(payload, entity, config)`` and **must** return the
    (possibly modified) payload dict.
    """
    payload = _GLOBAL_REGISTRY.run(name, payload, entity, config)
    scoped: HookRegistry | None = getattr(config, "hooks", None)
    if scoped is not None:
        payload = scoped.run(name, payload, entity, config)
    return payload


def clear(name: str | None = None) -> None:
    """Remove all global hooks, or only those under *name*."""
    _GLOBAL_REGISTRY.clear(name)


def get_registered() -> dict[str, list[HookFunc]]:
    """Return a copy of all global registered hooks."""
    return _GLOBAL_REGISTRY.get_registered()
