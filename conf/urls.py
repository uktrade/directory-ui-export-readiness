import directory_components.views
import directory_healthcheck.views

from django.conf.urls import include, url
from django.contrib.sitemaps.views import sitemap
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

import article.views
import casestudy.views
import contact.views
import core.views
import euexit.views
import finance.views
import marketaccess.views

from conf.url_redirects import redirects


sitemaps = {
    'static': core.views.StaticViewSitemap,
}


healthcheck_urls = [
    url(
        r'^$',
        directory_healthcheck.views.HealthcheckView.as_view(),
        name='healthcheck'
    ),
    url(
        r'^ping/$',
        directory_healthcheck.views.PingView.as_view(),
        name='ping'
    ),
]


urlpatterns = [
    url(
        r'^healthcheck/',
        include(
            healthcheck_urls, namespace='healthcheck', app_name='healthcheck'
        )
    ),
    url(
        r"^sitemap\.xml$", sitemap, {'sitemaps': sitemaps},
        name='sitemap'
    ),
    url(
        r"^robots\.txt$",
        directory_components.views.RobotsView.as_view(),
        name='robots'
    ),
    url(
        r"^$",
        core.views.LandingPageView.as_view(),
        name='landing-page',
    ),
    url(
        r"^international/$",
        core.views.InternationalLandingPageView.as_view(),
        name='landing-page-international'
    ),
    url(
        r"^international/contact/$",
        core.views.InternationalContactPageView.as_view(),
        name='contact-page-international'
    ),
    url(
        r"^not-found/$",
        TemplateView.as_view(template_name='404.html'),
        name='not-found'
    ),
    url(
        r"^campaigns/(?P<slug>[\w-]+)/$",
        core.views.CampaignPageView.as_view(),
        name='campaign-page',
    ),
    url(
        r"^performance-dashboard/$",
        core.views.PerformanceDashboardGreatView.as_view(),
        name='performance-dashboard'
    ),
    url(
        r"^performance-dashboard/export-opportunities/$",
        core.views.PerformanceDashboardExportOpportunitiesView.as_view(),
        name='performance-dashboard-export-opportunities'
    ),
    url(
        r"^performance-dashboard/selling-online-overseas/$",
        core.views.PerformanceDashboardSellingOnlineOverseasView.as_view(),
        name='performance-dashboard-selling-online-overseas'
    ),
    url(
        r"^performance-dashboard/trade-profiles/$",
        core.views.PerformanceDashboardTradeProfilesView.as_view(),
        name='performance-dashboard-trade-profiles'
    ),
    url(
        r"^performance-dashboard/invest/$",
        core.views.PerformanceDashboardInvestView.as_view(),
        name='performance-dashboard-invest'
    ),
    url(
        r"^performance-dashboard/guidance-notes/$",
        core.views.PerformanceDashboardNotesView.as_view(),
        name='performance-dashboard-notes'
    ),
    url(
        r"^about/$",
        core.views.AboutView.as_view(),
        name='about'
    ),
    url(
        r"^privacy-and-cookies/$",
        core.views.PrivacyCookiesDomesticCMS.as_view(),
        name='privacy-and-cookies'
    ),
    url(
        r"^privacy-and-cookies/(?P<slug>[-\w\d]+)/$",
        core.views.PrivacyCookiesDomesticSubpageCMS.as_view(),
        name='privacy-and-cookies-subpage'
    ),
    url(
        r"^terms-and-conditions/$",
        core.views.TermsConditionsDomesticCMS.as_view(),
        name='terms-and-conditions'
    ),
    url(
        r"^international/privacy-and-cookies/$",
        core.views.PrivacyCookiesInternationalCMS.as_view(),
        name='privacy-and-cookies-international'
    ),
    url(
        r"^international/terms-and-conditions/$",
        core.views.TermsConditionsInternationalCMS.as_view(),
        name='terms-and-conditions-international'
    ),
    url(
        r"^export-opportunities/$",
        core.views.InterstitialPageExoppsView.as_view(),
        name='export-opportunities',
    ),
    url(
        r'^story/hello-babys-rapid-online-growth/$',
        casestudy.views.CasestudyHelloBabyView.as_view(),
        name='casestudy-hello-baby'
    ),
    url(
        r'^story/online-marketplaces-propel-freestyle-xtreme-sales/$',
        casestudy.views.CasestudyMarketplaceView.as_view(),
        name='casestudy-online-marketplaces'
    ),
    url(
        r'^story/york-bag-retailer-goes-global-via-e-commerce/$',
        casestudy.views.CasestudyYorkBagView.as_view(),
        name='casestudy-york-bag'
    ),
    url(
        r"^get-finance/$",
        finance.views.GetFinanceView.as_view(),
        name='get-finance'
    ),
    url(
        r'^get-finance/contact/thanks/$',
        finance.views.GetFinanceLeadGenerationSuccessView.as_view(),
        name='uk-export-finance-lead-generation-form-success'
    ),
    url(
        r'^get-finance/(?P<step>.+)/$',
        finance.views.GetFinanceLeadGenerationFormView.as_view(
            url_name='uk-export-finance-lead-generation-form',
            done_step_name='finished'
        ),
        name='uk-export-finance-lead-generation-form'
    ),
    url(
        r'^triage/(?P<step>.+)/$',
        core.views.ServiceNoLongerAvailableView.as_view(),
        name='triage-wizard'
    ),
    url(
        r'^triage/$',
        core.views.ServiceNoLongerAvailableView.as_view(),
        name='triage-start'
    ),
    url(
        r'^custom/$',
        core.views.ServiceNoLongerAvailableView.as_view(),
        name='custom-page'
    )

]


