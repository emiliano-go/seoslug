"""Public API for seoslug."""

from .builder import build_seo_payload
from .config import SEOConfig, URLPolicy
from .exceptions import (
    SEOConfigError,
    SEOEntityError,
    SEOError,
    SEOPayloadError,
    URLPolicyError,
)
from .hooks import clear as clear_hooks, get_registered as get_registered_hooks, hook, register as register_hook, run as run_hooks
from .normalization import normalize_path, normalize_public_url
from .schemas import SEOEntity, SEOOverrides

__all__ = [
    "SEOConfig",
    "URLPolicy",
    "SEOEntity",
    "SEOOverrides",
    "normalize_public_url",
    "normalize_path",
    "build_seo_payload",
    "SEOError",
    "SEOConfigError",
    "SEOEntityError",
    "URLPolicyError",
    "SEOPayloadError",
    "hook",
    "register_hook",
    "clear_hooks",
    "get_registered_hooks",
    "run_hooks",
]
