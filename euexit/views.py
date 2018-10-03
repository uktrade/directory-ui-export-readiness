from directory_cms_client.client import cms_api_client
from directory_cms_client.constants import (
    EXPORT_READINESS_EUEXIT_INTERNATIONAL_FORM
)

from django.conf import settings
from django.http import Http404
from django.urls import reverse_lazy
from django.utils.functional import cached_property
from django.views.generic import TemplateView
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
    success_url = reverse_lazy('eu-exit-international-contact-form-success')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        return kwargs

    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=EXPORT_READINESS_EUEXIT_INTERNATIONAL_FORM,
            language_code=settings.LANGUAGE_CODE,
            draft_token=self.request.GET.get('draft_token'),
        )
        if response.status_code == 404:
            raise Http404()
        return handle_cms_response(response)

    def form_valid(self, form):
        cleaned_data = form.serialized_data
        name = cleaned_data['first_name'] + ' ' + cleaned_data['last_name']
        response = form.save(
            email_address=cleaned_data['email'],
            full_name=name,
            subject='EU Exit international contact form'
        )
        response.raise_for_status()
        return super().form_valid(form)


class InternationalContactSuccessView(TemplateView):
    template_name = 'euexit/international-contact-form-success.html'
