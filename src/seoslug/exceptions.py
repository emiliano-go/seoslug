"""Custom exceptions for seoslug."""


class SEOError(Exception):
    """Base exception for all seoslug errors."""


class SEOConfigError(SEOError, ValueError):
    """Invalid SEO configuration — raised during SEOConfig or URLPolicy construction."""


class SEOEntityError(SEOError, ValueError):
    """Invalid SEO entity data — raised during SEOEntity or SEOOverrides construction."""


class URLPolicyError(SEOConfigError):
    """Invalid URL policy configuration — raised during URLPolicy construction."""


class SEOPayloadError(SEOError, ValueError):
    """Error during payload generation or text processing."""
