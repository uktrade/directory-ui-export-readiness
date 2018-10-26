from django.conf import settings
from django.http import Http404

from formtools.wizard.views import SessionWizardView

from contact import forms


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['CONTACT_US_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)



class RoutingFormView(FeatureFlagMixin, SessionWizardView):
    LOCATION = 'location'
    INTERNATIONAL = 'international'
    DOMESTIC = 'domestic'
    GREAT_SERVICES = 'great-services'
    GREAT_ACCOUNT = 'great-account'
    EXPORT_OPPORTUNITIES = 'export-opportunities'

    form_list = (
        (LOCATION, forms.LocationRoutingForm),
        (DOMESTIC, forms.DomesticRoutingForm),
        (GREAT_SERVICES, forms.GreatServicesRoutingForm),
        (GREAT_ACCOUNT, forms.GreatAccountRoutingForm),
        (EXPORT_OPPORTUNITIES, forms.ExportOpportunitiesServiceRoutingForm),
        (INTERNATIONAL, forms.InternationalRoutingForm),
    )
    templates = {
        LOCATION: 'contact/routing-step-location.html',
        DOMESTIC: 'contact/routing-step-domestic.html',
        GREAT_SERVICES: 'contact/routing-step-great-services.html',
        GREAT_ACCOUNT: 'contact/routing-step-great-account.html',
        EXPORT_OPPORTUNITIES: 'contact/routing-step-export-opportunities-service.html',
        INTERNATIONAL: 'contact/routing-step-international.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, *args, **kwargs):
        #  ¯\_(ツ)_/¯
        pass
