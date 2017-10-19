from formtools.wizard.views import SessionWizardView

from django.http import JsonResponse
from django.template.response import TemplateResponse
from django.views.generic import View

from triage import forms, helpers


class CompaniesHouseSearchApiView(View):
    form_class = forms.CompaniesHouseSearchForm

    def get(self, request, *args, **kwargs):
        form = self.form_class(data=request.GET)
        if not form.is_valid():
            return JsonResponse(form.errors, status=400)
        api_response = helpers.CompaniesHouseClient.search(
            term=form.cleaned_data['term']
        )
        api_response.raise_for_status()
        return JsonResponse(api_response.json()['items'], safe=False)


class TriageWizardFormView(SessionWizardView):

    SECTOR = 'SECTOR'
    EXPORTED_BEFORE = 'EXPORTED_BEFORE'
    REGULAR_EXPORTER = 'REGULAR_EXPORTER'
    ONLINE_MARKETPLACE = 'ONLINE_MARKETPLACE'
    COMPANY = 'COMPANY'
    SUMMARY = 'SUMMARY'

    form_list = (
        (SECTOR, forms.SectorForm),
        (EXPORTED_BEFORE, forms.ExportExperienceForm),
        (REGULAR_EXPORTER, forms.RegularExporterForm),
        (ONLINE_MARKETPLACE, forms.OnlineMarketplaceForm),
        (COMPANY, forms.CompanyForm),
        (SUMMARY, forms.SummaryForm),
    )
    templates = {
        SECTOR: 'triage/wizard-step-sector.html',
        EXPORTED_BEFORE: 'triage/wizard-step-exported-before.html',
        REGULAR_EXPORTER: 'triage/wizard-step-regular-exporter.html',
        ONLINE_MARKETPLACE: 'triage/wizard-step-online-marketplace.html',
        COMPANY: 'triage/wizard-step-company.html',
        SUMMARY: 'triage/wizard-step-summary.html',
    }

    def process_step(self, form):
        if self.steps.current == self.REGULAR_EXPORTER:
            is_regular = forms.get_is_regular_exporter(form.cleaned_data)
            self.condition_dict[self.ONLINE_MARKETPLACE] = not is_regular
        elif self.steps.current == self.EXPORTED_BEFORE:
            has_exported = forms.get_has_exported_before(form.cleaned_data)
            self.condition_dict[self.ONLINE_MARKETPLACE] = has_exported
            self.condition_dict[self.REGULAR_EXPORTER] = has_exported
        return super().process_step(form)

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == self.SUMMARY:
            all_cleaned_data = self.get_all_cleaned_data()
            context['all_cleaned_data'] = all_cleaned_data
            context['sector_label'] = forms.get_sector_label(all_cleaned_data)
            context['persona'] = forms.get_persona(all_cleaned_data)[1]
        return context

    def done(self, *args, **kwargs):
        answer_manager = helpers.TriageAnswersManager(self.request)
        answer_manager.persist_answers(self.get_all_cleaned_data())
        return TemplateResponse(self.request, 'triage/wizard-step-done.html')
