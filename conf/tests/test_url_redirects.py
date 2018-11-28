import http

from django.core.urlresolvers import reverse

import pytest

from conf.url_redirects import (
    TOS_AND_PRIVACY_REDIRECT_LANGUAGES,
    ARTICLE_REDIRECTS_MAPPING,
    INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING,
    INTERNATIONAL_COUNTRY_REDIRECTS_MAPPING
)


UTM_QUERY_PARAMS = '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'


def add_utm_query_params(url):
    return '{url}{utm_query_params}'.format(
        url=url, utm_query_params=UTM_QUERY_PARAMS
    )


def get_redirect_mapping_param_values(redirect_mapping, url_patterns):
    param_values = []
    for path, expected in redirect_mapping:
        for url_pattern in (url_patterns):
            param_values.append(
                (url_pattern.format(path=path), expected)
            )

    return param_values


# Generate a list of URLs for all paths (e.g. /de and /int/de) with and without
# trailing slash
language_redirects = get_redirect_mapping_param_values(
    redirect_mapping=INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING,
    url_patterns=('/int/{path}/', '/int/{path}', '/{path}/', '/{path}')
)
country_redirects = get_redirect_mapping_param_values(
        redirect_mapping=INTERNATIONAL_COUNTRY_REDIRECTS_MAPPING,
        url_patterns=('/{path}/', '/{path}')
)
INTERNATIONAL_REDIRECTS_PARAMS = (
    'url,expected_language', language_redirects + country_redirects
)


@pytest.mark.parametrize(*INTERNATIONAL_REDIRECTS_PARAMS)
def test_international_redirects_no_query_params(
    url, expected_language, client
):

    if not url.endswith('/'):
        url = client.get(url).url

    response = client.get(url, follow=False)

    assert response.status_code == http.client.FOUND
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

    assert response.status_code == http.client.FOUND
    assert response.url == (
        '/international/{utm_query_params}&lang={expected_language}'.format(
            utm_query_params=UTM_QUERY_PARAMS,
            expected_language=expected_language
        )
    )


@pytest.mark.parametrize('path', TOS_AND_PRIVACY_REDIRECT_LANGUAGES)
def test_tos_international_redirect(path, client):
    response = client.get(
        '/int/{path}/terms-and-conditions/'.format(path=path)
    )

    assert response.status_code == http.client.FOUND
    assert response.url == reverse('terms-and-conditions-international')


@pytest.mark.parametrize('path', TOS_AND_PRIVACY_REDIRECT_LANGUAGES)
def test_privacy_international_redirect(path, client):
    response = client.get(
        '/int/{path}/privacy-policy/'.format(path=path)
    )

    assert response.status_code == http.client.FOUND
    assert response.url == reverse('privacy-and-cookies-international')


# Generate a list of URLs with and without trailing slash
ARTICLE_REDIRECT_PARAMS = (
    'url,expected_pattern', get_redirect_mapping_param_values(
        redirect_mapping=ARTICLE_REDIRECTS_MAPPING,
        url_patterns=('/{path}/', '/{path}')
    )
)


@pytest.mark.parametrize(*ARTICLE_REDIRECT_PARAMS)
def test_article_redirects(url, expected_pattern, client):
    if not url.endswith('/'):
        url = client.get(url).url

    response = client.get(url)

    assert response.status_code == http.client.FOUND
    assert response.url == reverse(expected_pattern)


@pytest.mark.parametrize(*ARTICLE_REDIRECT_PARAMS)
def test_article_redirects_query_params(url, expected_pattern, client):
    if not url.endswith('/'):
        url = client.get(add_utm_query_params(url)).url
    else:
        url = add_utm_query_params(url)

    response = client.get(url)

    assert response.status_code == http.client.FOUND
    assert response.url == '{url}{utm_query_params}'.format(
       url=reverse(expected_pattern), utm_query_params=UTM_QUERY_PARAMS
    )


