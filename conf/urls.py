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
import prototype.views
import triage.views

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
        core.views.LandingPageViewNegotiator.as_view(),
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
        r"^new/$",
        article.views.PersonaNewArticleListView.as_view(),
        name='article-list-persona-new',
    ),
    url(
        r"^occasional/$",
        article.views.PersonaOccasionalArticleListView.as_view(),
        name='article-list-persona-occasional',
    ),
    url(
        r"^regular/$",
        article.views.PersonaRegularArticleListView.as_view(),
        name='article-list-persona-regular',
    ),
    url(
        r"^market-research/$",
        article.views.MarketResearchArticleListView.as_view(),
        name='article-list-market-research',
    ),
    url(
        r"^customer-insight/$",
        article.views.CustomerInsightArticleListView.as_view(),
        name='article-list-customer-insight',
    ),
    url(
        r"^finance/$",
        article.views.FinanceArticleListView.as_view(),
        name='article-list-finance',
    ),
    url(
        r"^business-planning/$",
        article.views.BusinessPlanningArticleListView.as_view(),
        name='article-list-business-planning',
    ),
    url(
        r"^getting-paid/$",
        article.views.GettingPaidArticleListView.as_view(),
        name='article-list-getting-paid',
    ),
    url(
        r"^operations-and-compliance/$",
        article.views.OperationsAndComplianceArticleListView.as_view(),
        name='article-list-operations-and-compliance',
    ),
    url(
        r"^market-research/doing-business-with-integrity/$",
        article.views.DoBusinessWithIntegrityView.as_view(),
        name='business-with-integrity',
    ),
    url(
        r"^market-research/do-research-first/$",
        article.views.DoResearchFirstView.as_view(),
        name='article-research-market',
    ),
    url(
        r"^market-research/define-market-potential/$",
        article.views.DefineMarketPotentialView.as_view(),
        name='define-market-potential',
    ),
    url(
        r"^market-research/research-your-market/$",
        article.views.DoFieldResearchView.as_view(),
        name='do-field-research',
    ),
    url(
        r"^market-research/analyse-the-competition/$",
        article.views.AnalyseTheCompetitionView.as_view(),
        name='analyse-the-competition',
    ),
    url(
        r"^market-research/visit-a-trade-show/$",
        article.views.VisitTradeShowView.as_view(),
        name='visit-trade-show',
    ),
    url(
        r"^market-research/know-the-relevant-legislation/$",
        article.views.KnowTheRelevantLegislationView.as_view(),
        name='know-the-relevant-legislation',
    ),
    url(
        r"^customer-insight/know-your-customers/$",
        article.views.KnowYourCustomerView.as_view(),
        name='know-your-customer',
    ),
    url(
        r"^customer-insight/meet-your-customers/$",
        article.views.MeetYourCustomerView.as_view(),
        name='meet-your-customers',
    ),
    url(
        r"^customer-insight/manage-language-differences/$",
        article.views.ManageLanguageDifferencesView.as_view(),
        name='manage-language-differences',
    ),
    url(
        r"^customer-insight/understand-your-customers-culture/$",
        article.views.UnderstandYourCustomersCultureView.as_view(),
        name='understand-your-customers-culture',
    ),
    url(
        r"^finance/get-money-to-export/$",
        article.views.GetMoneyToExportView.as_view(),
        name='get-money-to-export',
    ),
    url(
        r"^finance/choose-the-right-finance/$",
        article.views.ChooseTheRightFinanceView.as_view(),
        name='choose-right-finance',
    ),
    url(
        r"^finance/get-export-finance/$",
        article.views.GetExportFinanceView.as_view(),
        name='get-export-finance',
    ),
    url(
        r"^finance/raise-money-by-borrowing/$",
        article.views.RaiseMoneyByBorrowingView.as_view(),
        name='raise-money-by-borrowing',
    ),
    url(
        r"^finance/borrow-against-assets/$",
        article.views.BorrowAgainstAssetsView.as_view(),
        name='borrow-against-assets',
    ),
    url(
        r"^finance/raise-money-with-investment/$",
        article.views.RaiseMoneyWithInvestmentView.as_view(),
        name='raise-money-with-investment',
    ),
    url(
        r"^finance/get-finance-support-from-government/$",
        article.views.GetGovernmentFinanceSupportView.as_view(),
        name='get-finance-support-from-government',
    ),
    url(
        r"^business-planning/make-an-export-plan/$",
        article.views.MakeExportingPlanView.as_view(),
        name='make-an-export-plan',
    ),
    url(
        r"^business-planning/find-a-route-to-market/$",
        article.views.FindARouteToMarketView.as_view(),
        name='find-a-route-to-market',
    ),
    url(
        r"^business-planning/sell-overseas-directly/$",
        article.views.SellOverseasDirectlyView.as_view(),
        name='sell-overseas-directly',
    ),
    url(
        r"^business-planning/use-an-overseas-agent/$",
        article.views.UseOverseasAgentView.as_view(),
        name='use-an-overseas-agent',
    ),
    url(
        r"^business-planning/use-a-distributor/$",
        article.views.UseDistributorView.as_view(),
        name='use-a-distributor',
    ),
    url(
        r"^business-planning/choosing-an-agent-or-distributor/$",
        article.views.ChoosingAgentOrDistributorView.as_view(),
        name='choosing-an-agent-or-distributor',
    ),
    url(
        r"^business-planning/licensing-and-franchising/$",
        article.views.LicenceAndFranchisingView.as_view(),
        name='licensing-and-franchising',
    ),
    url(
        r"^business-planning/license-your-product-or-service/$",
        article.views.LicenceYourProductOrServiceView.as_view(),
        name='license-your-product-or-service',
    ),
    url(
        r"^business-planning/franchise-your-business/$",
        article.views.FranchiseYourBusinessView.as_view(),
        name='franchise-your-business',
    ),
    url(
        r"^business-planning/start-a-joint-venture/$",
        article.views.StartJointVentureView.as_view(),
        name='start-a-joint-venture',
    ),
    url(
        r"^business-planning/set-up-an-overseas-operation/$",
        article.views.SetupOverseasOperationView.as_view(),
        name='set-up-an-overseas-operation',
    ),
    url(
        r"^getting-paid/consider-how-youll-get-paid/$",
        article.views.ConsiderHowPaidView.as_view(),
        name='consider-how-youll-get-paid',
    ),
    url(
        r"^getting-paid/invoice-currency-and-contents/$",
        article.views.InvoiceCurrencyAndContentsView.as_view(),
        name='invoice-currency-and-contents',
    ),
    url(
        r"^getting-paid/decide-when-youll-get-paid/$",
        article.views.DecideWhenPaidView.as_view(),
        name='decide-when-youll-get-paid',
    ),
    url(
        r"^getting-paid/payment-methods/$",
        article.views.PaymentMethodsView.as_view(),
        name='payment-methods',
    ),
    url(
        r"^getting-paid/insure-against-non-payment/$",
        article.views.InsureAgainstNonPaymentView.as_view(),
        name='insure-against-non-payment',
    ),
    url(
        r"^operations-and-compliance/anti-bribery-and-corruption-training/$",
        article.views.AntiBriberyAndCorruptionTrainingView.as_view(),
        name='anti-bribery-and-corruption-training',
    ),
    url(
        r"^operations-and-compliance/plan-the-logistics/$",
        article.views.PlanTheLogisticsView.as_view(),
        name='plan-the-logistics',
    ),
    url(
        r"^operations-and-compliance/use-a-freight-forwarder/$",
        article.views.UseFreightForwarderView.as_view(),
        name='use-a-freight-forwarder',
    ),
    url(
        r"^operations-and-compliance/use-incoterms-in-contracts/$",
        article.views.UseIncotermsInContractsView.as_view(),
        name='use-incoterms-in-contracts',
    ),
    url(
        r"^operations-and-compliance/get-your-export-documents-right/$",
        article.views.GetYourExportDocumentsRightView.as_view(),
        name='get-your-export-documents-right',
    ),
    url(
        r"^operations-and-compliance/internationalise-your-website/$",
        article.views.InternationaliseWesbiteView.as_view(),
        name='internationalise-your-website',
    ),
    url(
        r"^operations-and-compliance/match-your-website-to-your-audience/$",
        article.views.MatchYourWebsiteToYourAudienceView.as_view(),
        name='match-your-website-to-your-audience',
    ),
    url(
        r"^operations-and-compliance/protect-your-intellectual-property/$",
        article.views.WhatIntellectualPropertyIsView.as_view(),
        name='what-intellectual-property-is',
    ),
    url(
        r"^operations-and-compliance/types-of-intellectual-property/$",
        article.views.TypesOfIntellectualPropertyView.as_view(),
        name='types-of-intellectual-property',
    ),
    url(
        r"^operations-and-compliance/know-what-ip-you-have/$",
        article.views.KnowWhatIntellectualPropertyYouHaveView.as_view(),
        name='know-what-IP-you-have',
    ),
    url(
        r"^operations-and-compliance/international-ip-protection/$",
        article.views.IntellectualPropertyProtectionView.as_view(),
        name='ip-protection-in-multiple-countries',
    ),
    url(
        r"^operations-and-compliance/report-corruption/$",
        article.views.ReportCorruptionView.as_view(),
        name='report-corruption',
    ),
    url(
        r"^new/next-steps/$",
        article.views.NextStepsNewExporterView.as_view(),
        name='next-steps-new-exporter',
    ),
    url(
        r"^occasional/next-steps/$",
        article.views.NextStepsOccasionalExporterView.as_view(),
        name='next-steps-occasional-exporter',
    ),
    url(
        r"^regular/next-steps/$",
        article.views.NextStepsRegularExporterView.as_view(),
        name='next-steps-regular-exporter',
    ),
    url(
        r'^triage/(?P<step>.+)/$',
        triage.views.TriageWizardFormView.as_view(
            url_name='triage-wizard', done_step_name='finished'
        ),
        name='triage-wizard'
    ),
    url(
        r'^triage/$',
        triage.views.TriageStartPageView.as_view(),
        name='triage-start'
    ),
    url(
        r'^custom/$',
        triage.views.CustomPageView.as_view(),
        name='custom-page'
    ),
    url(
        r'^api/internal/companies-house-search/$',
        triage.views.CompaniesHouseSearchApiView.as_view(),
        name='api-internal-companies-house-search'
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
        prototype.views.NewsListPageView.as_view(),
        name='eu-exit-news-list',
    ),
    url(
        r"^eu-exit-news/(?P<slug>[\w-]+)/$",
        prototype.views.NewsArticleDetailView.as_view(),
        name='eu-exit-news-detail',
    ),
    url(
        r"^international/eu-exit-news/$",
        prototype.views.InternationalNewsListPageView.as_view(),
        name='international-eu-exit-news-list',
    ),
    url(
        r"^international/eu-exit-news/(?P<slug>[\w-]+)/$",
        prototype.views.InternationalNewsArticleDetailView.as_view(),
        name='international-eu-exit-news-detail',
    ),
]


