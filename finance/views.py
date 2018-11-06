from directory_constants.constants import cms
from formtools.wizard.views import NamedUrlSessionWizardView
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


class GetFinanceView(mixins.GetCMSPageMixin, TemplateView):
    template_name = 'finance/get_finance.html'
    slug = cms.EXPORT_READINESS_GET_FINANCE_SLUG


class PreventCaptchaRevalidationMixin:
    """When get_all_cleaned_data() is called the forms are revalidated,
    which causes captcha to fail becuase the same captcha response from google
    is posted to google multiple times. This captcha response is a nonce, and
    so google complains the second time it's seen.

    This is worked around by removing captcha from the form before the view
    calls get_all_cleaned_data

    """

    should_ignore_captcha = False

    def render_done(self, *args, **kwargs):
        self.should_ignore_captcha = True
        return super().render_done(*args, **kwargs)

    def get_form(self, step=None, *args, **kwargs):
        form = super().get_form(step=step, *args, **kwargs)
        if step == self.steps.last and self.should_ignore_captcha:
            del form.fields['captcha']
        return form


class GetFinanceLeadGenerationFormView(
    FeatureFlagMixin, PreventCaptchaRevalidationMixin,
    NamedUrlSessionWizardView
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
        del data['terms_agreed']
        return data


class GetFinanceLeadGenerationSuccessView(TemplateView):
    template_name = 'finance/lead_generation_form/success.html'
