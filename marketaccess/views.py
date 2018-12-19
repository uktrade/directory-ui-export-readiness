from directory_forms_api_client import actions

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from core import mixins
from marketaccess import forms


class ReportMarketAccessBarrierFormView(
    mixins.PrepopulateFormMixin,
    NamedUrlSessionWizardView
):
    success_url = reverse_lazy(
        'marketaccess-form-success'
    )

    START = 'start'
    ABOUT = 'about'
    PROBLEM_DETAILS = 'problem-details'
    OTHER_DETAILS = 'other-details'

    form_list = (
        (START, forms.StartForm),
        (ABOUT, forms.AboutForm),
        (PROBLEM_DETAILS, forms.ProblemDetailsForm),
        (OTHER_DETAILS, forms.OtherDetailsForm),
    )
    templates = {
        START: 'marketaccess/report_barrier_form/step-start.html',
        ABOUT: 'marketaccess/report_barrier_form/step-about.html',
        PROBLEM_DETAILS: 'marketaccess/report_barrier_form/step-problem.html',
        OTHER_DETAILS: 'marketaccess/report_barrier_form/step-others.html',
    }

    def get_form_kwargs(self, *args, **kwargs):
        return super(mixins.PrepopulateFormMixin, self).get_form_kwargs(
            *args, **kwargs
        )

    def get_form_initial(self, step):
        initial = super().get_form_initial(step)
        if step == self.ABOUT and self.company_profile:
            company = self.company_profile
            initial.update({
                'firstname': self.guess_given_name,
                'lastname': self.guess_family_name,
                'trading_name': company['name'],
                'email': self.request.sso_user.email,
                'phone': company['mobile_number'],
            })
        return initial

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def done(self, forms_list):
        # flatten the multi step data to one dictionary
        serialized_data = self.serialize_form_list(self.form_list)
        action = actions.ZendeskAction(
            email_address=serialized_data['email'],
            full_name=serialized_data['full_name'],
            subject=settings.CONTACT_MARKET_ACCESS_ZENDESK_SUBJECT,
            # informs zendesk which custom field to add to the ticket, allowing zendesk users to filter by this service (e.g, "show me all euexit tickets)
            service_name=settings.DIRECTORY_FORMS_API_ZENDESK_SEVICE_NAME,
            # informs forms-api of which zendesk account to send the ticket to
            subdomain=settings.EU_EXIT_ZENDESK_SUBDOMAIN,
            # simply allows the user of the forms API admin to filter results by this url
            form_url=reverse(
                'report-ma-barrier', kwargs={'step': 'start'}
            ),
        )
        # send to forms-api via POST request
        response = action.save(serialized_data)
        response.raise_for_status()
        return redirect(self.success_url)
