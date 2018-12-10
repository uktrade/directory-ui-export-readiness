from directory_constants.constants import cms
from directory_forms_api_client.actions import PardotAction
from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
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


class GetFinanceLeadGenerationFormView(
    FeatureFlagMixin, mixins.PreventCaptchaRevalidationMixin,
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
        action = PardotAction(
            pardot_url=settings.UKEF_FORM_SUBMIT_TRACKER_URL,
            form_url=reverse(
                'uk-export-finance-lead-generation-form',
                kwargs={'step': self.CATEGORY}
            )
        )
        response = action.save(
            self.serialize_form_list(form_list),
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
