from directory_forms_api_client import actions

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy

from core import mixins
from marketaccess import forms


class ReportMarketAccessBarrierFormView(
    mixins.NotFoundOnDisabledFeature,
    NamedUrlSessionWizardView
):
    success_url = reverse_lazy(
        'marketaccess-form-success'
    )

    ABOUT = 'about'
    PROBLEM_DETAILS = 'problem-details'
    OTHER_DETAILS = 'other-details'
    SUMMARY = 'summary'

    form_list = (
        (ABOUT, forms.AboutForm),
        (PROBLEM_DETAILS, forms.ProblemDetailsForm),
        (OTHER_DETAILS, forms.OtherDetailsForm),
        (SUMMARY, forms.SummaryForm),
    )
    templates = {
        ABOUT: 'marketaccess/report_barrier_form/step-about.html',
        PROBLEM_DETAILS: 'marketaccess/report_barrier_form/step-problem.html',
        OTHER_DETAILS: 'marketaccess/report_barrier_form/step-others.html',
        SUMMARY: 'marketaccess/report_barrier_form/step-summary.html',
    }

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['MARKET_ACCESS_FORM_ON']

    def get_form_kwargs(self, *args, **kwargs):
        return super(mixins.PrepopulateFormMixin, self).get_form_kwargs(
            *args, **kwargs
        )

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == self.SUMMARY:
            data = self.get_all_cleaned_data()
            context['all_cleaned_data'] = data
        return context

    def done(self, forms_list):
        # flatten the multi step data to one dictionary
        serialized_data = self.serialize_form_list(self.form_list)
        action = actions.ZendeskAction(
            email_address=serialized_data['email'],
            full_name=serialized_data['full_name'],
            subject=settings.CONTACT_MARKET_ACCESS_ZENDESK_SUBJECT,
            # informs zendesk which custom field to add to the ticket, allowing zendesk users to filter by this service (e.g, "show me all euexit tickets)
            service_name=settings.MARKET_ACCESS_FORMS_API_ZENDESK_SEVICE_NAME,
            # informs forms-api of which zendesk account to send the ticket to
            subdomain=settings.MARKET_ACCCESS_ZENDESK_SUBDOMAIN,
            # simply allows the user of the forms API admin to filter results by this url
            form_url=reverse(
                'report-ma-barrier', kwargs={'step': 'about'}
            ),
        )
        # send to forms-api via POST request
        response = action.save(serialized_data)
        response.raise_for_status()
        return redirect(self.success_url)
