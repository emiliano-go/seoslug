# Async Builder

The async builder offloads payload generation to a thread pool.
Use it in async frameworks like FastAPI, Starlette, or Litestar.

```python
from seoslug.async_builder import build_seo_payload_async

payload = await build_seo_payload_async(
    entity=entity,
    route_path="/posts/my-post",
    config=config,
    overrides=overrides,  # optional
)
```

## Thread pool executor

By default, `build_seo_payload_async` uses a module-level `ThreadPoolExecutor` with 4 workers.

The executor is lazily created on the first call and reused for subsequent calls.

```python
from seoslug.async_builder import build_seo_payload_async

# Uses default executor (4 workers)
payload = await build_seo_payload_async(entity, "/about", config)
```

## Custom executor

Pass your own `ThreadPoolExecutor` for fine-grained control.

```python
from concurrent.futures import ThreadPoolExecutor
from seoslug.async_builder import build_seo_payload_async

executor = ThreadPoolExecutor(max_workers=8)

payload = await build_seo_payload_async(
    entity, "/about", config, executor=executor,
)

executor.shutdown()
```

## Setting a global executor

Override the module-level default executor with `set_executor()`.
Pass `None` to reset to the default (4 workers).

```python
from concurrent.futures import ThreadPoolExecutor
from seoslug.async_builder import set_executor

# Set a custom global executor
set_executor(ThreadPoolExecutor(max_workers=2))

# Reset to default
set_executor(None)
```

## Integration with async frameworks

### FastAPI

```python
from fastapi import FastAPI
from seoslug import SEOConfig, SEOEntity, URLPolicy
from seoslug.async_builder import build_seo_payload_async

app = FastAPI()
config = SEOConfig(
    canonical_host="example.com",
    public_base_url="https://example.com",
    url_policy=URLPolicy(),
)

@app.get("/posts/{slug}")
async def get_post(slug: str):
    entity = SEOEntity(
        entity_type="post",
        title=slug.replace("-", " ").title(),
        status="published",
    )
    payload = await build_seo_payload_async(entity, f"/posts/{slug}", config)
    return payload.to_dict()
```

### Starlette

```python
from starlette.applications import Starlette
from starlette.responses import JSONResponse
from seoslug.async_builder import build_seo_payload_async
```

Same pattern: `await build_seo_payload_async(...)`.

## Sync vs async parity

The async builder delegates to the same `build_seo_payload` function.
Output is identical for the same inputs.

```python
from seoslug import build_seo_payload
from seoslug.async_builder import build_seo_payload_async

entity = SEOEntity(entity_type="post", title="Post", excerpt="Desc")

async_payload = await build_seo_payload_async(entity, "/post", config)
sync_payload = build_seo_payload(entity, "/post", config)

assert async_payload.to_dict() == sync_payload.to_dict()  # True
```
