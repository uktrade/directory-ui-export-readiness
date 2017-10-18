from django.template.exceptions import TemplateDoesNotExist
import pytest

from article.templatetags import article_tags


def test_include_markdown_valid_template():
    actual = article_tags.include_markdown(
        'article/markdown/14_license-your-product-or-service.md'
    )

    assert actual is not None


def test_include_markdown_missing_template():
    with pytest.raises(TemplateDoesNotExist):
        article_tags.include_markdown(
            'article/markdown/14_license-your-product-or-service-MISSING.md'
        )
