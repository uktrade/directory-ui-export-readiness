from invest.helpers import cms_api_client
from directory_cms_client.constants import (
    EXPORT_READINESS_HIGH_POTENTIAL_OPPORTUNITY_FORM_SLUG
)

from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.utils.functional import cached_property

from core.helpers import handle_cms_response
from invest import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class HighPotentialOpportunityDetailView(FeatureFlagMixin, TemplateView):
    template_name = 'invest/high-potential-opportunity-detail.html'

    def get_context_data(self, **kwargs):
        response = cms_api_client.lookup_by_slug(
            slug=self.kwargs.get('slug'),
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        page = handle_cms_response(response)
        return super().get_context_data(page=page, **kwargs)


class HighPotentialOpportunityFormView(FeatureFlagMixin, FormView):
    template_name = 'invest/high-potential-opportunities-form.html'
    form_class = forms.HighPotentialOpportunityForm

    #  TODO TT-364: 404 if the opportunity_slug is invalid
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        return kwargs

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=EXPORT_READINESS_HIGH_POTENTIAL_OPPORTUNITY_FORM_SLUG,
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, **kwargs):
        return super().get_context_data(page=self.page, **kwargs)

    def form_valid(self, form):
        # TODO T-336: link to thank you page
        # TODO TT-337: send email confirmation via govnotify and forms api
        return super().form_valid()
