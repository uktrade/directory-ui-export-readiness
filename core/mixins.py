from directory_cms_client.client import cms_api_client
from directory_constants.constants import cms
from django.http import Http404
from django.conf import settings
from directory_cms_client.helpers import (
    handle_cms_response, handle_cms_response_allow_404
)
from django.shortcuts import redirect

from django.utils import translation
from django.utils.functional import cached_property

from core import helpers

EXPORT_JOURNEY_REDIRECTS = {
    '/market-research/': '/advice/find-an-export-market/',
    '/market-research/do-research-first/':
        '/advice/find-an-export-market/plan-export-market-research',
    '/market-research/define-market-potential/':
        '/advice/find-an-export-market/define-export-market-potential',
    '/market-research/analyse-the-competition/':
        '/advice/find-an-export-market/define-export-market-potential',
    '/market-research/research-your-market/':
        '/advice/find-an-export-market/field-research-in-export-markets',
    '/market-research/visit-a-trade-show/':
        '/advice/find-an-export-market/trade-shows',
    '/market-research/doing-business-with-integrity/':
        '/advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets',  # NOQA
    '/market-research/know-the-relevant-legislation/':
        '/advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets',  # NOQA

    '/business-planning/': '/advice/define-route-to-market/',
    '/business-planning/make-an-export-plan/':
        '/advice/create-an-export-plan/how-to-create-an-export-plan',
    '/business-planning/find-a-route-to-market/':
        '/advice/define-route-to-market/routes-to-market',
    '/business-planning/sell-overseas-directly/':
        '/advice/define-route-to-market/sell-overseas-directly',
    '/business-planning/use-an-overseas-agent/':
        '/advice/define-route-to-market/export-agents',
    '/business-planning/choosing-an-agent-or-distributor/':
        '/advice/define-route-to-market/export-agents',
    '/business-planning/use-a-distributor/':
        '/advice/define-route-to-market/export-distributors',
    '/business-planning/license-your-product-or-service/':
        '/advice/define-route-to-market/create-a-licensing-agreement',
    '/business-planning/licensing-and-franchising/':
        '/advice/define-route-to-market/create-a-licensing-agreement',
    '/business-planning/franchise-your-business/':
        '/advice/define-route-to-market/create-a-franchise-agreement',
    '/business-planning/start-a-joint-venture/':
        '/advice/define-route-to-market/create-a-joint-venture-agreement',
    '/business-planning/set-up-an-overseas-operation/':
        '/advice/define-route-to-market/set-up-a-business-abroad',

    '/finance/': '/advice/get-export-finance-and-funding/',
    '/finance/choose-the-right-finance/':
        '/advice/get-export-finance-and-funding/choose-the-right-finance',
    '/finance/get-money-to-export/':
        '/advice/get-export-finance-and-funding/choose-the-right-finance',
    '/finance/get-export-finance/':
        '/advice/get-export-finance-and-funding/get-export-finance',
    '/finance/get-finance-support-from-government/':
        '/advice/get-export-finance-and-funding/get-export-finance',
    '/finance/raise-money-by-borrowing/':
        '/advice/get-export-finance-and-funding/raise-money-by-borrowing',
    '/finance/borrow-against-assets/':
        '/advice/get-export-finance-and-funding/borrow-against-assets',
    '/finance/raise-money-with-investment/':
        '/advice/get-export-finance-and-funding/raise-money-with-investment',

    '/getting-paid/': '/advice/manage-payment-for-export-orders/',
    '/getting-paid/invoice-currency-and-contents/':
        '/advice/manage-payment-for-export-orders/payment-methods-for-exporters',  # NOQA
    '/getting-paid/consider-how-youll-get-paid/':
        '/advice/manage-payment-for-export-orders/how-to-create-an-export-invoice',  # NOQA
    '/getting-paid/decide-when-youll-get-paid/':
        '/advice/manage-payment-for-export-orders/decide-when-youll-get-paid-for-export-orders',  # NOQA
    '/getting-paid/payment-methods/':
        '/advice/manage-payment-for-export-orders/payment-methods-for-exporters',  # NOQA
    '/getting-paid/insure-against-non-payment/':
        '/advice/manage-payment-for-export-orders/insure-against-non-payment',

    '/customer-insight/':
        '/advice/prepare-to-do-business-in-a-foreign-country/',
    '/customer-insight/meet-your-customers/':
        '/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market',  # NOQA
    '/customer-insight/know-your-customers/':
        '/advice/manage-legal-and-ethical-compliance/understand-business-risks-in-overseas-markets',  # NOQA
    '/customer-insight/manage-language-differences/':
        '/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market',  # NOQA
    '/customer-insight/understand-your-customers-culture/':
        '/advice/prepare-to-do-business-in-a-foreign-country/understand-the-business-culture-in-the-market',  # NOQA

    '/operations-and-compliance/':
        '/advice/manage-legal-and-ethical-compliance/',
    '/operations-and-compliance/internationalise-your-website/':
        '/advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website',  # NOQA
    '/operations-and-compliance/match-your-website-to-your-audience/':
        '/advice/prepare-to-do-business-in-a-foreign-country/internationalise-your-website',  # NOQA
    '/operations-and-compliance/protect-your-intellectual-property/':
        '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting',  # NOQA
    '/operations-and-compliance/types-of-intellectual-property/':
        '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting',  # NOQA
    '/operations-and-compliance/know-what-ip-you-have/':
        '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting',  # NOQA
    '/operations-and-compliance/international-ip-protection/':
        '/advice/manage-legal-and-ethical-compliance/protect-your-intellectual-property-when-exporting',  # NOQA
    '/operations-and-compliance/report-corruption/':
        '/advice/manage-legal-and-ethical-compliance/report-corruption-and-human-rights-violations',  # NOQA
    '/operations-and-compliance/anti-bribery-and-corruption-training/':
        '/advice/manage-legal-and-ethical-compliance/anti-bribery-and-corruption-training',  # NOQA
    '/operations-and-compliance/plan-the-logistics/':
        '/advice/prepare-for-export-procedures-and-logistics/plan-logistics-for-exporting',  # NOQA
    '/operations-and-compliance/get-your-export-documents-right/':
        '/advice/prepare-for-export-procedures-and-logistics/get-your-export-documents-right',  # NOQA
    '/operations-and-compliance/use-a-freight-forwarder/':
        '/advice/prepare-for-export-procedures-and-logistics/use-a-freight-forwarder-to-export',  # NOQA
    '/operations-and-compliance/use-incoterms-in-contracts/':
        '/advice/prepare-for-export-procedures-and-logistics/use-incoterms-in-contracts',  # NOQA

    '/new/next-steps/': '/advice',
    '/occasional/next-steps/': '/advice',
    '/regular/next-steps/': '/advice',

    '/new/': '/advice',
    '/occasional/': '/advice',
    '/regular/': '/advice'
}


