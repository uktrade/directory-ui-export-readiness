import pytest

from django.template.exceptions import TemplateDoesNotExist

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


@pytest.mark.parametrize('seconds,expected', (
	(59, 'Less than 1 minute'),
	(60, '1 min'),
	(61, '1 min'),
	(120, '2 mins'),
	(180, '3 mins'),
	(600, '10 mins'),
	(6000, '100 mins'),
))
def test_time_to_read(seconds, expected):
	assert article_tags.time_to_read(seconds) == expected