euexit_urls = [
    url(
        r'^international/eu-exit-news/contact/$',
        euexit.views.InternationalContactFormView.as_view(),
        name='eu-exit-international-contact-form'
    ),
    url(
        r'^international/eu-exit-news/contact/success/$',
        euexit.views.InternationalContactSuccessView.as_view(),
        name='eu-exit-international-contact-form-success'
    ),
    url(
        r'^eu-exit-news/contact/$',
        euexit.views.DomesticContactFormView.as_view(),
        name='eu-exit-domestic-contact-form'
    ),
    url(
        r'^eu-exit-news/contact/success/$',
        euexit.views.DomesticContactSuccessView.as_view(),
        name='eu-exit-domestic-contact-form-success'
    ),
]


news_urls = [
    url(
        r"^eu-exit-news/$",
        article.views.NewsListPageView.as_view(),
        name='eu-exit-news-list',
    ),
    url(
        r"^eu-exit-news/(?P<slug>[\w-]+)/$",
        article.views.NewsArticleDetailView.as_view(),
        name='eu-exit-news-detail',
    ),
    url(
        r"^international/eu-exit-news/$",
        article.views.InternationalNewsListPageView.as_view(),
        name='international-eu-exit-news-list',
    ),
    url(
        r"^international/eu-exit-news/(?P<slug>[\w-]+)/$",
        article.views.InternationalNewsArticleDetailView.as_view(),
        name='international-eu-exit-news-detail',
    ),
]


