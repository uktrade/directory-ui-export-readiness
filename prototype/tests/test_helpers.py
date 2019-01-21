import pytest
from prototype.helpers import prefix_international_news_url, unslugify

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

unslugify_slugs = [
    ('test-slug-one', 'Test slug one'),
    ('test-two', 'Test two'),
    ('slug', 'Slug'),
]


@pytest.mark.parametrize('url,exp', news_prefix_urls)
def test_prefix_international_news_url(url, exp):
    assert prefix_international_news_url(url) == exp


@pytest.mark.parametrize('slug,exp', unslugify_slugs)
def test_unslugify(slug, exp):
    assert unslugify(slug) == exp
