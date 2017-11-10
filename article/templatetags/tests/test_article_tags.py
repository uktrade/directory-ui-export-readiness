import pytest

from django.template.exceptions import TemplateDoesNotExist
from django.template.context import RequestContext
from django.urls import reverse

from article.templatetags import article_tags
from article import articles


def test_include_markdown_valid_template(rf):
    context = RequestContext(rf.get('/'), {})
    actual = article_tags.include_markdown(
        context, 'article/markdown/14_license-your-product-or-service.md',
    )

    assert actual is not None


def test_include_markdown_missing_template(rf):
    context = RequestContext(rf.get('/'), {})
    with pytest.raises(TemplateDoesNotExist):
        article_tags.include_markdown(
            context,
            'article/markdown/14_license-your-product-or-service-MISSING.md',
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


@pytest.mark.parametrize('current_source,expected', (
    ('persona_occasional', 'persona_occasional'),
    ('operations_and_compliance', 'market_research'),
    ('all', 'all'),
    ('market_research', 'market_research'),
))
def test_include_markdown_renders_source(rf, current_source, expected):
    article = articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE
    request = rf.get(article.url, {'source': current_source})
    context = RequestContext(request, {'request': request})

    html = article_tags.include_markdown(context, article.markdown_file_path)

    assert reverse('article-research-market') + '?source=' + expected in html
