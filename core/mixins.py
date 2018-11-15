from directory_cms_client.client import cms_api_client
from directory_constants.constants import cms
from django.http import Http404
from django.conf import settings
from directory_cms_client.helpers import (
    handle_cms_response, handle_cms_response_allow_404)
from core.helpers import cms_component_is_bidi
from django.utils import translation
from django.utils.functional import cached_property


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):
        if not self.flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class NewsSectionFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['NEWS_SECTION_ON']


class PrototypeFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON']


class PerformanceDashboardFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['PERFORMANCE_DASHBOARD_ON']


class GetCMSPageMixin:
    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(page=self.page, *args, **kwargs)


class GetCMSComponentMixin:
    @cached_property
    def cms_component(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.component_slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
            service_name=cms.COMPONENTS,
        )
        return handle_cms_response_allow_404(response)

    @property
    def component_is_bidi(self):
        if self.cms_component:
            return cms_component_is_bidi(
                translation.get_language(),
                self.cms_component['meta']['languages']
            )
        return False

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            component_is_bidi=self.component_is_bidi,
            cms_component=self.cms_component,
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
