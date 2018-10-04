from directory_cms_client.client import cms_api_client
from directory_cms_client.constants import (
    EXPORT_READINESS_EUEXIT_DOMESTIC_FORM_SLUG,
    EXPORT_READINESS_EUEXIT_INTERNATIONAL_FORM_SLUG,
    EXPORT_READINESS_EUEXIT_FORM_SUCCESS_SLUG,
)

from django.conf import settings
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core.mixins import GetCMSPageMixin
from euexit import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class BaseInternationalContactFormView(
    FeatureFlagMixin, GetCMSPageMixin, FormView
):
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        return kwargs

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


class InternationalContactFormView(BaseInternationalContactFormView):
    slug = EXPORT_READINESS_EUEXIT_INTERNATIONAL_FORM_SLUG
    form_class = forms.InternationalContactForm
    template_name = 'euexit/international-contact-form.html'
    success_url = reverse_lazy('eu-exit-international-contact-form-success')


class DomesticContactFormView(BaseInternationalContactFormView):
    slug = EXPORT_READINESS_EUEXIT_DOMESTIC_FORM_SLUG
    form_class = forms.DomesticContactForm
    template_name = 'euexit/domestic-contact-form.html'
    success_url = reverse_lazy('eu-exit-domestic-contact-form-success')


class InternationalContactSuccessView(
    FeatureFlagMixin, GetCMSPageMixin, TemplateView
):
    template_name = 'euexit/international-contact-form-success.html'
    slug = EXPORT_READINESS_EUEXIT_FORM_SUCCESS_SLUG


class DomesticContactSuccessView(
    FeatureFlagMixin, GetCMSPageMixin, TemplateView
):
    template_name = 'euexit/domestic-contact-form-success.html'
    slug = EXPORT_READINESS_EUEXIT_FORM_SUCCESS_SLUG
