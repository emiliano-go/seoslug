"""Tests for async SEO payload builder."""

import pytest

from seoslug import SEOConfig, SEOEntity, URLPolicy, build_seo_payload


def _config() -> SEOConfig:
    return SEOConfig(
        canonical_host="example.com",
        public_base_url="https://example.com",
        url_policy=URLPolicy(),
    )


@pytest.mark.asyncio
async def test_build_seo_payload_async_basic() -> None:
    from seoslug.async_builder import build_seo_payload_async

    entity = SEOEntity(entity_type="page", title="About")
    payload = await build_seo_payload_async(entity, "/about", _config())
    assert payload.title == "About"
    assert payload.canonical == "https://example.com/about"


@pytest.mark.asyncio
async def test_async_matches_sync() -> None:
    from seoslug.async_builder import build_seo_payload_async

    entity = SEOEntity(entity_type="post", title="Post", excerpt="Desc")
    async_payload = await build_seo_payload_async(entity, "/post", _config())
    sync_payload = build_seo_payload(entity, "/post", _config())
    assert async_payload.to_dict() == sync_payload.to_dict()


@pytest.mark.asyncio
async def test_async_custom_executor() -> None:
    from concurrent.futures import ThreadPoolExecutor
    from seoslug.async_builder import build_seo_payload_async

    executor = ThreadPoolExecutor(max_workers=2)
    entity = SEOEntity(entity_type="page", title="Test")
    payload = await build_seo_payload_async(entity, "/test", _config(), executor=executor)
    assert payload.title == "Test"
    executor.shutdown()
