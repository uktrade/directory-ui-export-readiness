from django.conf.urls import url
from django.views.generic.base import RedirectView

import core.views


redirects = [
    url(
        r'^invest/$',
        RedirectView.as_view(
            url='https://invest.great.gov.uk',
            permanent=False,
            query_string=True
        ),
        name='redirect-invest'
    ),
    url(
        r'^int/invest/$',
        RedirectView.as_view(
            url='https://invest.great.gov.uk/int',
            permanent=False,
            query_string=True
        ),
        name='redirect-int-invest'
    ),
    url(
        r'^us/invest/$',
        RedirectView.as_view(
            url='https://invest.great.gov.uk/us',
            permanent=False,
            query_string=True
        ),
        name='redirect-us-invest'
    ),
    url(
        r'^cn/invest/$',
        RedirectView.as_view(
            url='https://invest.great.gov.uk/cn',
            permanent=False,
            query_string=True
        ),
        name='redirect-cn-invest'
    ),
    url(
        r'^de/invest/$',
        RedirectView.as_view(
            url='https://invest.great.gov.uk/de',
            permanent=False,
            query_string=True
        ),
        name='redirect-de-invest'
    ),
    url(
        r'^in/invest/$',
        RedirectView.as_view(
            url='https://invest.great.gov.uk/in',
            permanent=False,
            query_string=True
        ),
        name='redirect-in-invest'
    ),
    url(
        r'^study/$',
        RedirectView.as_view(
            url='https://study-uk.britishcouncil.org',
            permanent=False,
            query_string=True
        ),
        name='redirect-study'
    ),
    url(
        r'^visit/$',
        RedirectView.as_view(
            url='https://www.visitbritain.com/gb/en',
            permanent=False,
            query_string=True
        ),
        name='redirect-visit'
    ),
    url(
        r'^export/$',
        RedirectView.as_view(
            pattern_name='landing-page',
            permanent=False,
            query_string=True
        ),
        name='redirect-export'
    ),
    url(
        r'^export/opportunities/$',
        RedirectView.as_view(
            url='https://opportunities.export.great.gov.uk',
            permanent=False,
            query_string=True
        ),
        name='redirect-export-opportunities'
    ),
    url(
        r'^opportunities/$',
        RedirectView.as_view(
            url='https://opportunities.export.great.gov.uk',
            permanent=False,
            query_string=True
        ),
        name='redirect-opportunities'
    ),
    url(
        r'^export/find-a-buyer/$',
        RedirectView.as_view(
            url='https://find-a-buyer.export.great.gov.uk',
            permanent=False,
            query_string=True
        ),
        name='redirect-find-a-buyer'
    ),
    url(
        r'^export/selling-online-overseas/$',
        RedirectView.as_view(
            url='https://selling-online-overseas.export.great.gov.uk',
            permanent=False,
            query_string=True
        ),
        name='redirect-find-a-buyer'
    ),
    url(
        r'^trade/$',
        RedirectView.as_view(
            url='https://trade.great.gov.uk',
            permanent=False,
            query_string=True
        ),
        name='redirect-trade'
    ),
    url(
        r'^uk/privacy-policy/$',
        RedirectView.as_view(
            pattern_name='privacy-and-cookies',
            permanent=False,
            query_string=True
        ),
        name='redirect-privacy-policy-uk'
    ),
    url(
        r'^uk/terms-and-conditions/$',
        RedirectView.as_view(
            pattern_name='terms-and-conditions',
            permanent=False,
            query_string=True
        ),
        name='redirect-terms-and-conditions-uk'
    ),
    url(
        r'^uk/$',
        core.views.TranslationRedirectView.as_view(
            pattern_name='landing-page',
        ),
        name='redirect-uk'
    ),
    url(
        r'^int/$',
        core.views.TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
        name='redirect-int'
    ),
    url(
        r'^in/$',
        core.views.TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
        name='redirect-in'
    ),
    url(
        r'^us/$',
        core.views.TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
        name='redirect-us'
    ),
    url(
        r'^innovation/$',
        RedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/'
                'the-great-festival-of-innovation-hong-kong-2018/'
            ),
            permanent=False,
            query_string=True
        ),
        name='redirect-invest'
    ),
]