article_urls = [
    url(
        r"^tagged/(?P<slug>[\w-]+)/$",
        article.views.TagListPageView.as_view(),
        name='tag-list',
    ),
    url(
        r"^advice/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'advice'},
        name='advice',
    ),
    url(
        r"^advice/create-an-export-plan/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'create-an-export-plan'},
        name='create-an-export-plan',
    ),
    url(
        r"^advice/create-an-export-plan/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='create-an-export-plan-article',
    ),
    url(
        r"^advice/find-an-export-market/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'find-an-export-market'},
        name='find-an-export-market',
    ),
    url(
        r"^advice/find-an-export-market/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='find-an-export-market-article',
    ),
    url(
        r"^advice/define-route-to-market/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'define-route-to-market'},
        name='define-route-to-market',
    ),
    url(
        r"^advice/define-route-to-market/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='define-route-to-market-article',
    ),
    url(
        r"^advice/get-export-finance-and-funding/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'get-export-finance-and-funding'},
        name='get-export-finance-and-funding',
    ),
    url(
        r"^advice/get-export-finance-and-funding/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='get-export-finance-and-funding-article',
    ),
    url(
        r"^advice/manage-payment-for-export-orders/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'manage-payment-for-export-orders'},
        name='manage-payment-for-export-orders',
    ),
    url(
        r"^advice/manage-payment-for-export-orders/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='manage-payment-for-export-orders-article',
    ),
    url(
        r"^advice/prepare-to-do-business-in-a-foreign-country/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'prepare-to-do-business-in-a-foreign-country'},
        name='prepare-to-do-business-in-a-foreign-country',
    ),
    url(
        r"^advice/prepare-to-do-business-in-a-foreign-country/(?P<slug>[\w-]+)/$",  # noqa
        article.views.CMSPageView.as_view(),
        name='prepare-to-do-business-in-a-foreign-country-article',
    ),
    url(
        r"^advice/manage-legal-and-ethical-compliance/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'manage-legal-and-ethical-compliance'},
        name='manage-legal-and-ethical-compliance',
    ),
    url(
        r"^advice/manage-legal-and-ethical-compliance/(?P<slug>[\w-]+)/$",
        article.views.CMSPageView.as_view(),
        name='manage-legal-and-ethical-compliance-article',
    ),
    url(
        r"^advice/prepare-for-export-procedures-and-logistics/$",
        article.views.CMSPageView.as_view(),
        {'slug': 'prepare-for-export-procedures-and-logistics'},
        name='prepare-for-export-procedures-and-logistics',
    ),
    url(
        r"^advice/prepare-for-export-procedures-and-logistics/(?P<slug>[\w-]+)/$",  # noqa
        article.views.CMSPageView.as_view(),
        name='prepare-for-export-procedures-and-logistics-article',
    ),
    url(
        r"^markets/$",
        article.views.MarketsPageView.as_view(),
        {'slug': 'markets'},
        name='markets',
    ),
    url(
        r"^markets/(?P<slug>[\w-]+)/$",
        article.views.MarketsPageView.as_view(),
        name='superregion',
    ),
    url(
        r"^markets/(?P<region>[\w-]+)/(?P<slug>[\w-]+)/$",
        article.views.MarketsPageView.as_view(),
        name='country-guide',
    ),
    url(
        r"^markets/(?P<region>[\w-]+)/(?P<country>[\w-]+)/(?P<slug>[\w-]+)/$",
        article.views.MarketsPageView.as_view(),
        name='country-guide-article',
    ),
]