class NotFoundOnDisabledFeature:
    def dispatch(self, *args, **kwargs):
        if not self.flag:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class ExportJourneyFeatureFlagMixin:
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON']

    def dispatch(self, *args, **kwargs):
        if not self.flag:
            if self.request.path in EXPORT_JOURNEY_REDIRECTS:
                return redirect(EXPORT_JOURNEY_REDIRECTS[self.request.path])
        return super().dispatch(*args, **kwargs)


class AdviceSectionFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return not settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON']


class CampaignPagesFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['CAMPAIGN_PAGES_ON']


class NewsSectionFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['NEWS_SECTION_ON']


class PrototypeFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['PROTOTYPE_PAGES_ON']


class PerformanceDashboardFeatureFlagMixin(NotFoundOnDisabledFeature):
    @property
    def flag(self):
        return settings.FEATURE_FLAGS['PERFORMANCE_DASHBOARD_ON']


class GetCMSPageMixin:
    @cached_property
    def page(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
        )
        return handle_cms_response(response)

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(page=self.page, *args, **kwargs)


class GetCMSComponentMixin:
    @cached_property
    def cms_component(self):
        response = cms_api_client.lookup_by_slug(
            slug=self.component_slug,
            language_code=translation.get_language(),
            draft_token=self.request.GET.get('draft_token'),
            service_name=cms.COMPONENTS,
        )
        return handle_cms_response_allow_404(response)

    @property
    def component_is_bidi(self):
        if self.cms_component:
            return helpers.cms_component_is_bidi(
                translation.get_language(),
                self.cms_component['meta']['languages']
            )
        return False

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            component_is_bidi=self.component_is_bidi,
            cms_component=self.cms_component,
            *args, **kwargs
        )


class TranslationsMixin:

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        context['directory_components_html_lang_attribute']\
            = translation.get_language()
        return context


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


class PrepopulateFormMixin:

    @cached_property
    def company_profile(self):
        return helpers.get_company_profile(self.request)

    def get_form_kwargs(self):
        form_kwargs = super().get_form_kwargs()
        form_kwargs['initial'] = self.get_form_initial()
        return form_kwargs

    @property
    def guess_given_name(self):
        if self.company_profile and self.company_profile['postal_full_name']:
            name = self.company_profile['postal_full_name']
            return name.split(' ')[0]

    @property
    def guess_family_name(self):
        if self.company_profile and self.company_profile['postal_full_name']:
            names = self.company_profile['postal_full_name'].split(' ')
            return names[-1] if len(names) > 1 else None
