import http

from django.core.urlresolvers import reverse

import pytest

from conf.url_redirects import (
    TOS_AND_PRIVACY_REDIRECT_LANGUAGES,
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


# the first element needs to end with a slash
redirects = [
    (
        '/future/',
        'https://www.events.great.gov.uk/ehome/index.php?eventid=200185206'
    ),
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
    ('/export/new/', '/advice/'),
    ('/export/occasional/', '/advice/'),
    ('/export/regular/', '/advice/'),
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


@pytest.mark.parametrize(
    'incoming_url,expected_url',
    [
        (
                '/market-research/',
                '/advice/find-an-export-market/'
        ),

        (
                '/market-research/do-research-first/',
                '/advice/find-an-export-market/plan-export-market-research'
        ),

        (
                '/market-research/define-market-potential/',
                '/advice/find-an-export-market/define-export-market-potential'
        ),

        (
                '/market-research/analyse-the-competition/',
                '/advice/find-an-export-market/define-export-market-potential'
        ),

        (
                '/market-research/research-your-market/',
                '/advice/find-an-export-market/field-research-in-export-markets'  # NOQA
        ),

        (
                '/market-research/visit-a-trade-show/',
                '/advice/find-an-export-market/trade-shows'
        ),

        (
                '/market-research/doing-business-with-integrity/',
                '/advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets'  # NOQA
        ),

        (
                '/market-research/know-the-relevant-legislation/',
                '/advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets'  # NOQA
        ),

        (
                '/business-planning/',
                '/advice/define-route-to-market/'
        ),

        (
                '/business-planning/make-an-export-plan/',
                '/advice/create-an-export-plan/how-to-create-an-export-plan'
        ),

        (
                '/business-planning/find-a-route-to-market/',
                '/advice/define-route-to-market/routes-to-market'
        ),

        (
                '/business-planning/sell-overseas-directly/',
                '/advice/define-route-to-market/sell-overseas-directly'
        ),

        (
                '/business-planning/use-an-overseas-agent/',
                '/advice/define-route-to-market/export-agents'
        ),

        (
                '/business-planning/choosing-an-agent-or-distributor/',
                '/advice/define-route-to-market/export-agents'
        ),

        (
                '/business-planning/use-a-distributor/',
                '/advice/define-route-to-market/export-distributors'
        ),

        (
                '/business-planning/license-your-product-or-service/',
                '/advice/define-route-to-market/create-a-licensing-agreement'
        ),

        (
                '/business-planning/licensing-and-franchising/',
                '/advice/define-route-to-market/create-a-licensing-agreement'
        ),

        (
                '/business-planning/franchise-your-business/',
                '/advice/define-route-to-market/create-a-franchise-agreement'
        ),

        (
                '/business-planning/start-a-joint-venture/',
                '/advice/define-route-to-market/create-a-joint-venture-agreement'  # NOQA
        ),

        (
                '/business-planning/set-up-an-overseas-operation/',
                '/advice/define-route-to-market/set-up-a-business-abroad'
        ),

        (
                '/finance/',
                '/advice/get-export-finance-and-funding/'
        ),

        (
                '/finance/choose-the-right-finance/',
                '/advice/get-export-finance-and-funding/choose-the-right-finance'  # NOQA
        ),

        (
                '/finance/get-money-to-export/',
                '/advice/get-export-finance-and-funding/choose-the-right-finance'  # NOQA
        ),

        (
                '/finance/get-export-finance/',
                '/advice/get-export-finance-and-funding/get-export-finance'
        ),

        (
                '/finance/get-finance-support-from-government/',
                '/advice/get-export-finance-and-funding/get-export-finance'
        ),

        (
                '/finance/raise-money-by-borrowing/',
                '/advice/get-export-finance-and-funding/raise-money-by-borrowing'  # NOQA
        ),

        (
                '/finance/borrow-against-assets/',
                '/advice/get-export-finance-and-funding/borrow-against-assets'
        ),

        (
                '/finance/raise-money-with-investment/',
                '/advice/get-export-finance-and-funding/raise-money-with-investment'  # NOQA
        ),
        (
                '/getting-paid/',
                '/advice/manage-payment-for-export-orders/'
        ),

        (
                '/getting-paid/invoice-currency-and-contents/',
                '/advice/manage-payment-for-export-orders/payment-methods-for-exporters'  # NOQA
        ),

        (
                '/getting-paid/consider-how-youll-get-paid/',
                '/advice/manage-payment-for-export-orders/how-to-create-an-export-invoice'  # NOQA
        ),

        (
                '/getting-paid/decide-when-youll-get-paid/',
                '/advice/manage-payment-for-export-orders/decide-when-youll-get-paid-for-export-orders'  # NOQA
        ),

        (
                '/getting-paid/payment-methods/',
                '/advice/manage-payment-for-export-orders/payment-methods-for-exporters'  # NOQA
        ),

        (
                '/getting-paid/insure-against-non-payment/',
                '/advice/manage-payment-for-export-orders/insure-against-non-payment'  # NOQA
        ),

        (
                '/customer-insight/',
                '/advice/prepare-to-do-business-in-a-foreign-country/'
        ),

        (
                '/customer-insight/meet-your-customers/',
                '/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market'  # NOQA
        ),

        (
                '/customer-insight/know-your-customers/',
                '/advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets'  # NOQA
        ),

        (
                '/customer-insight/manage-language-differences/',
                '/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market'  # NOQA
        ),

        (
                '/customer-insight/understand-your-customers-culture/',
                '/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market'  # NOQA
        ),

        (
                '/operations-and-compliance/',
                '/advice/manage-legal-and-ethical-compliance/'
        ),

        (
                '/operations-and-compliance/internationalise-your-website/',
                '/advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website'  # NOQA
        ),

        (
                '/operations-and-compliance/match-your-website-to-your-audience/',  # NOQA
                '/advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website'  # NOQA
        ),

        (
                '/operations-and-compliance/protect-your-intellectual-property/',  # NOQA
                '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        ),

        (
                '/operations-and-compliance/types-of-intellectual-property/',
                '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        ),

        (
                '/operations-and-compliance/know-what-ip-you-have/',
                '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        ),

        (
                '/operations-and-compliance/international-ip-protection/',
                '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting'  # NOQA
        ),
        (
                '/operations-and-compliance/report-corruption/',
                '/advice/manage-legal-and-ethical-compliance/report-corruption-and-human-rights-violations'  # NOQA
        ),
        (
                '/operations-and-compliance/anti-bribery-and-corruption-training/',  # NOQA
                '/advice/manage-legal-and-ethical-compliance/anti-bribery-and-corruption-training'  # NOQA
        ),
        (
                '/operations-and-compliance/plan-the-logistics/',
                '/advice/prepare-for-export-procedures-and-logistics/plan-logistics-for-exporting'  # NOQA
        ),
        (
                '/operations-and-compliance/get-your-export-documents-right/',
                '/advice/prepare-for-export-procedures-and-logistics/get-your-export-documents-right'  # NOQA
        ),
        (
                '/operations-and-compliance/use-a-freight-forwarder/',
                '/advice/prepare-for-export-procedures-and-logistics/use-a-freight-forwarder-to-export'  # NOQA
        ),
        (
                '/operations-and-compliance/use-incoterms-in-contracts/',
                '/advice/prepare-for-export-procedures-and-logistics/use-incoterms-in-contracts'  # NOQA
        ),
        (
                '/new/next-steps/',
                '/advice'
        ),
        (
                '/occasional/next-steps/',
                '/advice'
        ),
        (
                '/regular/next-steps/',
                '/advice'
        ),
        (
                '/new/',
                '/advice'
        ),
        (
                '/occasional/',
                '/advice'
        ),
        (
                '/regular/',
                '/advice'
        ),
    ])
def redirect_articles(incoming_url, expected_url, client):
    response = client.get(incoming_url)
    assert response.status_code == 302
    assert response.url == expected_url
