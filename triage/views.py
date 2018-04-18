from formtools.wizard.views import NamedUrlSessionWizardView
from directory_constants.constants.exred_sector_names import CODES_SECTORS_DICT

from django.core.urlresolvers import reverse_lazy
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.functional import cached_property
from django.views.generic import TemplateView
from django.views.generic import View
from django.views.generic.edit import FormView

from article import structure
from casestudy import casestudies
from core.views import ArticlesViewedManagerMixin
from triage import forms, helpers
from triage.helpers import TriageAnswersManager


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


class TriageWizardFormView(NamedUrlSessionWizardView):

    EXPORTED_BEFORE = 'exported-before'
    REGULAR_EXPORTER = 'regular-exporter'
    ONLINE_MARKETPLACE = 'online-marketplace'
    GOODS_SERVICES = 'goods-services'
    COMPANY = 'company'
    COMPANIES_HOUSE = 'companies-house'
    SUMMARY = 'summary'

    form_list = (
        (EXPORTED_BEFORE, forms.ExportExperienceForm),
        (REGULAR_EXPORTER, forms.RegularExporterForm),
        (ONLINE_MARKETPLACE, forms.OnlineMarketplaceForm),
        (GOODS_SERVICES, forms.GoodsServicesForm),
        (COMPANIES_HOUSE, forms.CompaniesHouseForm),
        (COMPANY, forms.CompanyForm),
        (SUMMARY, forms.SummaryForm),
    )
    templates = {
        EXPORTED_BEFORE: 'triage/wizard-step-exported-before.html',
        REGULAR_EXPORTER: 'triage/wizard-step-regular-exporter.html',
        ONLINE_MARKETPLACE: 'triage/wizard-step-online-marketplace.html',
        GOODS_SERVICES: 'triage/wizard-step-goods-services.html',
        COMPANIES_HOUSE: 'triage/wizard-step-sole-trader.html',
        COMPANY: 'triage/wizard-step-company.html',
        SUMMARY: 'triage/wizard-step-summary.html',
    }
    success_url = reverse_lazy('custom-page')

    def should_show_online_marketplace(self):
        export_data = self.get_cleaned_data_for_step(self.EXPORTED_BEFORE)
        regular_data = self.get_cleaned_data_for_step(self.REGULAR_EXPORTER)
        has_exported_before = forms.get_has_exported_before(export_data or {})
        is_regular_exporter = forms.get_is_regular_exporter(regular_data or {})
        return has_exported_before and not is_regular_exporter

    def should_show_regular_exporter(self):
        data = self.get_cleaned_data_for_step(self.EXPORTED_BEFORE)
        return forms.get_has_exported_before(data or {})

    def should_show_company(self):
        data = self.get_cleaned_data_for_step(self.COMPANIES_HOUSE)
        is_in_companies_house = forms.get_is_in_companies_house(data or {})
        return is_in_companies_house

    condition_dict = {
        ONLINE_MARKETPLACE: should_show_online_marketplace,
        REGULAR_EXPORTER: should_show_regular_exporter,
        COMPANY: should_show_company,
    }

    @cached_property
    def persisted_triage_answers(self):
        answer_manager = helpers.TriageAnswersManager(self.request)
        return answer_manager.retrieve_answers()

    def get_form_initial(self, step):
        return self.persisted_triage_answers

    def process_step(self, form):
        if self.is_user_skipping_current_step:
            return {}
        if self.steps.current == self.COMPANIES_HOUSE:
            if not forms.get_is_in_companies_house(form.cleaned_data):
                self.storage.set_step_data(self.COMPANY, {})
        return super().process_step(form)

    def render_next_step(self, form):
        if self.steps.current == self.COMPANY:
            if self.is_user_skipping_current_step:
                self.storage.set_step_data(self.COMPANY, {})
                return self.render_goto_step(self.SUMMARY)
        return super().render_next_step(form)

    def get_template_names(self):
        return [self.templates[self.steps.current]]

    @property
    def is_user_reviewing_persisted_answers(self):
        # on the custom page there is a link to "change your preferences". That
        # link includes '?result' in the querystring. This indicates that the
        # user should be sent to the last step in the wizard to review their
        # answers
        return 'result' in self.request.GET

    @property
    def is_user_skipping_current_step(self):
        return 'wizard_skip_step' in self.request.POST

    def get(self, *args, **kwargs):
        if self.is_user_reviewing_persisted_answers:
            for form_key in self.form_list:
                initial_data = {
                    self.get_form_prefix(step=form_key) + '-' + key: [value]
                    for key, value in self.persisted_triage_answers.items()
                }
                self.storage.set_step_data(form_key, initial_data)
            return self.render_goto_step(self.SUMMARY)
        return super().get(*args, **kwargs)

    def render_done(self, form, **kwargs):
        if self.is_user_reviewing_persisted_answers:
            return redirect(self.success_url)
        return super().render_done(form, **kwargs)

    def render(self, form=None, **kwargs):
        """If summary is called without data, redirect to exported_before."""
        data = self.get_all_cleaned_data()
        if self.steps.current == self.SUMMARY and not data:
            return self.render_goto_step(self.EXPORTED_BEFORE)
        return super().render(form, **kwargs)

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form=form, **kwargs)
        if self.steps.current == self.SUMMARY:
            data = self.get_all_cleaned_data()
            context['all_cleaned_data'] = data
            context['persona'] = forms.get_persona(data)
            context['is_updating_answers'] = (
                self.persisted_triage_answers != {}
            )
        return context

    def done(self, *args, **kwargs):
        completed_triage = self.persisted_triage_answers != {}
        if completed_triage and self.persisted_triage_answers['sector']:
            sector = {'sector': self.persisted_triage_answers['sector']}
        else:
            sector = {'sector': None}
        answers = forms.serialize_triage_form(self.get_all_cleaned_data())
        answers.update(sector)
        answer_manager = helpers.TriageAnswersManager(self.request)
        answer_manager.persist_answers(answers)
        return redirect(self.success_url)


