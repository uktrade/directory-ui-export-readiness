from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from casestudy import casestudies
from triage.helpers import TriageAnswersManager
from ui import urls
from article.helpers import ArticleReadManager


class LandingPagelView(TemplateView):
    template_name = 'core/landing-page.html'

    def get_context_data(self, *args, **kwargs):
        answer_manager = TriageAnswersManager(self.request)
        article_manager = ArticleReadManager(request=self.request)
        has_completed_triage = answer_manager.retrieve_answers() != {}
        return super().get_context_data(
            *args, **kwargs,
            has_completed_triage=has_completed_triage,
            casestudies=[
                casestudies.MARKETPLACE,
                casestudies.HELLO_BABY,
                casestudies.YORK,
            ],
            group_read_progress=article_manager.get_group_read_progress(),
        )


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        return [url.name for url in urls.urlpatterns]

    def location(self, item):
        return reverse(item)


class RobotsView(TemplateView):
    template_name = 'core/robots.txt'
    content_type = 'text/plain'