# the first element needs to end with a slash
redirects = [
    ('/bodw2019/', 'https://www.events.great.gov.uk/bodw2019/'),
    ('/events/', 'https://www.events.great.gov.uk/'),
    ('/ukpavilion2020/', 'https://www.events.trade.gov.uk/dubai-expo-2020/'),
    ('/expo2020/', 'https://www.events.trade.gov.uk/dubai-expo-2020/'),
    ('/invest/', 'https://invest.great.gov.uk'),
    ('/int/invest/', 'https://invest.great.gov.uk/int'),
    ('/us/invest/', 'https://invest.great.gov.uk/us'),
    ('/cn/invest/', 'https://invest.great.gov.uk/cn'),
    ('/de/invest/', 'https://invest.great.gov.uk/de'),
    ('/in/invest/', 'https://invest.great.gov.uk/in'),

    ('/es/invest/', 'https://invest.great.gov.uk/es'),
    ('/int/es/invest/', 'https://invest.great.gov.uk/int/es'),
    ('/int/zh/invest/', 'https://invest.great.gov.uk/int/zh'),
    ('/int/pt/invest/', 'https://invest.great.gov.uk/int/pt'),
    ('/br/invest/', 'https://invest.great.gov.uk/br'),
    ('/int/de/invest/', 'https://invest.great.gov.uk/int/de'),
    ('/jp/invest/', 'https://invest.great.gov.uk/jp'),
    ('/int/ja/invest/', 'https://invest.great.gov.uk/int/ja'),
    ('/int/ar/invest/', 'https://invest.great.gov.uk/int/ar'),
    ('/study/', 'https://study-uk.britishcouncil.org'),
    ('/visit/', 'https://www.visitbritain.com/gb/en'),
    ('/export/', 'landing-page'),
    ('/export/new/', 'article-list-persona-new'),
    ('/export/occasional/', 'article-list-persona-occasional'),
    ('/export/regular/', 'article-list-persona-regular'),
    ('/export/opportunities/', 'https://opportunities.export.great.gov.uk/'),
    (
        '/opportunities/',
        'https://opportunities.export.great.gov.uk/'
    ),
    (
        (
            '/opportunities/usa-'
            'centre-for-medicare-and-medicaid-services-hospital-improvement'
            '-innovation-network-hiin-rfp/'
        ),
        (
            'https://opportunities.export.great.gov.uk/opportunities/usa-'
            'centre-for-medicare-and-medicaid-services-hospital-improvement'
            '-innovation-network-hiin-rfp/'
        )
    ),
    (
        (
            '/opportunities/usa-'
            'centre-for-medicare-and-medicaid-services-hospital-improvement'
            '-innovation-network-hiin-rfp/'
            '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'
        ),
        (
            'https://opportunities.export.great.gov.uk/opportunities/usa-'
            'centre-for-medicare-and-medicaid-services-hospital-improvement'
            '-innovation-network-hiin-rfp/'
            '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'
        )
    ),
    (
        (
            '/opportunities/'
            'mexico-craft-beer-distributor-looking-for-international-brands/'
        ),
        (
            'https://opportunities.export.great.gov.uk/opportunities/'
            'mexico-craft-beer-distributor-looking-for-international-brands/'
        )
    ),
    (
        (
            '/opportunities/'
            'mexico-craft-beer-distributor-looking-for-international-brands/'
            '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'
        ),
        (
            'https://opportunities.export.great.gov.uk/opportunities/'
            'mexico-craft-beer-distributor-looking-for-international-brands/'
            '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'
        )
    ),
    (
        (
            '/opportunities/'
            'taiwan-2018-flora-expo-seeking'
            '-suppliers-to-help-develop-exhibition/'
        ),
        (
            'https://opportunities.export.great.gov.uk/opportunities/'
            'taiwan-2018-flora-expo-seeking'
            '-suppliers-to-help-develop-exhibition/'
        )
    ),
    (
        (
            '/opportunities/'
            'taiwan-2018-flora-expo-seeking'
            '-suppliers-to-help-develop-exhibition/'
            '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'
        ),
        (
            'https://opportunities.export.great.gov.uk/opportunities/'
            'taiwan-2018-flora-expo-seeking'
            '-suppliers-to-help-develop-exhibition/'
            '?utm_source=test%12&utm_medium=test&utm_campaign=test%test'
        )
    ),
    ('/export/find-a-buyer/', 'https://find-a-buyer.export.great.gov.uk'),
    (
        '/export/selling-online-overseas/',
        'https://selling-online-overseas.export.great.gov.uk'
    ),
    ('/trade/', 'https://trade.great.gov.uk'),
    ('/uk/privacy-policy/', 'privacy-and-cookies'),
    ('/uk/terms-and-conditions/', 'terms-and-conditions'),
    ('/int/', 'landing-page-international'),
    ('/uk/', 'landing-page'),
    ('/in/', 'landing-page-international'),
    ('/us/', 'landing-page-international'),
    ('/innovation/', (
        'https://www.events.trade.gov.uk/'
        'the-great-festival-of-innovation-hong-kong-2018/'
    )),
    ('/uk/cy/', (
        'https://www.great.gov.uk/?utm_source=Mailing&utm_medium'
        '=Brochure&utm_campaign=ExportBrochureCY'
    )),
    ('/verify/', (
        'https://find-a-buyer.export.great.gov.uk/'
        'verify/letter-confirm/'
    )),
    ('/legal/', (
        'https://trade.great.gov.uk/'
        'campaign/legal-is-great/singapore/'
    )),
    ('/kr/', (
        'https://www.events.trade.gov.uk/invest-in-great---korea'
        '?utm_source=print&utm_campaign=korean_winter_olympics_invest'
    )),
    (
        '/legacy/contact/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'})
    ),
    (
        '/legacy/contact/contact/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'})
    ),
    (
        '/legacy/contact/directory/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'})
    ),
    (
        '/legacy/contact/directory/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/eig/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'})
    ),
    (
        '/legacy/contact/export-opportunities/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/export_opportunities/',
        reverse('contact-us-routing-form', kwargs={'step': 'domestic'})
    ),
    (
        '/legacy/contact/export_opportunities/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/export_ops/',
        reverse('contact-us-routing-form', kwargs={'step': 'domestic'})
    ),
    (
        '/legacy/contact/export_readiness/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    ('/legacy/contact/feedback/', reverse('contact-us-feedback')),
    ('/legacy/contact/feedback/datahub/', reverse('contact-us-feedback')),
    ('/legacy/contact/feedback/directory/', reverse('contact-us-feedback')),
    ('/legacy/contact/feedback/e_navigator/', reverse('contact-us-feedback')),
    ('/legacy/contact/feedback/eig/', reverse('contact-us-feedback')),
    ('/legacy/contact/feedback/export_ops/', reverse('contact-us-feedback')),
    (
        '/legacy/contact/feedback/exportingisgreat/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/feedback/exportopportunities/',
        reverse('contact-us-feedback')
    ),
    ('/legacy/contact/feedback/invest/', reverse('contact-us-feedback')),
    (
        '/legacy/contact/feedback/opportunities/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/feedback/selling-online-overseas/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/feedback/selling_online_overseas/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/feedback/single_sign_on/',
        reverse('contact-us-feedback')
    ),
    ('/legacy/contact/feedback/soo/', reverse('contact-us-feedback')),
    ('/legacy/contact/feedback/sso/', reverse('contact-us-feedback')),
    ('/legacy/contact/invest/FeedbackForm/', reverse('contact-us-feedback')),
    (
        '/legacy/contact/opportunities/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/selling_online_overseas/',
        reverse('contact-us-routing-form', kwargs={'step': 'domestic'})
    ),
    (
        '/legacy/contact/selling_online_overseas/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/single_sign_on/',
        reverse('contact-us-routing-form', kwargs={'step': 'great-account'})
    ),
    (
        '/legacy/contact/single_sign_on/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/soo/feedback/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/soo/FeedbackForm/',
        reverse('contact-us-feedback')
    ),
    (
        '/legacy/contact/soo/Triage/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
    ),
    (
        '/legacy/contact/soo/TriageForm/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
    ),
    (
        '/legacy/contact/triage/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
    ),
    (
        '/legacy/contact/triage/directory/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
    ),
    (
        '/legacy/contact/triage/soo/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
    ),
    (
        '/legacy/contact/triage/sso/',
        reverse('contact-us-routing-form', kwargs={'step': 'location'}),
    ),
    (
        '/legacy/contact/cookies/',
        reverse('privacy-and-cookies')
    ),
    (
        '/legacy/contact/terms-and-conditions/',
        reverse('terms-and-conditions')
    ),
]


@pytest.mark.parametrize('url,expected', redirects)
def test_redirects(url, expected, client):
    response = client.get(url)

    assert response.status_code == http.client.FOUND
    if not expected.startswith('http') and not expected.startswith('/'):
        expected = reverse(expected)

    assert response.url == expected


# add urls with no trailing slash
redirects_no_slash = [
    (redirect[0].split('?')[0][:-1], redirect[1]) for redirect in redirects
]


@pytest.mark.parametrize('url,expected', redirects_no_slash)
def test_redirects_no_trailing_slash(url, expected, client):
    response = client.get(url)
    assert response.status_code == http.client.MOVED_PERMANENTLY, url
