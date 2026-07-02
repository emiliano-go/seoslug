"""Domain-specific factory functions for SEOEntity creation."""

from .schemas import Breadcrumb, FAQItem, SEOEntity


def from_blog_post(
    title: str,
    body_html: str,
    slug: str | None = None,
    author: str = "",
    excerpt: str | None = None,
    breadcrumbs: list[dict] | None = None,
) -> SEOEntity:
    """Create an SEOEntity for a blog post.

    Parameters
    ----------
    title:
        Post title.
    body_html:
        Full HTML body (used for auto-generated description).
    slug:
        URL slug (optional).
    author:
        Author name (optional).
    excerpt:
        Optional explicit excerpt. Falls back to body snippet when ``None``.
    breadcrumbs:
        Optional list of ``{"name": ..., "url": ...}`` dicts.
    """
    _breadcrumbs: list[Breadcrumb] | None = None
    if breadcrumbs:
        _breadcrumbs = [Breadcrumb(name=b["name"], url=b["url"]) for b in breadcrumbs]
    return SEOEntity(
        entity_type="post",
        title=title,
        body_html=body_html,
        slug=slug,
        author_name=author or None,
        excerpt=excerpt,
        status="published",
        breadcrumbs=_breadcrumbs,
    )


def from_product(
    name: str,
    sku: str,
    price: str | float,
    currency: str = "USD",
    availability: str = "InStock",
    description: str | None = None,
    breadcrumbs: list[dict] | None = None,
) -> SEOEntity:
    """Create an SEOEntity for a product page.

    Parameters
    ----------
    name:
        Product name.
    sku:
        Stock-keeping unit.
    price:
        Price as a string (e.g. ``"29.99"``) or numeric.
    currency:
        ISO 4217 currency code (default ``"USD"``).
    availability:
        Schema.org availability value (default ``"InStock"``).
    description:
        Optional product description (excerpt).
    breadcrumbs:
        Optional list of ``{"name": ..., "url": ...}`` dicts.
    """
    _breadcrumbs: list[Breadcrumb] | None = None
    if breadcrumbs:
        _breadcrumbs = [Breadcrumb(name=b["name"], url=b["url"]) for b in breadcrumbs]
    return SEOEntity(
        entity_type="product",
        title=name,
        sku=sku,
        price=str(price),
        price_currency=currency,
        availability=availability,
        excerpt=description,
        status="published",
        breadcrumbs=_breadcrumbs,
    )


def from_faq(
    questions: list[dict[str, str]],
    title: str = "FAQ",
    description: str | None = None,
    breadcrumbs: list[dict] | None = None,
) -> SEOEntity:
    """Create an SEOEntity for an FAQ page.

    Parameters
    ----------
    questions:
        List of ``{"question": "...", "answer": "..."}`` dicts.
    title:
        Page title (default ``"FAQ"``).
    description:
        Optional meta description.
    breadcrumbs:
        Optional list of ``{"name": ..., "url": ...}`` dicts.
    """
    _breadcrumbs: list[Breadcrumb] | None = None
    if breadcrumbs:
        _breadcrumbs = [Breadcrumb(name=b["name"], url=b["url"]) for b in breadcrumbs]
    return SEOEntity(
        entity_type="faq",
        title=title,
        excerpt=description,
        faq_items=[FAQItem(**q) for q in questions],
        status="published",
        breadcrumbs=_breadcrumbs,
    )
