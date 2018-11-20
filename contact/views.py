from directory_constants.constants import cms
from directory_forms_api_client.actions import EmailAction, GovNotifyAction

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from core import mixins
from contact import constants, forms


SESSION_KEY_FORM_INGRESS_URL = 'CONTACT_FORM_INGRESS_URL'


def build_export_opportunites_guidance_url(step_name, ):
    return reverse_lazy(
        'contact-us-export-opportunities-guidance', kwargs={'slug': step_name}
    )


def build_great_account_guidance_url(step_name, ):
    return reverse_lazy(
        'contact-us-great-account-guidance', kwargs={'slug': step_name}
    )


class FormIngressURLMixin:

    def get(self, *args, **kwargs):
        if SESSION_KEY_FORM_INGRESS_URL not in self.request.session:
            self.request.session[SESSION_KEY_FORM_INGRESS_URL] = (
                self.request.META.get('HTTP_REFERER')
            )
        return super().get(*args, **kwargs)

    @property
    def ingress_url(self):
        return self.request.session.get(SESSION_KEY_FORM_INGRESS_URL)

    @property
    def form_url(self):
        return self.request.build_absolute_uri()

    def clear_ingress_url(self):
        del self.request.session[SESSION_KEY_FORM_INGRESS_URL]


class FeatureFlagMixin:
    def dispatch(self, *args, **kwargs):
        if not settings.FEATURE_FLAGS['CONTACT_US_ON']:
            raise Http404()
        return super().dispatch(*args, **kwargs)


class SendNotifyMessagesMixin:

    def send_agent_message(self, form):
        response = form.save(
            template_id=self.notify_template_id_agent,
            email_address=self.notify_email_address_agent,
        )
        response.raise_for_status()

    def send_user_message(self, form):
        response = form.save(
            template_id=self.notify_template_id_user,
            email_address=form.cleaned_data['email'],
        )
        response.raise_for_status()

    def form_valid(self, form):
        self.send_agent_message(form)
        self.send_user_message(form)
        return super().form_valid(form)


class BaseNotifyFormView(
    FeatureFlagMixin, FormIngressURLMixin, SendNotifyMessagesMixin, FormView
):
    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'form_url': self.form_url,
            'ingress_url': self.ingress_url,
        }

    def form_valid(self, form):
        response = super().form_valid(form)
        self.clear_ingress_url()
        return response


class BaseSuccessView(FeatureFlagMixin, mixins.GetCMSPageMixin, TemplateView):
    pass



