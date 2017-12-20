from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.utils.cache import set_response_etag
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView

from article.helpers import ArticleReadManager
from article import structure
from casestudy import casestudies
from triage.helpers import TriageAnswersManager
from ui.views import TranslationsMixin


class ArticleReadManagerMixin:

    article_read_manager = None

    def create_article_manager(self, request):
        return ArticleReadManager(request=request)

    def dispatch(self, request, *args, **kwargs):
        self.article_read_manager = self.create_article_manager(request)
        return super().dispatch(request, *args, **kwargs)

    def get_article_group_progress_details(self):
        name = self.article_group.name
        manager = self.article_read_manager
        read_article_uuids = manager.read_articles_keys_in_group(name)
        return {
            'read_article_uuids': read_article_uuids,
            'read_count': len(read_article_uuids),
            'total_articles_count': len(self.article_group.articles),
            'time_left_to_read': manager.remaining_reading_time_in_group(name),
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


class LandingPageView(ArticleReadManagerMixin, TemplateView):
    template_name = 'core/landing-page.html'
    article_group = structure.ALL_ARTICLES

    def get_context_data(self, *args, **kwargs):
        answer_manager = TriageAnswersManager(self.request)
        has_completed_triage = answer_manager.retrieve_answers() != {}
        return super().get_context_data(
            *args, **kwargs,
            has_completed_triage=has_completed_triage,
            casestudies=[
                casestudies.MARKETPLACE,
                casestudies.HELLO_BABY,
                casestudies.YORK,
            ],
            article_group_read_progress=(
                self.article_read_manager.get_group_read_progress()
            ),
        )


class InternationalLandingPageView(
    SetEtagMixin, TranslationsMixin, TemplateView
):
    template_name = 'core/landing_page_international.html'


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
        from django.conf import settings
        context = {
            'exopps_url': settings.SERVICES_EXOPPS_ACTUAL
            }
        return context


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'daily'
    excluded_pattern_names = ['redirect-opportunities-slug']

    def items(self):
        # import here to avoid circular import
        from ui import urls
        return [
            url.name for url in urls.urlpatterns
            if url.name not in self.excluded_pattern_names
        ]

    def location(self, item):
        # triage-wizard needs an additional argument to be reversed
        if item == 'triage-wizard':
            # import here to avoid circular import
            from triage.views import TriageWizardFormView
            return reverse(item, kwargs={'step': TriageWizardFormView.SECTOR})
        return reverse(item)


class RobotsView(TemplateView):
    template_name = 'core/robots.txt'
    content_type = 'text/plain'


class AboutView(SetEtagMixin, TemplateView):
    template_name = 'core/about.html'


class PrivacyCookiesDomestic(SetEtagMixin, TemplateView):
    template_name = 'core/privacy_cookies-domestic.html'


class PrivacyCookiesInternational(SetEtagMixin, TemplateView):
    template_name = 'core/privacy_cookies-international.html'


class TermsConditionsDomestic(SetEtagMixin, TemplateView):
    template_name = 'core/terms_conditions-domestic.html'


class TermsConditionsInternational(SetEtagMixin, TemplateView):
    template_name = 'core/terms_conditions-international.html'
