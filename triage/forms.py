from django import forms

from core.widgets import CheckboxWithInlineLabel, RadioSelect


SECTOR_CHOICES = [
    ('CHOICE_1', 'Choice 1'),
    ('CHOICE_2', 'Choice 2'),
]
REGULAR_EXPORTER = ('REGULAR_EXPORTER', 'Regular Exporter')
OCCASIONAL_EXPORTER = ('OCCASIONAL_EXPORTER', 'Occasional Exporter')
NEW_EXPORTER = ('NEW_EXPORTER', 'New Exporter')


class BaseTriageForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'input-field-container has-error'


class SectorForm(BaseTriageForm):
    sector = forms.ChoiceField(
        choices=SECTOR_CHOICES,
        label='What is your sector?',
        label_suffix='',
    )


class ExportExperienceForm(BaseTriageForm):
    exported_before = forms.TypedChoiceField(
        label='Have you exported before?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect()
    )


class RegularExporterForm(BaseTriageForm):
    regular_exporter = forms.TypedChoiceField(
        label='Is exporting a regular part of your business?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect(),
    )


class OnlineMarketplaceForm(BaseTriageForm):
    used_online_marketplace = forms.TypedChoiceField(
        label='Do you use online marketplace to sell your products?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect()
    )


class CompanyForm(BaseTriageForm):
    company_name = forms.CharField(
        max_length=1000,
        required=False
    )
    sole_trader = forms.BooleanField(
        label='',
        widget=CheckboxWithInlineLabel(
            label='Check here if you are a sole trader'
        ),
        required=False,
    )


class SummaryForm(BaseTriageForm):
    pass


class CompaniesHouseSearchForm(forms.Form):
    term = forms.CharField()


def get_persona(cleaned_data):
    is_regular_exporter = cleaned_data.get('regular_exporter') is True
    has_exported_before = cleaned_data.get('exported_before') is True

    if is_regular_exporter:
        return REGULAR_EXPORTER
    elif not is_regular_exporter and has_exported_before:
        return OCCASIONAL_EXPORTER
    return NEW_EXPORTER


def get_has_exported_before(cleaned_data):
    return cleaned_data.get('exported_before') is True


def get_is_regular_exporter(cleaned_data):
    return cleaned_data.get('regular_exporter') is True


def get_sector_label(cleaned_data):
    for key, label in SECTOR_CHOICES:
        if key == cleaned_data['sector']:
            return label
