from directory_cms_client.constants import EXPORT_READINESS_GET_FINANCE_SLUG
from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.http import Http404
from django.views.generic.base import TemplateView

from core import mixins
from finance import forms, helpers


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class PiTrackerContextData:
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            pi_tracker_javascript_url=settings.UKEF_PI_TRACKER_JAVASCRIPT_URL,
            pi_tracker_account_id=settings.UKEF_PI_TRACKER_ACCOUNT_ID,
            pi_tracker_campaign_id=settings.UKEF_PI_TRACKER_CAMPAIGN_ID,
            *args,
            **kwargs,
        )


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
    FeatureFlagMixin, NamedUrlSessionWizardView
):

    CATEGORY = 'contact'
    PERSONAL_DETAILS = 'your-details'
    COMPANY_DETAILS = 'company-details'
    HELP = 'help'
    DONE = 'done'

    form_list = (
        (CATEGORY, forms.CategoryForm),
        (PERSONAL_DETAILS, forms.PersonalDetailsForm),
        (COMPANY_DETAILS, forms.CompanyDetailsForm),
        (HELP, forms.HelpForm),
        (DONE, forms.forms.Form),  # noop
    )
    templates = {
        CATEGORY: 'finance/lead_generation_form/step-category.html',
        PERSONAL_DETAILS: 'finance/lead_generation_form/step-personal.html',
        COMPANY_DETAILS: 'finance/lead_generation_form/step-company.html',
        HELP: 'finance/lead_generation_form/step-help.html',
        DONE: 'finance/lead_generation_form/step-done.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        if self.steps.current == self.DONE:
            data = self.get_all_cleaned_data()
            # from ipdb import set_trace; set_trace()
            context_data['all_form_data'] = helpers.flatten_form_data(data)
            context_data['form_submit_url'] = (
                settings.UKEF_FORM_SUBMIT_TRACKER_URL
            )
        return context_data


class GetFinanceLeadGenerationSuccessView(TemplateView):
    template_name = 'finance/lead_generation_form/success.html'
