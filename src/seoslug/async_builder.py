"""Async SEO payload builder for seoslug.

Offloads the synchronous *build_seo_payload* call to a thread pool
so it does not block the event loop in async frameworks (FastAPI,
Starlette, Litestar, Quart, etc.).
"""

from __future__ import annotations

import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import TYPE_CHECKING

from .builder import build_seo_payload

if TYPE_CHECKING:
    from .config import SEOConfig
    from .payload import SEOPayload
    from .schemas import SEOEntity, SEOOverrides


_default_executor: ThreadPoolExecutor | None = None


def _get_executor(max_workers: int = 4) -> ThreadPoolExecutor:
    global _default_executor
    if _default_executor is None:
        _default_executor = ThreadPoolExecutor(max_workers=max_workers)
    return _default_executor


def set_executor(executor: ThreadPoolExecutor | None) -> None:
    """Override the default thread pool executor.

    Pass ``None`` to reset to the default (4 workers).
    """
    global _default_executor
    _default_executor = executor


async def build_seo_payload_async(
    entity: SEOEntity,
    route_path: str,
    config: SEOConfig,
    overrides: SEOOverrides | None = None,
    executor: ThreadPoolExecutor | None = None,
) -> SEOPayload:
    """Async version of :func:`build_seo_payload <seoslug.builder.build_seo_payload>`.

    Runs the synchronous payload builder in a thread pool executor
    so it does not block the asyncio event loop.

    Parameters
    ----------
    entity:
        Content entity.
    route_path:
        URL path (e.g. ``"/posts/my-post"``).
    config:
        SEO configuration.
    overrides:
        Optional per-entity overrides.
    executor:
        Optional thread pool executor. Uses a module-level default
        (4 workers) when ``None``.
    """
    loop = asyncio.get_running_loop()
    ex = executor if executor is not None else _get_executor()
    return await loop.run_in_executor(
        ex,
        build_seo_payload,
        entity,
        route_path,
        config,
        overrides,
    )
