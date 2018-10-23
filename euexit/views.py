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

from core.mixins import GetCMSPageMixin, TranslationsMixin
from euexit import forms


SESSION_KEY_FORM_INGRESS_URL = 'FORM_INGRESS_URL'


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class HideLanguageSelectorMixin(TranslationsMixin):
    def get_context_data(self, **kwargs):
        return super().get_context_data(
            hide_language_selector=True,
            **kwargs,
        )


class BaseInternationalContactFormView(
    FeatureFlagMixin, GetCMSPageMixin, HideLanguageSelectorMixin, FormView,
):

    def get(self, *args, **kwargs):
        self.request.session[SESSION_KEY_FORM_INGRESS_URL] = (
            self.request.META.get('HTTP_REFERER')
        )
        return super().get(*args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['field_attributes'] = self.page
        kwargs['form_url'] = self.request.build_absolute_uri()
        kwargs['ingress_url'] = (
            self.request.session.get(SESSION_KEY_FORM_INGRESS_URL)
        )
        kwargs['disclaimer'] = self.page['disclaimer']
        return kwargs

    def form_valid(self, form):
        cleaned_data = form.serialized_data
        name = cleaned_data['first_name'] + ' ' + cleaned_data['last_name']
        response = form.save(
            email_address=cleaned_data['email'],
            full_name=name,
            subject=self.subject,
            subdomain=settings.EU_EXIT_ZENDESK_SUBDOMAIN,
        )
        response.raise_for_status()
        return super().form_valid(form)


class BaseContactView(
    FeatureFlagMixin, GetCMSPageMixin, HideLanguageSelectorMixin, TemplateView
):
    pass


class InternationalContactFormView(BaseInternationalContactFormView):
    slug = EXPORT_READINESS_EUEXIT_INTERNATIONAL_FORM_SLUG
    form_class = forms.InternationalContactForm
    template_name = 'euexit/international-contact-form.html'
    success_url = reverse_lazy('eu-exit-international-contact-form-success')
    subject = 'EU Exit international contact form'


class DomesticContactFormView(BaseInternationalContactFormView):
    slug = EXPORT_READINESS_EUEXIT_DOMESTIC_FORM_SLUG
    form_class = forms.DomesticContactForm
    template_name = 'euexit/domestic-contact-form.html'
    success_url = reverse_lazy('eu-exit-domestic-contact-form-success')
    subject = 'EU Exit contact form'


class InternationalContactSuccessView(BaseContactView):
    template_name = 'euexit/international-contact-form-success.html'
    slug = EXPORT_READINESS_EUEXIT_FORM_SUCCESS_SLUG


class DomesticContactSuccessView(BaseContactView):
    template_name = 'euexit/domestic-contact-form-success.html'
    slug = EXPORT_READINESS_EUEXIT_FORM_SUCCESS_SLUG
