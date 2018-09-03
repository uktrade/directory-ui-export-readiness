from directory_cms_client.constants import EXPORT_READINESS_GET_FINANCE_SLUG

from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView, TemplateView

from core import mixins
from finance import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['UKEF_LEAD_GENEATION_ON']:
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


class GetFinanceCMS(
    mixins.GetCMSPageMixin, PiTrackerContextData, TemplateView
):
    template_name = 'finance/get_finance.html'
    slug = EXPORT_READINESS_GET_FINANCE_SLUG


class GetFinanceLeadGenerationFormView(
    FeatureFlagMixin, PiTrackerContextData, FormView
):
    form_class = forms.ExampleForm
    template_name = 'finance/lead_generation_form.html'

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            form_submit_tracker_url=settings.UKEF_FORM_SUBMIT_TRACKER_URL,
            *args,
            **kwargs,
        )


class GetFinanceStartRedirectView(FeatureFlagMixin, RedirectView):
    url = settings.UKEF_FORM_START_TRACKER_URL


class GetFinanceLeadGenerationSuccessView(TemplateView):
    template_name = 'finance/lead_generation_form_success.html'
