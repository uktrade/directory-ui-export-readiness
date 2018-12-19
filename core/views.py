from directory_constants.constants import cms, urls
from directory_cms_client.client import cms_api_client

from django.conf import settings
from django.contrib import sitemaps
from django.urls import reverse, RegexURLResolver
from django.utils.cache import set_response_etag
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.utils.functional import cached_property

from article.helpers import ArticlesViewedManagerFactory
from article import structure
from casestudy import casestudies
from core import helpers, mixins
from triage.helpers import TriageAnswersManager
from euexit.mixins import (
    HideLanguageSelectorMixin, EUExitFormsFeatureFlagMixin)


class ArticlesViewedManagerMixin:

    article_read_manager = None

    def create_article_manager(self, request):
        return ArticlesViewedManagerFactory(request=request)

    def dispatch(self, request, *args, **kwargs):
        self.article_read_manager = self.create_article_manager(request)
        return super().dispatch(request, *args, **kwargs)

    def get_article_group_progress_details(self):
        name = self.article_group.name
        manager = self.article_read_manager
        viewed_article_uuids = manager.articles_viewed_for_group(name)
        return {
            'viewed_article_uuids': viewed_article_uuids,
            'read_count': len(viewed_article_uuids),
            'total_articles_count': len(self.article_group.articles),
            'time_left_to_read': manager.remaining_read_time_for_group(name),
        }

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs,
            article_group_progress=self.get_article_group_progress_details(),
        )


class SetEtagMixin:
    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        if request.method == 'GET':
            response.add_post_render_callback(set_response_etag)
        return response


class LandingPageViewNegotiator(TemplateView):
    def __new__(cls, *args, **kwargs):
        if settings.FEATURE_FLAGS['NEWS_SECTION_ON']:
            return NewsSectionLandingPageView(*args, **kwargs)
        elif settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON']:
            return LandingPageView(*args, **kwargs)
        return PrototypeLandingPageView(*args, **kwargs)


class LandingPageView(ArticlesViewedManagerMixin, TemplateView):
    template_name = 'core/landing-page.html'
    article_group = structure.ALL_ARTICLES

    def get_context_data(self, *args, **kwargs):
        answer_manager = TriageAnswersManager(self.request)
        has_completed_triage = answer_manager.retrieve_answers() != {}
        return super().get_context_data(
            *args, **kwargs,
            LANDING_PAGE_VIDEO_URL=settings.LANDING_PAGE_VIDEO_URL,
            has_completed_triage=has_completed_triage,
            casestudies=[
                casestudies.MARKETPLACE,
                casestudies.HELLO_BABY,
                casestudies.YORK,
            ],
            article_group_read_progress=(
                self.article_read_manager.get_view_progress_for_groups()
            ),
        )

    def get(self, request, *args, **kwargs):
        redirector = helpers.GeoLocationRedirector(self.request)
        if redirector.should_redirect:
            return redirector.get_response()
        return super().get(request, *args, **kwargs)


class NewsSectionLandingPageView(LandingPageView):
    template_name = 'prototype/landing_page.html'

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=cms.EXPORT_READINESS_HOME_SLUG,
            draft_token=self.request.GET.get('draft_token'),
        )
        return helpers.handle_cms_response_allow_404(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            page=self.page,
            *args, **kwargs
        )


class PrototypeLandingPageView(
    mixins.PrototypeFeatureFlagMixin,
    NewsSectionLandingPageView,
):
    pass


class CampaignPageView(
    mixins.CampaignPagesFeatureFlagMixin,
    mixins.GetCMSPageMixin,
    TemplateView
):
    template_name = 'core/campaign.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class InternationalLandingPageView(
    mixins.TranslationsMixin,
    mixins.GetCMSPageMixin,
    mixins.GetCMSComponentMixin,
    TemplateView,
):
    template_name = 'core/landing_page_international.html'
    component_slug = cms.COMPONENTS_BANNER_INTERNATIONAL_SLUG
    slug = cms.EXPORT_READINESS_HOME_INTERNATIONAL_SLUG


class InternationalContactPageView(
    EUExitFormsFeatureFlagMixin,
    HideLanguageSelectorMixin,
    TemplateView,
):
    template_name = 'core/contact_page_international.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            invest_contact_us_url=urls.build_invest_url('contact/'),
            *args, **kwargs
        )


class QuerystringRedirectView(RedirectView):
    query_string = True