# (<lang code path>, <language to use in query parameter>)
INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING = [
    ('de', 'de'),
    ('ar', 'ar'),
    ('zh', 'zh-hans'),
    ('pt', 'pt'),
    ('es', 'es'),
    ('ja', 'ja'),
]
international_redirects = [
    url(
        r'^int/{path}/$'.format(path=redirect[0]),
        core.views.TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
            language=redirect[1],
        ),
        name='redirect-int-{}'.format(redirect[0])
    ) for redirect in INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING
]
# (<country code path>, <language to use in query parameter>)
INTERNATIONAL_COUNTRY_REDIRECTS_MAPPING = [
    ('cn', 'zh-hans'),
    ('br', 'pt'),
    ('jp', 'ja'),
]
international_redirects += [
    url(
        r'^{path}/$'.format(path=redirect[0]),
        core.views.TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
            language=redirect[1],
        ),
        name='redirect-{path}'.format(path=redirect[0])
    ) for redirect in (
        INTERNATIONAL_LANGUAGE_REDIRECTS_MAPPING +
        INTERNATIONAL_COUNTRY_REDIRECTS_MAPPING
    )
]


# TOS and privacy-and-cookies are no longer translated, instead we redirect to
# the ENG version
TOS_AND_PRIVACY_REDIRECT_LANGUAGES = (
    'zh', 'ja', r'es', 'pt', 'ar', 'de'
)

tos_redirects = [
    url(
        r'^int/{path}/terms-and-conditions/$'.format(path=language),
        RedirectView.as_view(
            pattern_name='terms-and-conditions-international',
            permanent=False,
            query_string=True
        ),
        name='redirect-terms-and-conditions-{path}'.format(
            path=language
        )
    ) for language in TOS_AND_PRIVACY_REDIRECT_LANGUAGES
]

privacy_redirects = [
    url(
        r'^int/{path}/privacy-policy/$'.format(
            path=language
        ),
        RedirectView.as_view(
            pattern_name='privacy-and-cookies-international',
            permanent=False,
            query_string=True
        ),
        name='redirect-privacy-policy-{path}'.format(
            path=language
        )
    ) for language in TOS_AND_PRIVACY_REDIRECT_LANGUAGES
]

# (<path>, <pattern to redirect to>)
ARTICLE_REDIRECTS_MAPPING = (
    (
        'find-out-if-a-potential-customer-is-creditworthy',
        'decide-when-youll-get-paid'
    ),
    (
        'get-ready-to-manage-regulations-legal-issues-and-risk',
        'article-list-operations-and-compliance'
    ),
    (
        'get-your-finances-ready',
        'get-money-to-export'
    ),
    (
        'get-your-team-and-your-business-ready',
        'make-an-export-plan'
    ),
    (
        'getting-paid-and-being-competitive',
        'decide-when-youll-get-paid'
    ),
    (
        'getting-ready-to-sell-overseas',
        'article-research-market'
    ),
    (
        'grow-your-export-business',
        'article-list-persona-occasional'
    ),
    (
        'help-for-exporters-from-finance-partners',
        'article-list-finance'
    ),
    (
        'make-sure-your-online-presence-is-legal',
        'sell-overseas-directly'
    ),
    (
        'methods-used-to-research-export-markets',
        'article-list-market-research'
    ),
    (
        'new-partners-page-for-logistics',
        'article-list-operations-and-compliance'
    ),
    (
        'reach-overseas-customers-online',
        'sell-overseas-directly'
    ),
    (
        'research-your-market',
        'article-research-market'
    ),
    (
        'routes-to-market',
        'find-a-route-to-market'
    ),
    (
        'selling-direct-to-customers-overseas',
        'sell-overseas-directly'
    ),
    (
        'selling-overseas-an-experts-view',
        'article-research-market'
    ),
    (
        'selling-overseas',
        'article-list-persona-new'
    ),
    (
        'setting-up-an-overseas-operation',
        'set-up-an-overseas-operation'
    ),
    (
        'shipping-and-logistics',
        'plan-the-logistics'
    ),
    (
        'simplifying-customs-and-licences',
        'plan-the-logistics'
    ),
    (
        'use-social-media-and-commerce-to-export',
        'sell-overseas-directly'
    ),
    (
        'ways-to-grow-your-exports',
        'article-list-persona-regular'
    ),
    (
        'write-an-export-plan',
        'make-an-export-plan'
    ),
    (
        'clear-goals-for-face-to-face-meetings',
        'meet-your-customers',
    ),
    (
        'face-to-face-communication',
        'meet-your-customers',
    ),
    (
        'finance-for-export',
        'get-export-finance',
    )
)

article_redirects = [
    url(
        r'^{path}/$'.format(path=redirect[0]),
        RedirectView.as_view(
            pattern_name=redirect[1],
            permanent=False,
            query_string=True
        ),
        name='redirect-{path}'.format(path=redirect[0])
    ) for redirect in ARTICLE_REDIRECTS_MAPPING
]

redirects += (
    article_redirects + tos_redirects +
    privacy_redirects + international_redirects
)
