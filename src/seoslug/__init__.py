"""Public API for seoslug."""

from .async_builder import build_seo_payload_async
from .builder import build_seo_payload, build_seo_payload_dict
from .config import SEOConfig, URLPolicy
from .exceptions import (
    SEOConfigError,
    SEOEntityError,
    SEOError,
    SEOPayloadError,
    URLPolicyError,
)
from .factories import from_blog_post, from_faq, from_product
from .hooks import HookRegistry, clear as clear_hooks, get_registered as get_registered_hooks, hook, register as register_hook, run as run_hooks
from .normalization import normalize_path, normalize_public_url
from .registry import SchemaRegistry
from .schemas import (
    Breadcrumb,
    FAQItem,
    OGImage,
    Robots,
    SEOEntity,
    SEOEntityBuilder,
    SEOOverrides,
)

__all__ = [
    "HookRegistry",
    "SEOConfig",
    "URLPolicy",
    "SEOEntity",
    "SEOOverrides",
    "SEOEntityBuilder",
    "OGImage",
    "Breadcrumb",
    "FAQItem",
    "Robots",
    "SchemaRegistry",
    "normalize_public_url",
    "normalize_path",
    "build_seo_payload",
    "build_seo_payload_dict",
    "build_seo_payload_async",
    "from_blog_post",
    "from_product",
    "from_faq",
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
