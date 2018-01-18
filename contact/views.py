from formtools.wizard.views import SessionWizardView

from django.conf import settings
from django.http import Http404
from django.template.response import TemplateResponse
from django.views.generic import TemplateView

from contact import forms, helpers


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_CONTACT_US_ENABLED:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class InterstitialView(FeatureFlagMixin, TemplateView):
    template_name = 'contact/interstitial.html'
    service = None

    def dispatch(self, *args, **kwargs):
        self.request.session[helpers.INGRESS_URL_SESSION_KEY] = (
            self.request.META.get('HTTP_REFERER')
        )
        return super().dispatch(*args, **kwargs)


class TriageWizardFormView(FeatureFlagMixin, SessionWizardView):

    BUSINESS = 'business'
    DETAILS = 'business_details'
    EXPERIENCE = 'experience'
    CONTACT = 'contact'
    SUCCESS = 'success'

    form_list = (
        (BUSINESS, forms.YourBusinessForm),
        (DETAILS, forms.BusinessDetailsForm),
        (EXPERIENCE, forms.YourExperienceForm),
        (CONTACT, forms.ContactDetailsForm),
    )
    templates = {
        BUSINESS: 'contact/wizard-step-business.html',
        DETAILS: 'contact/wizard-step-details.html',
        EXPERIENCE: 'contact/wizard-step-experience.html',
        CONTACT: 'contact/wizard-step-contact.html',
        SUCCESS: 'contact/triage-success.html'
    }

    form_labels = (
        (BUSINESS, 'Your business'),
        (DETAILS, 'Business details'),
        (EXPERIENCE, 'Your experience'),
        (CONTACT, 'Contact details'),
    )

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, *args, **kwargs):
        helpers.create_zendesk_ticket(
            cleaned_data=self.get_all_cleaned_data(),
            service=self.kwargs['service'],
            ingress_url=helpers.get_ingress_url(self.request),
        )
        return TemplateResponse(self.request, self.templates[self.SUCCESS])

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs, form_labels=self.form_labels,
        )


class FeedbackWizardFormView(FeatureFlagMixin, SessionWizardView):
    service = None

    FEEDBACK = 'feedback'
    SUCCESS = 'success'

    form_list = (
        (FEEDBACK, forms.FeedbackForm),
    )
    templates = {
        FEEDBACK: 'contact/feedback.html',
        SUCCESS: 'contact/feedback-success.html'
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, *args, **kwargs):
        helpers.create_zendesk_ticket(
            cleaned_data=self.get_all_cleaned_data(),
            service=self.kwargs.get('service'),
            ingress_url=helpers.get_ingress_url(self.request),
        )
        return TemplateResponse(self.request, self.templates[self.SUCCESS])