contact_urls = [
    url(
        r'^contact/triage/export-opportunities/(?P<slug>[-\w\d]+)/$',
        contact.views.GuidanceView.as_view(),
        name='contact-us-export-opportunities-guidance'
    ),
    url(
        r'^contact/triage/great-account/(?P<slug>[-\w\d]+)/$',
        contact.views.GuidanceView.as_view(),
        name='contact-us-great-account-guidance'
    ),
    url(
        r'^contact/events/$',
        contact.views.EventsFormView.as_view(),
        name='contact-us-events-form'
    ),
    url(
        r'^contact/events/success/$',
        contact.views.EventsSuccessView.as_view(),
        name='contact-us-events-success'
    ),
    url(
        r'^contact/defence-and-security-organisation/$',
        contact.views.DefenceAndSecurityOrganisationFormView.as_view(),
        name='contact-us-dso-form'
    ),
    url(
        r'^contact/defence-and-security-organisation/success/$',
        contact.views.DefenceAndSecurityOrganisationSuccessView.as_view(),
        name='contact-us-dso-success'
    ),
    url(
        r'^contact/export-advice/success/$',
        contact.views.ExportingAdviceSuccessView.as_view(),
        name='contact-us-export-advice-success'
    ),
    url(
        r'^contact/export-advice/$',
        RedirectView.as_view(
            url=reverse_lazy(
                'contact-us-export-advice', kwargs={'step': 'comment'}
            )
        ),
        name='export-advice-routing-form'
    ),
    url(
        r'^contact/export-advice/(?P<step>.+)/$',
        contact.views.ExportingAdviceFormView.as_view(
            url_name='contact-us-export-advice', done_step_name='finished'
        ),
        name='contact-us-export-advice'
    ),
    url(
        r'^contact/feedback/$',
        contact.views.FeedbackFormView.as_view(),
        name='contact-us-feedback'
    ),
    url(
        r'^contact/feedback/success/$',
        contact.views.FeedbackSuccessView.as_view(),
        name='contact-us-feedback-success'
    ),
    url(
        r'^contact/domestic/$',
        contact.views.DomesticFormView.as_view(),
        name='contact-us-domestic'
    ),
    url(
        r'^contact/domestic/enquiries/$',
        contact.views.DomesticEnquiriesFormView.as_view(),
        name='contact-us-enquiries'
    ),
    url(
        r'^contact/domestic/success/$',
        contact.views.DomesticSuccessView.as_view(),
        name='contact-us-domestic-success'
    ),
    url(
        r'^contact/international/$',
        contact.views.InternationalFormView.as_view(),
        name='contact-us-international'
    ),
    url(
        r'^contact/international/success/$',
        contact.views.InternationalSuccessView.as_view(),
        name='contact-us-international-success'
    ),
    url(
        r'^contact/selling-online-overseas/$',
        RedirectView.as_view(
            url=reverse_lazy(
                'contact-us-soo', kwargs={'step': 'organisation'}
            )
        ),
        name='contact-us-soo-redirect'
    ),
    url(
        r'^contact/selling-online-overseas/success/$',
        contact.views.SellingOnlineOverseasSuccessView.as_view(),
        name='contact-us-selling-online-overseas-success'
    ),
    url(
        r'^contact/selling-online-overseas/(?P<step>.+)/$',
        contact.views.SellingOnlineOverseasFormView.as_view(
            url_name='contact-us-soo', done_step_name='finished'
        ),
        name='contact-us-soo'
    ),
    url(
        r'^contact/$',
        RedirectView.as_view(
            url=reverse_lazy(
                'contact-us-routing-form', kwargs={'step': 'location'}
            )
        ),
        name='contact-us-routing-form-redirect'
    ),
    url(
        r'^contact/triage/(?P<step>.+)/$',
        contact.views.RoutingFormView.as_view(
            url_name='contact-us-routing-form', done_step_name='finished'
        ),
        name='contact-us-routing-form'
    ),
    url(
        r'^contact/office-finder/$',
        contact.views.OfficeFinderFormView.as_view(),
        name='office-finder'
    ),
    url(
        r'^contact/office-finder/(?P<postcode>[\w\d]+)/$',
        contact.views.OfficeContactFormView.as_view(),
        name='office-finder-contact'
    ),
    url(
        r'^contact/office-finder/(?P<postcode>[\w\d]+)/success/$',
        contact.views.OfficeSuccessView.as_view(),
        name='contact-us-office-success'
    ),
    url(
        r'^api/internal/companies-house-search/$',
        core.views.CompaniesHouseSearchApiView.as_view(),
        name='api-internal-companies-house-search'
    ),
]

marketaccess_urls = [
    url(
        r'^market-access/$',
        marketaccess.views.MarketAccessView.as_view(),
        name='market-access'
    ),
    url(
        r'^market-access/report-barrier/emergency-details/$',
        marketaccess.views.ReportBarrierEmergencyView.as_view(),
        name='market-access-emergency'
    ),
    url(
        r'^market-access/report-barrier/success/$',
        marketaccess.views.ReportMarketAccessBarrierSuccessView.as_view(),
        name='report-barrier-form-success'
    ),
    url(
        r'^market-access/report-barrier/(?P<step>.+)/$',
        marketaccess.views.ReportMarketAccessBarrierFormView.as_view(
            url_name='report-ma-barrier',
            done_step_name='finished',
        ),
        name='report-ma-barrier'
    ),

]

urlpatterns += euexit_urls
urlpatterns += redirects
urlpatterns += news_urls
urlpatterns += article_urls
urlpatterns += contact_urls
urlpatterns += marketaccess_urls
