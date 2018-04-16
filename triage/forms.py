from collections import namedtuple
from directory_constants.constants import exred_sector_names
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH

from directory_components.fields import PaddedCharField
from directory_components.fields import ChoiceField
from directory_components.widgets import RadioSelect
from directory_components.widgets import CheckboxWithInlineLabel


Persona = namedtuple('Persona', ['name', 'label'])
REGULAR_EXPORTER = Persona(name='REGULAR_EXPORTER', label='Regular exporter')
OCCASIONAL_EXPORTER = Persona(
    name='OCCASIONAL_EXPORTER', label='Occasional exporter'
)
NEW_EXPORTER = Persona(name='NEW_EXPORTER', label='New exporter')
SECTORS_CHOICES = [
    (v, v + ' ' + l)
    for v, l in exred_sector_names.SECTORS_CHOICES if v.startswith('HS')
]


class BaseTriageForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'form-group-error'


class ExportExperienceForm(BaseTriageForm):
    exported_before = forms.TypedChoiceField(
        label='Have you exported before?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'triage-exported-before'}),
    )


class RegularExporterForm(BaseTriageForm):
    regular_exporter = forms.TypedChoiceField(
        label='Is exporting a regular part of your business activities?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'triage-regular-exporter'}),
        required=False,
        empty_value=None,
    )


class OnlineMarketplaceForm(BaseTriageForm):
    used_online_marketplace = forms.TypedChoiceField(
        label='Do you use online marketplaces to sell your products?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'triage-online-marketplace'}),
        required=False,
        empty_value=None,
    )


class GoodsServicesForm(BaseTriageForm):
    is_exporting_services = forms.BooleanField(
        label='',
        label_suffix='',
        required=False,
        widget=CheckboxWithInlineLabel(
            attrs={'id': 'triage-services'},
            label='Services',
            help_text=(
                'Services are activities such as design consultancy or '
                'financial advice.'),
        )
    )
    is_exporting_goods = forms.BooleanField(
        label='',
        label_suffix='',
        required=False,
        widget=CheckboxWithInlineLabel(
            attrs={'id': 'triage-goods'},
            label='Goods',
            help_text=(
                'Goods are tangible items. They can be raw materials or parts '
                'used to make something, or finished products.'),
        )
    )


class CompanyForm(BaseTriageForm):
    company_name = forms.CharField(
        label='What is your company name? (optional)',
        help_text="We'll use this information to personalise your experience",
        label_suffix='',
        max_length=1000,
        widget=forms.TextInput(
            attrs={
                    'id': 'triage-company-name',
                    'class': 'form-control form-control-3-4'
                }
        ),
        required=False,
    )
    company_number = PaddedCharField(
        label='Company number:',
        max_length=8,
        fillchar='0',
        widget=forms.HiddenInput(attrs={'id': 'triage-company-number'}),
        required=False,
    )

    def clean_company_number(self):
        number = self.cleaned_data['company_number']
        if number == '':
            return None
        return number


class CompaniesHouseForm(BaseTriageForm):
    is_in_companies_house = forms.TypedChoiceField(
        label='Is your company incorporated in the UK?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect(
            use_nice_ids=True,
            attrs={'id': 'triage-is-in-companies-house'}
        ),
        required=False,
        empty_value=None,
    )


class SummaryForm(forms.Form):
    pass


class CompaniesHouseSearchForm(forms.Form):
    term = forms.CharField()


class SectorForm(forms.Form):
    sector = ChoiceField(
        choices=BLANK_CHOICE_DASH + SECTORS_CHOICES,
        label='',
        widget=forms.Select(attrs={'id': 'js-sector-select'}),
    )


def get_sector_label(sector_code):
    for key, label in exred_sector_names.SECTORS_CHOICES:
        if key == sector_code:
            return label


def get_persona(cleaned_data):
    is_regular_exporter = cleaned_data.get('regular_exporter') is True
    has_exported_before = cleaned_data.get('exported_before') is True

    if is_regular_exporter:
        return REGULAR_EXPORTER
    elif not is_regular_exporter and has_exported_before:
        return OCCASIONAL_EXPORTER
    return NEW_EXPORTER


def get_has_exported_before(answers):
    return answers.get('exported_before') is True


def get_is_regular_exporter(answers):
    return answers.get('regular_exporter') is True


def get_is_in_companies_house(answers):
    return answers.get('is_in_companies_house') is True


def get_used_marketplace(answers):
    return answers.get('used_online_marketplace') is True


def serialize_triage_form(data):
    return {
        'exported_before': data['exported_before'],
        'regular_exporter': data.get('regular_exporter'),
        'used_online_marketplace': data.get('used_online_marketplace'),
        'is_exporting_goods': data.get('is_exporting_goods'),
        'is_exporting_services': data.get('is_exporting_services'),
        'company_name': data.get('company_name', ''),
        'company_number': data.get('company_number'),
        'is_in_companies_house': data['is_in_companies_house'],
    }
