import pytest
from prototype.helpers import (
    unprefix_prototype_url, prefix_international_news_url
)

unprefix_urls = [
    ('/prototype/markets/', '/markets/'),
    ('/prototype/guidance/', '/guidance/'),
    ('/prototype/prototype-test-page/', '/prototype-test-page/'),
    ('/eu-exit-news/', '/eu-exit-news/'),
    ('/', '/'),
]

news_prefix_urls = [
    ('/international/eu-exit-news/', '/international/international-eu-exit-news/'), # noqa
    ('/international/eu-exit-news/test-page/',
        '/international/international-eu-exit-news/test-page/'),
    ('/international/eu-exit-news/international-eu-exit-news-test/',
        '/international/international-eu-exit-news/international-eu-exit-news-test/'), # noqa
    ('/eu-exit-news/', '/eu-exit-news/'),
    ('/international/', '/international/'),
    ('/', '/'),
]


@pytest.mark.parametrize('url,exp', unprefix_urls)
def test_unprefix_prototype_url(url, exp):
    assert unprefix_prototype_url(url) == exp


@pytest.mark.parametrize('url,exp', news_prefix_urls)
def test_prefix_international_news_url(url, exp):
    assert prefix_international_news_url(url) == exp
