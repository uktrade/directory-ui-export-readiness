import pytest
from prototype.helpers import unprefix_prototype_url

unprefix_urls = [
    ('/prototype/markets/', '/markets/'),
    ('/prototype/guidance/', '/guidance/'),
    ('/news/', '/news/'),
    ('/', '/'),
]


@pytest.mark.parametrize('url,exp', unprefix_urls)
def test_unprefix_prototype_url(url, exp):
    assert unprefix_prototype_url(url) == exp
