from formtools.wizard.views import SessionWizardView

from django.views.generic import TemplateView

from triage import forms


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

    def get_template_names(self):
        return [self.templates[self.steps.current]]
