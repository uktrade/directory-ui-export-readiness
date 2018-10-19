import pytest
from prototype.helpers import (
    unprefix_prototype_url, prefix_international_news_url
)

unprefix_urls = [
    ('/prototype/markets/', '/markets/'),
    ('/prototype/guidance/', '/guidance/'),
    ('/prototype/prototype-test-page/', '/prototype-test-page/'),
    ('/news/', '/news/'),
    ('/', '/'),
]

news_prefix_urls = [
    ('/international/news/', '/international/international-news/'),
    ('/international/news/test-page/',
        '/international/international-news/test-page/'),
    ('/international/news/international-news-test/',
        '/international/international-news/international-news-test/'),
    ('/news/', '/news/'),
    ('/international/', '/international/'),
    ('/', '/'),
]


@pytest.mark.parametrize('url,exp', unprefix_urls)
def test_unprefix_prototype_url(url, exp):
    assert unprefix_prototype_url(url) == exp


@pytest.mark.parametrize('url,exp', news_prefix_urls)
def test_prefix_international_news_url(url, exp):
    assert prefix_international_news_url(url) == exp
