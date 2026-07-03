"""Tests for the hook system: global registry, scoped HookRegistry, thread safety."""

import threading

import pytest

from seoslug import HookRegistry, SEOConfig, SEOEntity, URLPolicy, run_hooks
from seoslug.hooks import _GLOBAL_REGISTRY, clear, get_registered, register


# -- Helpers -- #

_EMPTY_CONFIG = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=URLPolicy(),
)


@pytest.fixture(autouse=True)
def _clear_global_hooks():
    clear()
    yield
    clear()


# -- Module-level (global) hooks -- #


def test_register_and_run():
    def add_tag(payload, entity, config):
        payload["custom"] = "yes"
        return payload

    register("post_process", add_tag)
    result = run_hooks("post_process", {}, None, _EMPTY_CONFIG)
    assert result["custom"] == "yes"


def test_decorator():
    from seoslug import hook

    @hook("post_process")
    def add_tag(payload, entity, config):
        payload["custom"] = "yes"
        return payload

    result = run_hooks("post_process", {}, None, _EMPTY_CONFIG)
    assert result["custom"] == "yes"


def test_multiple_hooks_run_in_order():
    results: list[int] = []

    def first(payload, entity, config):
        results.append(1)
        return payload

    def second(payload, entity, config):
        results.append(2)
        return payload

    register("post_process", first)
    register("post_process", second)
    run_hooks("post_process", {}, None, _EMPTY_CONFIG)
    assert results == [1, 2]


def test_clear_by_name():
    register("post_process", lambda p, e, c: p)
    register("other", lambda p, e, c: p)
    clear("post_process")
    registered = get_registered()
    assert "post_process" not in registered
    assert "other" in registered


def test_clear_all():
    register("post_process", lambda p, e, c: p)
    register("other", lambda p, e, c: p)
    clear()
    assert get_registered() == {}


def test_get_registered_returns_copy():
    register("post_process", lambda p, e, c: p)
    registered = get_registered()
    registered["other"] = []
    assert "other" not in get_registered()


def test_missing_hook_point_is_noop():
    result = run_hooks("nonexistent", {"a": 1}, None, _EMPTY_CONFIG)
    assert result == {"a": 1}


def test_invalid_name_raises():
    with pytest.raises((ValueError, Exception)):
        register("", lambda p, e, c: p)


def test_non_callable_raises():
    with pytest.raises((ValueError, Exception)):
        register("post_process", "not callable")  # type: ignore


# -- HookRegistry (scoped) -- #


def test_scoped_register_and_run():
    registry = HookRegistry()
    registry.register("post_process", lambda p, e, c: {**p, "scoped": "yes"})
    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
        hooks=registry,
    )
    result = run_hooks("post_process", {}, None, config)
    assert result["scoped"] == "yes"


def test_global_runs_before_scoped():
    order: list[str] = []

    register("post_process", lambda p, e, c: (order.append("global"), p)[1])

    scoped = HookRegistry()
    scoped.register("post_process", lambda p, e, c: (order.append("scoped"), p)[1])

    config = SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
        hooks=scoped,
    )
    run_hooks("post_process", {}, None, config)
    assert order == ["global", "scoped"]


def test_scoped_hooks_dont_leak():
    registry_a = HookRegistry()
    registry_a.register("post_process", lambda p, e, c: {**p, "from": "a"})

    registry_b = HookRegistry()
    registry_b.register("post_process", lambda p, e, c: {**p, "from": "b"})

    config_a = SEOConfig(
        canonical_host="a.com",
        public_base_url="https://a.com",
        url_policy=URLPolicy(),
        hooks=registry_a,
    )
    config_b = SEOConfig(
        canonical_host="b.com",
        public_base_url="https://b.com",
        url_policy=URLPolicy(),
        hooks=registry_b,
    )

    result_a = run_hooks("post_process", {}, None, config_a)
    result_b = run_hooks("post_process", {}, None, config_b)
    assert result_a["from"] == "a"
    assert result_b["from"] == "b"


def test_scoped_clear():
    registry = HookRegistry()
    registry.register("post_process", lambda p, e, c: p)
    registry.clear("post_process")
    assert registry.get_registered() == {}


def test_scoped_get_registered_copy():
    registry = HookRegistry()
    registry.register("post_process", lambda p, e, c: p)
    r = registry.get_registered()
    r["other"] = []
    assert "other" not in registry.get_registered()


def test_scoped_invalid_name_raises():
    registry = HookRegistry()
    with pytest.raises((ValueError, Exception)):
        registry.register("", lambda p, e, c: p)


def test_scoped_non_callable_raises():
    registry = HookRegistry()
    with pytest.raises((ValueError, Exception)):
        registry.register("post_process", "not callable")  # type: ignore


# -- Thread safety -- #


def test_concurrent_register():
    registry = HookRegistry()
    n = 100
    barrier = threading.Barrier(n)

    def register_fn(i):
        barrier.wait()
        registry.register("post_process", lambda p, e, c, i=i: {**p, str(i): i})

    threads = [threading.Thread(target=register_fn, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=5)

    registered = registry.get_registered()
    assert len(registered["post_process"]) == n


# -- Exception behavior -- #


def test_hook_exception_skips_remaining():
    results: list[int] = []

    def ok(payload, entity, config):
        results.append(1)
        return payload

    def broken(payload, entity, config):
        raise ValueError("boom")

    def never_called(payload, entity, config):
        results.append(3)
        return payload

    register("post_process", ok)
    register("post_process", broken)
    register("post_process", never_called)

    with pytest.raises(ValueError, match="boom"):
        run_hooks("post_process", {}, None, _EMPTY_CONFIG)

    assert results == [1]
