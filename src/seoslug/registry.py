"""Schema registry for custom JSON-LD generators."""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Protocol

if TYPE_CHECKING:
    from .config import SEOConfig
    from .schemas import SEOEntity


class SchemaGenerator(Protocol):
    """Protocol for custom schema generator callables."""
    def __call__(
        self,
        entity: SEOEntity,
        config: SEOConfig,
        canonical: str,
        title: str,
        description: str | None,
        og_image: str | None,
    ) -> dict | None: ...


class SchemaRegistry:
    """Registry for user-registered schema generators.

    Register a generator for any schema type name.
    When build_schema encounters a type registered here, it calls
    the generator instead of the built-in builder.
    """

    def __init__(self) -> None:
        self._generators: dict[str, SchemaGenerator] = {}

    def register(
        self,
        schema_type: str,
        generator: SchemaGenerator,
    ) -> None:
        """Register a generator for *schema_type* (e.g. ``"Podcast"``)."""
        if not isinstance(schema_type, str) or not schema_type.strip():
            raise ValueError("schema_type must be a non-empty string")
        self._generators[schema_type.strip()] = generator

    def unregister(self, schema_type: str) -> None:
        """Remove a previously registered generator."""
        self._generators.pop(schema_type.strip(), None)

    def get(self, schema_type: str) -> SchemaGenerator | None:
        """Look up a generator by schema type name."""
        return self._generators.get(schema_type.strip())
