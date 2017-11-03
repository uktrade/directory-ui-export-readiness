from django.contrib import sitemaps
from django.core.urlresolvers import reverse
from django.views.generic import TemplateView

from casestudy import casestudies
from triage.helpers import TriageAnswersManager


class ArticleReadMixin:
    def get_article_group_progress_details(self):
        key = self.article_group.key
        manager = self.request.article_read_manager
        read_article_uuids = manager.read_articles_keys_in_group(key)
        return {
            'read_article_uuids': read_article_uuids,
            'read_count': len(read_article_uuids),
            'total_articles_count': len(self.article_group.articles),
            'time_left_to_read': manager.remaining_reading_time_in_group(key),
        }

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs,
            article_group_progress=self.get_article_group_progress_details(),
        )


class LandingPagelView(TemplateView):
    template_name = 'core/landing-page.html'

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
                self.request.article_read_manager.get_group_read_progress()
            ),
        )


class StaticViewSitemap(sitemaps.Sitemap):
    changefreq = 'daily'

    def items(self):
        # import here to avoid circular import
        from ui import urls
        return [url.name for url in urls.urlpatterns]

    def location(self, item):
        return reverse(item)


class RobotsView(TemplateView):
    template_name = 'core/robots.txt'
    content_type = 'text/plain'