class TriageStartPageView(TemplateView):
    template_name = 'triage/start-now.html'


class CustomPageView(ArticlesViewedManagerMixin, FormView):
    template_name = 'triage/custom-page.html'
    success_url = reverse_lazy('custom-page')
    form_class = forms.SectorForm

    @cached_property
    def triage_answers(self):
        answer_manager = helpers.TriageAnswersManager(self.request)
        return answer_manager.retrieve_answers()

    def update_triage_sector(self, request, answers, form):
        answers.update(form.cleaned_data)
        answer_manager = TriageAnswersManager(request)
        answer_manager.persist_answers(answers)

    def form_valid(self, form):
        self.update_triage_sector(self.request, self.triage_answers, form)
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if not self.triage_answers:
            return redirect('triage-start')
        # for people with a session state from before the new custom page
        # with the sector dropdown was released
        if not self.triage_answers.get('sector'):
            self.triage_answers['sector'] = None

        if self.triage_answers['sector'] is not None:
            initial_sector = self.triage_answers['sector']
            self.initial = {'sector': initial_sector}

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['persona'] = forms.get_persona(self.triage_answers)
        context['triage_result'] = self.triage_answers
        # for people who selected a service category before the sector
        # question was removed from triage
        context['service_sector'] = self.triage_answers[
            'sector'] and self.triage_answers['sector'].startswith('EB')
        context['section_configuration'] = self.get_section_configuration()
        context['article_group'] = self.article_group
        context['casestudies'] = [
            casestudies.MARKETPLACE,
            casestudies.HELLO_BABY,
            casestudies.YORK,
        ]
        context['article_group_read_progress'] = (
            self.article_read_manager.get_view_progress_for_groups()
        )
        context['sector_label'] = forms.get_sector_label(
            self.triage_answers['sector'])
        context['sector_code'] = self.triage_answers['sector']

        if self.triage_answers[
             'sector'] and self.triage_answers['sector'].startswith('HS'):
            sector_code = self.triage_answers['sector']
            context['top_markets'] = helpers.get_top_markets(sector_code)[:10]
            context['sector_name'] = CODES_SECTORS_DICT[sector_code]
            context['top_importer'] = helpers.get_top_importer(sector_code)
        return context

    @property
    def article_group(self):
        answers = self.triage_answers
        persona = forms.get_persona(answers)
        if persona == forms.NEW_EXPORTER:
            return structure.CUSTOM_PAGE_NEW_ARTICLES
        elif persona == forms.OCCASIONAL_EXPORTER:
            return structure.CUSTOM_PAGE_OCCASIONAL_ARTICLES
        return structure.CUSTOM_PAGE_REGULAR_ARTICLES

    def get_section_configuration(self):
        answers = self.triage_answers
        persona = forms.get_persona(answers)
        if persona == forms.NEW_EXPORTER:
            return self.get_persona_new_section_configuration(answers)
        elif persona == forms.OCCASIONAL_EXPORTER:
            return self.get_persona_occasional_section_configuration(answers)
        elif persona == forms.REGULAR_EXPORTER:
            return self.get_persona_regular_section_configuration(answers)

    def get_persona_new_section_configuration(self, answers):
        return {
            'persona_article_group': self.article_group,
            'trade_profile': forms.get_is_in_companies_house(answers),
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        }

    def get_persona_occasional_section_configuration(self, answers):
        return {
            'persona_article_group': self.article_group,
            'trade_profile': forms.get_is_in_companies_house(answers),
            'selling_online_overseas': forms.get_used_marketplace(answers),
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        }

    @staticmethod
    def get_persona_regular_section_configuration(answers):
        return {
            'persona_article_group': [],
            'trade_profile': forms.get_is_in_companies_house(answers),
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': True,
            'articles_resources': True,
            'case_studies': False,
        }
