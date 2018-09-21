from directory_cms_client.client import cms_api_client
from django.http import Http404
from django.conf import settings
from core.helpers import handle_cms_response
from django.utils import translation


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):
        if not self.flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class PerformanceDashboardFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['PERFORMANCE_DASHBOARD_ON']


class GetCMSPageMixin:
    def get_context_data(self, *args, **kwargs):
        if hasattr(self, 'slug'):
            slug = self.slug
        else:
            slug = self.kwargs['slug']
        response = cms_api_client.lookup_by_slug(
            slug=slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return super().get_context_data(
            page=handle_cms_response(response),
            *args, **kwargs
        )


class TranslationsMixin:

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        context['directory_components_html_lang_attribute']\
            = translation.get_language()
        return context
