from directory_forms_api_client import actions

from formtools.wizard.views import NamedUrlSessionWizardView

from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView


from core import mixins
from marketaccess import forms


class MarketAccessView(
    mixins.NotFoundOnDisabledFeature,
    TemplateView
):
    template_name = "marketaccess/report_a_barrier.html"

    @property
    def flag(self):
        return settings.FEATURE_FLAGS['MARKET_ACCESS_FORM_ON']


class ReportMarketAccessBarrierSuccessView(TemplateView):
    template_name = "marketaccess/report_barrier_form/success.html"


class ReportMarketAccessBarrierFormView(
    mixins.NotFoundOnDisabledFeature,
    NamedUrlSessionWizardView
):

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

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == self.SUMMARY:
            data = self.get_all_cleaned_data()
            context['all_cleaned_data'] = data
        return context

    def serialize_form_list(self, form_list):
        data = {}
        for form in form_list:
            data.update(form.cleaned_data)
        return data

    def done(self, form_list, **kwargs):
        serialized_data = self.serialize_form_list(form_list)
        subject = f"{settings.MARKET_ACCESS_ZENDESK_SUBJECT}: {serialized_data['country']}: {serialized_data['company_name']}"
        action = actions.ZendeskAction(
            email_address=serialized_data['email'],
            full_name=f"{serialized_data['firstname']} {serialized_data['lastname']}",
            subject=subject,
            service_name=settings.MARKET_ACCESS_FORMS_API_ZENDESK_SEVICE_NAME,
            form_url=reverse(
                'report-ma-barrier', kwargs={'step': 'about'}
            )
        )
        response = action.save(serialized_data)
        response.raise_for_status()
        return redirect('report-barrier-form-success')
