from directory_cms_client.constants import EXPORT_READINESS_GET_FINANCE_SLUG

from django.conf import settings
from django.http import Http404
from django.views.generic.edit import FormView
from django.views.generic.base import RedirectView, TemplateView

from core import mixins
from finance import forms


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


class DeprecatedGetFinance(
    mixins.GetCMSPageMixin, PiTrackerContextData, TemplateView
):
    template_name = 'finance/get_finance_deprecated.html'
    slug = EXPORT_READINESS_GET_FINANCE_SLUG + '-deprecated'


class GetFinance(
    mixins.GetCMSPageMixin, PiTrackerContextData, TemplateView
):
    template_name = 'finance/get_finance.html'
    slug = EXPORT_READINESS_GET_FINANCE_SLUG


class GetFinanceNegotiator(TemplateView):
    def __new__(cls, *args, **kwargs):
        if settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON']:
            return GetFinance(*args, **kwargs)
        else:
            return DeprecatedGetFinance(*args, **kwargs)


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
    """
    Using a redirect URL here instead of putting a hyperlink directly to Pardot
    in the html. the reason is go Google links to this page instead of Pardot.
    The reason that is desirable is in future we may change how we track, or
    change the Pardot URL, but Google or links in emails will still link to the
    old Pardot URL.
    """

    url = settings.UKEF_FORM_START_TRACKER_URL


class GetFinanceLeadGenerationSuccessView(TemplateView):
    template_name = 'finance/lead_generation_form_success.html'