class TranslationRedirectView(RedirectView):
    language = None
    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        """
        Return the URL redirect
        """
        url = super().get_redirect_url(*args, **kwargs)

        if self.language:
            # Append 'lang' to query params
            if self.request.META.get('QUERY_STRING'):
                concatenation_character = '&'
            # Add 'lang' query param
            else:
                concatenation_character = '?'

            url = '{}{}lang={}'.format(
                url, concatenation_character, self.language
            )

        return url


class OpportunitiesRedirectView(RedirectView):
    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        redirect_url = '{export_opportunities_url}{slug}/'.format(
            export_opportunities_url=(
                'https://opportunities.export.great.gov.uk/opportunities/'
            ),
            slug=kwargs.get('slug', '')
        )

        query_string = self.request.META.get('QUERY_STRING')
        if query_string:
            redirect_url = "{redirect_url}?{query_string}".format(
                redirect_url=redirect_url, query_string=query_string
            )

        return redirect_url


class InterstitialPageExoppsView(SetEtagMixin, TemplateView):
    template_name = 'core/interstitial_exopps.html'

    def get_context_data(self, **kwargs):
        context = {
            'exopps_url': settings.SERVICES_EXOPPS_ACTUAL
            }
        return context


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        # import here to avoid circular import
        from conf import urls
        from conf.url_redirects import redirects

        dynamic_cms_page_url_names = [
            'privacy-and-cookies-subpage',
            'contact-us-export-opportunities-guidance',
            'contact-us-great-account-guidance',
            'contact-us-export-advice',
            'contact-us-soo',
            'campaign-page',
            'contact-us-routing-form',
            'office-finder-contact',
            'contact-us-office-success',
        ]

        dynamic_cms_page_url_names += [url.name for url in urls.prototype_urls]
        dynamic_cms_page_url_names += [url.name for url in urls.news_urls]

        return [
            item.name for item in urls.urlpatterns
            if not isinstance(item, RegexURLResolver) and
            item not in redirects and
            item.name not in dynamic_cms_page_url_names
        ]

    def location(self, item):
        if item == 'triage-wizard':
            # import here to avoid circular import
            from triage.views import TriageWizardFormView
            return reverse(item, kwargs={
                'step': TriageWizardFormView.EXPORTED_BEFORE})
        if item == 'uk-export-finance-lead-generation-form':
            return reverse(item, kwargs={'step': 'contact'})
        return reverse(item)


class AboutView(SetEtagMixin, TemplateView):
    template_name = 'core/about.html'


class PrivacyCookiesDomesticCMS(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'core/info_page.html'
    slug = cms.EXPORT_READINESS_PRIVACY_AND_COOKIES_SLUG


class PrivacyCookiesDomesticSubpageCMS(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'core/privacy_subpage.html'

    @property
    def slug(self):
        return self.kwargs['slug']


class PrivacyCookiesInternationalCMS(PrivacyCookiesDomesticCMS):
    template_name = 'core/info_page_international.html'


class TermsConditionsDomesticCMS(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'core/info_page.html'
    slug = cms.EXPORT_READINESS_TERMS_AND_CONDITIONS_SLUG


class TermsConditionsInternationalCMS(TermsConditionsDomesticCMS):
    template_name = 'core/info_page_international.html'


class PerformanceDashboardView(
    mixins.PerformanceDashboardFeatureFlagMixin,
    mixins.GetCMSPageMixin,
    TemplateView
):
    template_name = 'core/performance_dashboard.html'


class PerformanceDashboardGreatView(PerformanceDashboardView):
    slug = cms.EXPORT_READINESS_PERFORMANCE_DASHBOARD_SLUG


class PerformanceDashboardExportOpportunitiesView(PerformanceDashboardView):
    slug = cms.EXPORT_READINESS_PERFORMANCE_DASHBOARD_EXOPPS_SLUG


class PerformanceDashboardSellingOnlineOverseasView(PerformanceDashboardView):
    slug = cms.EXPORT_READINESS_PERFORMANCE_DASHBOARD_SOO_SLUG


class PerformanceDashboardTradeProfilesView(PerformanceDashboardView):
    slug = cms.EXPORT_READINESS_PERFORMANCE_DASHBOARD_TRADE_PROFILE_SLUG


class PerformanceDashboardInvestView(PerformanceDashboardView):
    slug = cms.EXPORT_READINESS_PERFORMANCE_DASHBOARD_INVEST_SLUG


class PerformanceDashboardNotesView(PerformanceDashboardView):
    slug = cms.EXPORT_READINESS_PERFORMANCE_DASHBOARD_NOTES_SLUG
    template_name = 'core/performance_dashboard_notes.html'
