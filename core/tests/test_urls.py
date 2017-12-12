import pytest
from django.urls import reverse


@pytest.mark.parametrize(
    'view_name,expected_url',
    (
        (
            'landing-page', '/'),
        (
            'landing-page-international',
            '/international/'
        ),
        (
            'not-found',
            '/not-found/'
        ),
        (
            'about',
            '/about/'
        ),
        (
            'privacy-and-cookies',
            '/privacy-and-cookies/'
        ),
        (
            'privacy-and-cookies-international',
            '/international/privacy-and-cookies/'
        ),
        (
            'terms-and-conditions',
            '/terms-and-conditions/'
        ),
        (
            'terms-and-conditions-international',
            '/international/terms-and-conditions/'
        ),
        (
            'get-finance',
            '/get-finance/'
        )
    )
)
def test_reverse_urls(view_name, expected_url):
    assert reverse(view_name) == expected_url
