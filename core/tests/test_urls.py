import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'view_name,expected_url',
    (
        ('landing-page', '/'),
        ('landing-page-international', '/international'),
        ('sorry', '/sorry'),
        ('not-found', '/not-found'),
        ('finance', '/finance'),
        (
                'get-finance-support',
                '/finance/get-finance-support-from-government'
        ),
        ('about', '/about'),
        ('privacy-cookies', '/privacy-cookies'),
        ('terms-conditions', '/terms-conditions')
    )
)
def test_reverse_urls(view_name, expected_url):
    assert reverse(view_name) == expected_url
