import http

from django.core.urlresolvers import reverse

import pytest

from ui.urls import (
    TOS_AND_PRIVACY_REDIRECT_LANGUAGES,
    ARTICLE_REDIRECTS_MAPPING,
    INTERNATIONAL_TRANSLATION_REDIRECTS_MAPPING
)


UTM_QUERY_PARAMS = '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'


def add_utm_query_params(url):
    return '{url}{utm_query_params}'.format(
        url=url, utm_query_params=UTM_QUERY_PARAMS
    )

# Generate a list of URLs for all paths (e.g. /de and /int/de) with and without
# trailing slash
international_url_and_param_values = []
for path, lang_param_value in INTERNATIONAL_TRANSLATION_REDIRECTS_MAPPING:
    for url_pattern in ('/int/{path}/', '/int/{path}', '/{path}/', '/{path}'):
        international_url_and_param_values.append(
            (url_pattern.format(path=path), lang_param_value)
        )

INTERNATIONAL_REDIRECTS_PARAMS = (
    'url,expected_language', international_url_and_param_values
)


@pytest.mark.parametrize(*INTERNATIONAL_REDIRECTS_PARAMS)
def test_international_redirects_no_query_params(
    url, expected_language, client
):

    if not url.endswith('/'):
        url = client.get(url).url

    response = client.get(url, follow=False)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == '/international/?lang={expected_language}'.format(
        expected_language=expected_language
    )


@pytest.mark.parametrize(*INTERNATIONAL_REDIRECTS_PARAMS)
def test_international_redirects_query_params(
    url, expected_language, client
):

    if not url.endswith('/'):
        url = client.get(add_utm_query_params(url)).url
    else:
        url = add_utm_query_params(url)

    response = client.get(url, follow=False)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == (
        '/international/{utm_query_params}&lang={expected_language}'.format(
            utm_query_params=UTM_QUERY_PARAMS,
            expected_language=expected_language
        )
    )


@pytest.mark.parametrize('url', ('/int/', '/int'))
def test_int_international_redirect(url, client):
    if not url.endswith('/'):
        url = client.get(url).url
    response = client.get(url)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == reverse('landing-page-international')


@pytest.mark.parametrize('path', TOS_AND_PRIVACY_REDIRECT_LANGUAGES)
def test_tos_international_redirect(path, client):
    response = client.get(
        '/int/{path}/terms-and-conditions/'.format(path=path)
    )

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == reverse('terms-and-conditions-international')


@pytest.mark.parametrize('path', TOS_AND_PRIVACY_REDIRECT_LANGUAGES)
def test_privacy_international_redirect(path, client):
    response = client.get(
        '/int/{path}/privacy-policy/'.format(path=path)
    )

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == reverse('privacy-and-cookies-international')


@pytest.mark.parametrize(
    'url,expected_pattern',
    (
        ('/uk/terms-and-conditions/', 'terms-and-conditions'),
        ('/uk/privacy-policy/', 'privacy-and-cookies'),
        ('/uk/terms-and-conditions', 'terms-and-conditions'),
        ('/uk/privacy-policy', 'privacy-and-cookies'),

    )
)
def test_tos_privacy_redirects(url, expected_pattern, client):
    if not url.endswith('/'):
        url = client.get(url).url

    response = client.get(url)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == reverse(expected_pattern)

# Generate a list of URLs with and without trailing slash
article_url_and_patterns = []
for path, expected_pattern in ARTICLE_REDIRECTS_MAPPING:
    for url_pattern in ('/{path}/', '/{path}'):
        article_url_and_patterns.append(
            (url_pattern.format(path=path), expected_pattern)
        )


@pytest.mark.parametrize('url,expected_pattern', article_url_and_patterns)
def test_article_redirects(url, expected_pattern, client):
    if not url.endswith('/'):
        url = client.get(url).url

    response = client.get(url)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == reverse(expected_pattern)


@pytest.mark.parametrize('url,expected_pattern', article_url_and_patterns)
def test_article_redirects_query_params(url, expected_pattern, client):
    if not url.endswith('/'):
        url = client.get(add_utm_query_params(url)).url
    else:
        url = add_utm_query_params(url)

    response = client.get(url)

    assert response.status_code == http.client.MOVED_PERMANENTLY
    assert response.url == '{url}{utm_query_params}'.format(
       url=reverse(expected_pattern), utm_query_params=UTM_QUERY_PARAMS
    )
