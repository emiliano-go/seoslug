"""Tests for domain-specific factory functions."""

from seoslug import from_blog_post, from_faq, from_product
from seoslug.schemas import Breadcrumb, FAQItem


def test_from_blog_post_minimal() -> None:
    entity = from_blog_post(title="Hello", body_html="<p>World</p>")
    assert entity.entity_type == "post"
    assert entity.title == "Hello"
    assert entity.body_html == "<p>World</p>"
    assert entity.status == "published"


def test_from_blog_post_full() -> None:
    entity = from_blog_post(
        title="Hello",
        body_html="<p>World</p>",
        slug="hello-world",
        author="Jane",
        excerpt="Short excerpt",
        breadcrumbs=[{"name": "Home", "url": "/"}],
    )
    assert entity.slug == "hello-world"
    assert entity.author_name == "Jane"
    assert entity.excerpt == "Short excerpt"
    assert len(entity.breadcrumbs) == 1
    assert entity.breadcrumbs[0].name == "Home"


def test_from_product_minimal() -> None:
    entity = from_product(name="Widget", sku="W-001", price="29.99")
    assert entity.entity_type == "product"
    assert entity.title == "Widget"
    assert entity.sku == "W-001"
    assert entity.price == "29.99"
    assert entity.price_currency == "USD"
    assert entity.availability == "InStock"


def test_from_product_numeric_price() -> None:
    entity = from_product(name="Shoe", sku="S-001", price=99.99)
    assert entity.price == "99.99"


def test_from_product_with_breadcrumbs() -> None:
    entity = from_product(
        name="Shoe", sku="S-001", price=49.99,
        breadcrumbs=[{"name": "Shop", "url": "/shop"}, {"name": "Shoes", "url": "/shop/shoes"}],
    )
    assert len(entity.breadcrumbs) == 2
    assert entity.breadcrumbs[1].name == "Shoes"


def test_from_faq_minimal() -> None:
    entity = from_faq(questions=[{"question": "Q?", "answer": "A."}])
    assert entity.entity_type == "faq"
    assert len(entity.faq_items) == 1
    assert entity.faq_items[0].question == "Q?"
    assert entity.faq_items[0].answer == "A."


def test_from_faq_multiple() -> None:
    entity = from_faq(
        questions=[
            {"question": "Q1", "answer": "A1"},
            {"question": "Q2", "answer": "A2"},
        ],
        title="FAQ Page",
        description="Frequently asked questions",
    )
    assert entity.title == "FAQ Page"
    assert entity.excerpt == "Frequently asked questions"
    assert len(entity.faq_items) == 2


def test_from_faq_with_breadcrumbs() -> None:
    entity = from_faq(
        questions=[{"question": "Q1", "answer": "A1"}],
        breadcrumbs=[
            {"name": "Home", "url": "/"},
            {"name": "FAQ", "url": "/faq"},
        ],
    )
    assert len(entity.breadcrumbs) == 2
    assert entity.breadcrumbs[0].name == "Home"
    assert entity.breadcrumbs[1].name == "FAQ"