prototype_urls = [
    url(
        r"^tagged/(?P<slug>[\w-]+)/$",
        prototype.views.TagListPageView.as_view(),
        name='tag-list',
    ),
    url(
        r"^advice/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'advice'},
        name='advice',
    ),
    url(
        r"^advice/create-an-export-plan/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'create-an-export-plan'},
        name='create-an-export-plan',
    ),
    url(
        r"^advice/create-an-export-plan/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
        name='create-an-export-plan-article',
    ),
    url(
        r"^advice/find-an-export-market/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'find-an-export-market'},
        name='find-an-export-market',
    ),
    url(
        r"^advice/find-an-export-market/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
        name='find-an-export-market-article',
    ),
    url(
        r"^advice/define-route-to-market/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'define-route-to-market'},
        name='define-route-to-market',
    ),
    url(
        r"^advice/define-route-to-market/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
        name='define-route-to-market-article',
    ),
    url(
        r"^advice/get-export-finance-and-funding/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'get-export-finance-and-funding'},
        name='get-export-finance-and-funding',
    ),
    url(
        r"^advice/get-export-finance-and-funding/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
        name='get-export-finance-and-funding-article',
    ),
    url(
        r"^advice/manage-payment-for-export-orders/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'manage-payment-for-export-orders'},
        name='manage-payment-for-export-orders',
    ),
    url(
        r"^advice/manage-payment-for-export-orders/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
        name='manage-payment-for-export-orders-article',
    ),
    url(
        r"^advice/prepare-to-do-business-in-a-foreign-country/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'prepare-to-do-business-in-a-foreign-country'},
        name='prepare-to-do-business-in-a-foreign-country',
    ),
    url(
        r"^advice/prepare-to-do-business-in-a-foreign-country/(?P<slug>[\w-]+)/$",  # noqa
        prototype.views.PrototypePageView.as_view(),
        name='prepare-to-do-business-in-a-foreign-country-article',
    ),
    url(
        r"^advice/manage-legal-and-ethical-compliance/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'manage-legal-and-ethical-compliance'},
        name='manage-legal-and-ethical-compliance',
    ),
    url(
        r"^advice/manage-legal-and-ethical-compliance/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
        name='manage-legal-and-ethical-compliance-article',
    ),
    url(
        r"^advice/prepare-for-export-procedures-and-logistics/$",
        prototype.views.PrototypePageView.as_view(),
        {'slug': 'prepare-for-export-procedures-and-logistics'},
        name='prepare-for-export-procedures-and-logistics',
    ),
    url(
        r"^advice/prepare-for-export-procedures-and-logistics/(?P<slug>[\w-]+)/$",  # noqa
        prototype.views.PrototypePageView.as_view(),
        name='prepare-for-export-procedures-and-logistics-article',
    ),
    url(
        r"^markets/(?P<region>[\w-]+)/(?P<country>[\w-]+)/(?P<slug>[\w-]+)/$",
        prototype.views.PrototypePageView.as_view(),
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
]


urlpatterns += euexit_urls
urlpatterns += redirects
urlpatterns += news_urls
urlpatterns += prototype_urls
urlpatterns += contact_urls
