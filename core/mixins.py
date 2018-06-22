from django.http import Http404
from django.conf import settings
from core.helpers import cms_client, handle_cms_response
from django.utils import translation


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):
        if not self.flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class PerformanceDashboardFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_PERFORMANCE_DASHBOARD_ENABLED


class GetCMSPageMixin:
    def get_context_data(self, *args, **kwargs):
        response = cms_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return super().get_context_data(
            page=handle_cms_response(response),
            *args, **kwargs
        )
