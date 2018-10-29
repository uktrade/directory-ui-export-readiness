from directory_cms_client.constants import (
    EXPORT_READINESS_EUEXIT_DOMESTIC_FORM_SLUG,
    EXPORT_READINESS_EUEXIT_INTERNATIONAL_FORM_SLUG,
    EXPORT_READINESS_EUEXIT_FORM_SUCCESS_SLUG,
)

from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core.mixins import GetCMSPageMixin
from euexit import forms
from euexit.mixins import (
    EUExitFormsFeatureFlagMixin, HideLanguageSelectorMixin)


SESSION_KEY_FORM_INGRESS_URL = 'FORM_INGRESS_URL'


class BaseInternationalContactFormView(
    EUExitFormsFeatureFlagMixin,
    GetCMSPageMixin,
    HideLanguageSelectorMixin,
    FormView,
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
        kwargs['subject'] = self.subject
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class BaseContactView(
    EUExitFormsFeatureFlagMixin,
    GetCMSPageMixin,
    HideLanguageSelectorMixin,
    TemplateView
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
