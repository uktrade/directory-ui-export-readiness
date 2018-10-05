from directory_cms_client.constants import EXPORT_READINESS_GET_FINANCE_SLUG
from formtools.wizard.views import NamedUrlCookieWizardView
import requests

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView

from core import mixins
from finance import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class DeprecatedGetFinance(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'finance/get_finance_deprecated.html'
    slug = EXPORT_READINESS_GET_FINANCE_SLUG + '-deprecated'


class GetFinance(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'finance/get_finance.html'
    slug = EXPORT_READINESS_GET_FINANCE_SLUG


class GetFinanceNegotiator(TemplateView):
    def __new__(cls, *args, **kwargs):
        if settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON']:
            return GetFinance(*args, **kwargs)
        else:
            return DeprecatedGetFinance(*args, **kwargs)


class GetFinanceLeadGenerationFormView(
    FeatureFlagMixin, NamedUrlCookieWizardView
):
    success_url = reverse_lazy(
        'uk-export-finance-lead-generation-form-success'
    )

    CATEGORY = 'contact'
    PERSONAL_DETAILS = 'your-details'
    COMPANY_DETAILS = 'company-details'
    HELP = 'help'

    form_list = (
        (CATEGORY, forms.CategoryForm),
        (PERSONAL_DETAILS, forms.PersonalDetailsForm),
        (COMPANY_DETAILS, forms.CompanyDetailsForm),
        (HELP, forms.HelpForm),
    )
    templates = {
        CATEGORY: 'finance/lead_generation_form/step-category.html',
        PERSONAL_DETAILS: 'finance/lead_generation_form/step-personal.html',
        COMPANY_DETAILS: 'finance/lead_generation_form/step-company.html',
        HELP: 'finance/lead_generation_form/step-help.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, form_list, **kwargs):
        response = requests.post(
            settings.UKEF_FORM_SUBMIT_TRACKER_URL,
            self.serialize_form_list(form_list),
            allow_redirects=False,
        )
        response.raise_for_status()
        return redirect(self.success_url)

    @staticmethod
    def serialize_form_list(form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        del data['captcha']
        del data['terms_agreed']
        return data


class GetFinanceLeadGenerationSuccessView(TemplateView):
    template_name = 'finance/lead_generation_form/success.html'