class RoutingFormView(
    FeatureFlagMixin, FormIngressURLMixin, NamedUrlSessionWizardView
):

    # given the current step, based on selected  option, where to redirect.
    redirect_mapping = {
        constants.DOMESTIC: {
            constants.TRADE_OFFICE: settings.FIND_TRADE_OFFICE_URL,
            constants.EXPORT_ADVICE: reverse_lazy(
                'contact-us-export-advice',
                kwargs={'step': 'comment'}
            ),
            constants.FINANCE: reverse_lazy(
                'uk-export-finance-lead-generation-form',
                kwargs={'step': 'contact'}
            ),
            constants.EUEXIT: reverse_lazy('eu-exit-domestic-contact-form'),
            constants.EVENTS: reverse_lazy('contact-us-events-form'),
            constants.DSO: reverse_lazy('contact-us-dso-form'),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.INTERNATIONAL: {
            constants.INVESTING: settings.INVEST_CONTACT_URL,
            constants.BUYING: reverse_lazy('contact-us-find-uk-companies'),
            constants.EUEXIT: reverse_lazy(
                'eu-exit-international-contact-form'
            ),
            constants.OTHER: reverse_lazy('contact-us-international'),
        },
        constants.EXPORT_OPPORTUNITIES: {
            constants.NO_RESPONSE: reverse_lazy('contact-us-domestic'),
            constants.ALERTS: build_export_opportunites_guidance_url(
                cms.EXPORT_READINESS_HELP_EXOPP_ALERTS_IRRELEVANT_SLUG
            ),
            constants.MORE_DETAILS: reverse_lazy('contact-us-domestic'),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_SERVICES: {
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        },
        constants.GREAT_ACCOUNT: {
            constants.NO_VERIFICATION_EMAIL: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_MISSING_VERIFY_EMAIL_SLUG
            ),
            constants.PASSWORD_RESET: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_PASSWORD_RESET_SLUG
            ),
            constants.COMPANIES_HOUSE_LOGIN: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_COMPANIES_HOUSE_LOGIN_SLUG
            ),
            constants.VERIFICATION_CODE: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_ENTER_SLUG,
            ),
            constants.NO_VERIFICATION_LETTER: build_great_account_guidance_url(
                cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_LETTER_SLUG
            ),
            constants.OTHER: reverse_lazy('contact-us-domestic'),
        }
    }

    form_list = (
        (constants.LOCATION, forms.LocationRoutingForm),
        (constants.DOMESTIC, forms.DomesticRoutingForm),
        (constants.GREAT_SERVICES, forms.GreatServicesRoutingForm),
        (constants.GREAT_ACCOUNT, forms.GreatAccountRoutingForm),
        (constants.EXPORT_OPPORTUNITIES, forms.ExportOpportunitiesRoutingForm),
        (constants.INTERNATIONAL, forms.InternationalRoutingForm),
        ('NO-OPERATION', forms.NoOpForm),  # should never be reached
    )
    templates = {
        constants.LOCATION: 'contact/routing/step-location.html',
        constants.DOMESTIC: 'contact/routing/step-domestic.html',
        constants.GREAT_SERVICES: 'contact/routing/step-great-services.html',
        constants.GREAT_ACCOUNT: 'contact/routing/step-great-account.html',
        constants.EXPORT_OPPORTUNITIES: (
            'contact/routing/step-export-opportunities-service.html'
        ),
        constants.INTERNATIONAL: 'contact/routing/step-international.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_redirect_url(self, choice):
        if self.steps.current in self.redirect_mapping:
            mapping = self.redirect_mapping[self.steps.current]
            return mapping.get(choice)

    def render_next_step(self, form):
        choice = form.cleaned_data['choice']
        redirect_url = self.get_redirect_url(choice)
        if redirect_url:
            return redirect(redirect_url)
        return self.render_goto_step(choice)


class ExportingAdviceFormView(
    FeatureFlagMixin, mixins.PreventCaptchaRevalidationMixin,
    FormIngressURLMixin, NamedUrlSessionWizardView
):
    success_url = reverse_lazy('contact-us-domestic-success')

    COMMENT = 'comment'
    PERSONAL = 'personal'
    BUSINESS = 'business'

    form_list = (
        (COMMENT, forms.CommentForm),
        (PERSONAL, forms.PersonalDetailsForm),
        (BUSINESS, forms.BusinessDetailsForm),
    )

    templates = {
        COMMENT: 'contact/exporting/step-comment.html',
        PERSONAL: 'contact/exporting/step-personal.html',
        BUSINESS: 'contact/exporting/step-business.html',
    }

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    @staticmethod
    def send_user_message(form_data):
        action = GovNotifyAction(
            template_id=settings.CONTACT_EXPORTING_USER_NOTIFY_TEMPLATE_ID,
            email_address=form_data['email'],
        )
        response = action.save(form_data)
        response.raise_for_status()

    @staticmethod
    def send_agent_message(form_data):
        action = EmailAction(
            # todo: retrieve email from office finder
            recipients=['text@example.com'],
            subject=settings.CONTACT_EXPORTING_AGENT_SUBJECT,
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        template_name = 'contact/exporting-from-uk-agent-email.html'
        text = render_to_string(template_name, {'form_data': form_data})
        response = action.save({'text_body': text, 'html_body': text})
        response.raise_for_status()

    def done(self, form_list, **kwargs):
        form_data = self.serialize_form_list(form_list)
        self.send_agent_message(form_data)
        self.send_user_message(form_data)
        self.clear_ingress_url()
        return redirect(self.success_url)

    def serialize_form_list(self, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        del data['terms_agreed']
        data['ingress_url'] = self.ingress_url
        data['form_url'] = self.form_url
        return data


class FeedbackFormView(FeatureFlagMixin, FormIngressURLMixin, FormView):
    form_class = forms.FeedbackForm
    template_name = 'contact/comment-contact.html'
    success_url = reverse_lazy('contact-us-feedback-success')

    def get_form_kwargs(self):
        return {
            **super().get_form_kwargs(),
            'form_url': self.form_url,
            'ingress_url': self.ingress_url,
        }

    def form_valid(self, form):
        response = form.save(
            email_address=form.cleaned_data['email'],
            full_name=form.cleaned_data['name'],
            subject=settings.CONTACT_DOMESTIC_ZENDESK_SUBJECT,
        )
        response.raise_for_status()
        self.clear_ingress_url()
        return super().form_valid(form)


class InternationalFormView(BaseNotifyFormView):
    form_class = forms.InternationalContactForm
    template_name = 'contact/international/step.html'
    success_url = reverse_lazy('contact-us-international-success')

    notify_template_id_agent = (
        settings.CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID
    )
    notify_email_address_agent = (
        settings.CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS
    )
    notify_template_id_user = (
        settings.CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID
    )


class BuyingFromUKCompaniesFormView(BaseNotifyFormView):
    form_class = forms.BuyingFromUKContactForm
    template_name = 'contact/comment-contact.html'
    success_url = reverse_lazy('contact-us-find-uk-companies-success')

    notify_template_id_agent = settings.CONTACT_BUYING_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_BUYING_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_BUYING_USER_NOTIFY_TEMPLATE_ID


class DomesticFormView(BaseNotifyFormView):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-domestic-success')

    notify_template_id_agent = settings.CONTACT_DIT_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_DIT_USER_NOTIFY_TEMPLATE_ID


class EventsFormView(BaseNotifyFormView):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-events-success')

    notify_template_id_agent = settings.CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_EVENTS_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID


class DefenceAndSecurityOrganisationFormView(BaseNotifyFormView):
    form_class = forms.DomesticContactForm
    template_name = 'contact/domestic/step.html'
    success_url = reverse_lazy('contact-us-dso-success')

    notify_template_id_agent = settings.CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID
    notify_email_address_agent = settings.CONTACT_DSO_AGENT_EMAIL_ADDRESS
    notify_template_id_user = settings.CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID


class InternationalSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_INTERNATIONAL_SLUG


class DomesticSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_SLUG


class EventsSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_EVENTS_SLUG


class DefenceAndSecurityOrganisationSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_DSO_SLUG


class ExportingAdviceSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_EXPORT_ADVICE_SLUG


class FeedbackSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_FEEDBACK_SLUG


class BuyingFromUKCompaniesSuccessView(BaseSuccessView):
    template_name = 'contact/submit-success.html'
    slug = cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_FIND_COMPANIES_SLUG


class GuidanceView(BaseSuccessView):
    template_name = 'contact/guidance.html'

    @property
    def slug(self):
        return self.kwargs['slug']
