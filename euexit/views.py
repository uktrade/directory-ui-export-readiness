from directory_cms_client.client import cms_api_client

from django.conf import settings
from django.http import Http404
from django.utils.functional import cached_property
from django.views.generic.edit import FormView

from core.helpers import handle_cms_response
from euexit import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class InternationalContactFormView(FeatureFlagMixin, FormView):
    form_class = forms.InternationalContactForm
    template_name = 'euexit/international-contact-form.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        return kwargs

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug='eu-exit-international',
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        if response.status_code == 404:
            raise Http404()
        return handle_cms_response(response)
