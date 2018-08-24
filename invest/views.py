from directory_cms_client.client import cms_api_client
from directory_cms_client.constants import (
    EXPORT_READINESS_HIGH_POTENTIAL_OPPORTUNITY_FORM_SLUG
)
from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView

from core.helpers import handle_cms_response
from invest import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['HIGH_POTENTIAL_OPPORTUNITIES_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class HighPotentialOpportunityFormView(FeatureFlagMixin, FormView):
    template_name = 'invest/high-potential-opportunities-form.html'
    form_class = forms.HighPotentialOpportunityForm

    #  TODO TT-364: 404 if the opportunity_slug is invalid
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.get_form_content()
        return kwargs

    def get_form_content(self):
        response = cms_api_client.lookup_by_slug(
            slug=EXPORT_READINESS_HIGH_POTENTIAL_OPPORTUNITY_FORM_SLUG,
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def form_valid(self, form):
        # TODO T-336: link to thank you page
        # TODO TT-337: send email confirmation via govnotify and forms api
        return super().form_valid()
