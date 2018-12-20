from django.conf.urls import url
from django.urls import reverse_lazy
from django.views.generic.base import RedirectView

from core.views import (
    OpportunitiesRedirectView, TranslationRedirectView, QuerystringRedirectView
)

redirects = [
    url(
        r'^bodw2019/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/bodw2019/'),
    ),
    url(
        r'^events/$',
        QuerystringRedirectView.as_view(
            url='https://www.events.great.gov.uk/'),
    ),
    url(
        r'^expo2020/$',
        RedirectView.as_view(
            url='https://www.events.trade.gov.uk/dubai-expo-2020/'),
    ),
    url(
        r'^ukpavilion2020/$',
        RedirectView.as_view(
            url='https://www.events.trade.gov.uk/dubai-expo-2020/'
        ),
    ),
    url(
        r'^exporting-edge/$',
        RedirectView.as_view(pattern_name='get-finance'),
    ),
    url(
        r'^invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk'),
    ),
    url(
        r'^int/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/int'),
    ),
    url(
        r'^us/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/us'),
    ),
    url(
        r'^es/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/es'),
    ),
    url(
        r'^int/es/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/es',
        ),
    ),
    url(
        r'^cn/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/cn'),
    ),
    url(
        r'^int/zh/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/zh',
        ),
    ),
    url(
        r'^int/pt/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/pt',
        ),
    ),
    url(
        r'^br/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/br'),
    ),
    url(
        r'^de/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/de'),
    ),
    url(
        r'^int/de/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/de',
        ),
    ),
    url(
        r'^jp/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/jp'),
    ),
    url(
        r'^int/ja/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/ja',
        ),
    ),
    url(
        r'^in/invest/$',
        QuerystringRedirectView.as_view(url='https://invest.great.gov.uk/in'),
    ),
    url(
        r'^int/ar/invest/$',
        QuerystringRedirectView.as_view(
            url='https://invest.great.gov.uk/int/ar',
        ),
    ),
    url(
        r'^study/$',
        QuerystringRedirectView.as_view(
            url='https://study-uk.britishcouncil.org',
        ),
    ),
    url(
        r'^visit/$',
        QuerystringRedirectView.as_view(
            url='https://www.visitbritain.com/gb/en',
        ),
    ),
    url(
        r'^export/$',
        QuerystringRedirectView.as_view(pattern_name='landing-page'),
    ),
    url(
        r'^export/new/$',
        QuerystringRedirectView.as_view(
            pattern_name='article-list-persona-new',
        ),
    ),
    url(
        r'^export/occasional/$',
        QuerystringRedirectView.as_view(
            pattern_name='article-list-persona-occasional',
        ),
    ),
    url(
        r'^export/regular/$',
        QuerystringRedirectView.as_view(
            pattern_name='article-list-persona-regular',
        ),
    ),
    url(
        r'^export/opportunities/$',
        QuerystringRedirectView.as_view(
            url='https://opportunities.export.great.gov.uk/',
        ),
    ),
    url(
        r'^opportunities/$',
        QuerystringRedirectView.as_view(
            url='https://opportunities.export.great.gov.uk/',
        ),
    ),
    url(
        r'^opportunities/(?P<slug>[-\w]+)/$',
        # Redirects to https://opportunities.export.great.gov.uk/opportunities
        # with the slug and query parameters
        OpportunitiesRedirectView.as_view(),
    ),
    url(
        r'^export/find-a-buyer/$',
        QuerystringRedirectView.as_view(
            url='https://find-a-buyer.export.great.gov.uk',
        ),
    ),
    url(
        r'^export/selling-online-overseas/$',
        QuerystringRedirectView.as_view(
            url='https://selling-online-overseas.export.great.gov.uk',
        ),
    ),
    url(
        r'^trade/$',
        QuerystringRedirectView.as_view(url='https://trade.great.gov.uk'),
    ),
    url(
        r'^uk/privacy-policy/$',
        QuerystringRedirectView.as_view(pattern_name='privacy-and-cookies'),
    ),
    url(
        r'^uk/terms-and-conditions/$',
        QuerystringRedirectView.as_view(pattern_name='terms-and-conditions'),
    ),
    url(
        r'^uk/$',
        TranslationRedirectView.as_view(pattern_name='landing-page'),
    ),
    url(
        r'^int/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
    ),
    url(
        r'^in/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
    ),
    url(
        r'^us/$',
        TranslationRedirectView.as_view(
            pattern_name='landing-page-international',
        ),
    ),
    url(
        r'^innovation/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/'
                'the-great-festival-of-innovation-hong-kong-2018/'
            ),
        ),
    ),
    url(
        r'^uk/cy/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.great.gov.uk/?utm_source=Mailing&utm_medium'
                '=Brochure&utm_campaign=ExportBrochureCY'
            ),
        ),
    ),
    url(
        r'^verify/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://find-a-buyer.export.great.gov.uk/'
                'verify/letter-confirm/'
            ),
        ),
    ),
    url(
        r'^legal/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://trade.great.gov.uk/'
                'campaign/legal-is-great/singapore/'
            ),
        ),
    ),
    url(
        r'^kr/$',
        QuerystringRedirectView.as_view(
            url=(
                'https://www.events.trade.gov.uk/invest-in-great---korea'
                '?utm_source=print&utm_campaign=korean_winter_olympics_invest'
            )
        ),
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
    ) for redirect in ARTICLE_REDIRECTS_MAPPING
]

contact_redirects = [
    url(
        r'^legacy/contact/(?P<service>[-\w\d]+)/FeedbackForm/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/feedback/(?P<service>[-\w\d]+)/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/feedback/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/(?P<service>[-\w\d]+)/feedback/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy('contact-us-feedback')
        ),
    ),
    url(
        r'^legacy/contact/single_sign_on/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'great-account'}
            )
        ),
    ),
    url(
        r'^legacy/contact/selling_online_overseas/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'domestic'}
            )
        ),
    ),
    url(
        r'^legacy/contact/export_ops/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'domestic'}
            )
        ),
    ),
    url(
        r'^legacy/contact/export_opportunities/$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'domestic'}
            )
        ),
    ),
    url(
        r'^legacy/contact/cookies/$',
        QuerystringRedirectView.as_view(pattern_name='privacy-and-cookies'),
    ),
    url(
        r'^legacy/contact/terms-and-conditions/$',
        QuerystringRedirectView.as_view(pattern_name='terms-and-conditions'),
    ),
    # catch everything not covered above but not interfere with trailing slash
    # redirects
    url(
        r'^legacy/contact/(.*/)?$',
        QuerystringRedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'location'}
            )
        ),
    ),
]


redirects += (
        article_redirects + tos_redirects + contact_redirects +
        privacy_redirects + international_redirects
)
