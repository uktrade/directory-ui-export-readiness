from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.views.generic.base import RedirectView

from core.views import (
    OpportunitiesRedirectView, TranslationRedirectView, QuerystringRedirectView
)


redirects = [
    url(
        r'^ukpavilion2020/$',
        RedirectView.as_view(
            url='https://www.events.trade.gov.uk/dubai-expo-2020/'),
        name='redirect-uk-pavilion'
    ),
    url(
        r'^exporting-edge/$',
        RedirectView.as_view(pattern_name='get-finance'),
        name='redirect-exporting-edge'
    ),
    url(
        r'^invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk'),
        name='redirect-invest'
    ),
    url(
        r'^int/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/int'),
        name='redirect-int-invest'
    ),
    url(
        r'^us/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/us'),
        name='redirect-us-invest'
    ),
    url(
        r'^es/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/es'),
        name='redirect-es-invest'
    ),
    url(
        r'^int/es/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/es',
        ),
        name='redirect-int-es-invest'
    ),
    url(
        r'^cn/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/cn'),
        name='redirect-cn-invest'
    ),
    url(
        r'^int/zh/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/zh',
        ),
        name='redirect-int-zh-invest'
    ),
    url(
        r'^int/pt/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/pt',
        ),
        name='redirect-int-pt-invest'
    ),
    url(
        r'^br/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/br'),
        name='redirect-br-invest'
    ),
    url(
        r'^de/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/de'),
        name='redirect-de-invest'
    ),
    url(
        r'^int/de/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/de',
        ),
        name='redirect-int-de-invest'
    ),
    url(
        r'^jp/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/jp'),
        name='redirect-jp-invest'
    ),
    url(
        r'^int/ja/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/ja',
        ),
        name='redirect-int-ja-invest'
    ),
    url(
        r'^in/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/in'),
        name='redirect-in-invest'
    ),
    url(
        r'^int/ar/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/ar',
        ),
        name='redirect-int-ar-invest'
    ),
    url(
        r'^study/$',
        QuerystringRedirectView.as_view(
            url='https://study-uk.britishcouncil.org',
        ),
        name='redirect-study'
    ),
    url(
        r'^visit/$',
        QuerystringRedirectView.as_view(
            url='https://www.visitbritain.com/gb/en',
        ),
        name='redirect-visit'
    ),
    url(
        r'^export/$',
        QuerystringRedirectView.as_view(pattern_name='landing-page'),
        name='redirect-export'
    ),
    url(
        r'^export/new/$',
        QuerystringRedirectView.as_view(
            pattern_name='article-list-persona-new',
        ),
        name='redirect-export-new'
    ),
    url(
        r'^export/occasional/$',
        QuerystringRedirectView.as_view(
            pattern_name='article-list-persona-occasional',
        ),
        name='redirect-export-occasional'
    ),
    url(
        r'^export/regular/$',
        QuerystringRedirectView.as_view(
            pattern_name='article-list-persona-regular',
        ),
        name='redirect-export-regular'
    ),
    url(
        r'^export/opportunities/$',
        QuerystringRedirectView.as_view(
            url='https://opportunities.export.great.gov.uk/',
        ),
        name='redirect-export-opportunities'
    ),
    url(
        r'^opportunities/$',
        QuerystringRedirectView.as_view(
            url='https://opportunities.export.great.gov.uk/',
        ),
        name='redirect-opportunities'
    ),
    url(
        r'^opportunities/(?P<slug>[-\w]+)/$',
        # Redirects to https://opportunities.export.great.gov.uk/opportunities
        # with the slug and query parameters
        OpportunitiesRedirectView.as_view(),
        name='redirect-opportunities-slug'
    ),
    url(
        r'^export/find-a-buyer/$',
        QuerystringRedirectView.as_view(
            url='https://find-a-buyer.export.great.gov.uk',
        ),
        name='redirect-find-a-buyer'
    ),
    url(
        r'^export/selling-online-overseas/$',
        QuerystringRedirectView.as_view(
            url='https://selling-online-overseas.export.great.gov.uk',
        ),
        name='redirect-find-a-buyer'
    ),
    url(
        r'^trade/$',
        QuerystringRedirectView.as_view(url='https://trade.great.gov.uk'),
        name='redirect-trade'
    ),
    url(
        r'^uk/privacy-policy/$',
        QuerystringRedirectView.as_view(pattern_name='privacy-and-cookies'),
        name='redirect-privacy-policy-uk'
    ),
    url(
        r'^uk/terms-and-conditions/$',
        QuerystringRedirectView.as_view(pattern_name='terms-and-conditions'),
        name='redirect-terms-and-conditions-uk'
    ),
    url(
        r'^uk/$',
        TranslationRedirectView.as_view(pattern_name='landing-page'),
        name='redirect-uk'
    ),
    url(
        r'^int/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
        name='redirect-int'
    ),
    url(
        r'^in/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
        name='redirect-in'
    ),
    url(
        r'^us/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
        name='redirect-us'
    ),
    url(
        r'^innovation/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/'
                'the-great-festival-of-innovation-hong-kong-2018/'
            ),
        ),
        name='redirect-innovation'
    ),
    url(
        r'^uk/cy/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.great.gov.uk/?utm_source=Mailing&utm_medium'
                '=Brochure&utm_campaign=ExportBrochureCY'
            ),
        ),
        name='redirect-uk-cy'
    ),
    url(
        r'^verify/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://find-a-buyer.export.great.gov.uk/'
                'verify/letter-confirm/'
            ),
        ),
        name='redirect-verify'
    ),
    url(
        r'^legal/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://trade.great.gov.uk/'
                'campaign/legal-is-great/singapore/'
            ),
        ),
        name='redirect-legal'
    ),
    url(
        r'^kr/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/invest-in-great---korea'
                '?utm_source=print&utm_campaign=korean_winter_olympics_invest'
            )
        ),
        name='redirect-kr'
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
        TranslationRedirectView.as_view(
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
        TranslationRedirectView.as_view(
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
        QuerystringRedirectView.as_view(
            pattern_name='terms-and-conditions-international',
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
        QuerystringRedirectView.as_view(
            pattern_name='privacy-and-cookies-international',
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
        QuerystringRedirectView.as_view(
            pattern_name=redirect[1],
        ),
        name='redirect-{path}'.format(path=redirect[0])
    ) for redirect in ARTICLE_REDIRECTS_MAPPING
]

contact_redirects = [
    url(
        r'^help/triage/(?P<service>[-\w\d]+)/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-triage-wizard',
        ),
    ),
    url(
        r'^help/(?P<service>[-\w\d]+)/TriageForm/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-triage-wizard',
        ),
    ),
    url(
        r'^help/(?P<service>[-\w\d]+)/Triage/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-triage-wizard',
        ),
    ),
    url(
        r'^help/triage/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-triage-wizard',
                kwargs={'service': 'selling-online-overseas'}
            ),
        ),
    ),
    url(
        r'^help/(?P<service>[-\w\d]+)/FeedbackForm/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-service-specific',
        ),
    ),
    url(
        r'^help/feedback/(?P<service>[-\w\d]+)/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-service-specific',
        ),
    ),
    url(
        r'^help/feedback/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-interstitial-service-agnostic',
        ),
    ),
    url(
        r'^help/(?P<service>[-\w\d]+)/feedback/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-service-specific',
        ),
    ),
    url(
        r'^help/single_sign_on/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-interstitial-service-specific',
                kwargs={'service': 'single_sign_on'}
            ),
        ),
    ),
    url(
        r'^help/selling_online_overseas/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-interstitial-service-specific',
                kwargs={'service': 'selling_online_overseas'}
            ),
        ),
    ),
    url(
        r'^help/export_ops/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-interstitial-service-specific',
                kwargs={'service': 'export_ops'}
            ),
        ),
    ),
    url(
        r'^help/export_opportunities/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-interstitial-service-specific',
                kwargs={'service': 'export_opportunities'}
            ),
        ),
    ),
    url(
        r'^help/eig/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-interstitial-service-specific',
                kwargs={'service': 'eig'}
            ),
        ),
    ),
    url(
        r'^help/directory/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-interstitial-service-specific',
                kwargs={'service': 'directory'}
            ),
        ),
    ),
    url(
        r'^help/contact/$',
        QuerystringRedirectView.as_view(
            pattern_name='contact-us-interstitial-service-agnostic',
        ),
    ),
]


redirects += (
    article_redirects + tos_redirects +
    privacy_redirects + international_redirects +
    contact_redirects
)
