from django import forms

from core.widgets import CheckboxWithInlineLabel, RadioSelect


class EmptyForm(forms.Form):
    pass


class SectorForm(forms.Form):
    sector = forms.ChoiceField(
        choices=[
            ('Choice 1', 'Choice 1'),
            ('Choice 2', 'Choice 2'),
        ],
        label='What is your sector?',
        label_suffix='',
    )


class ExportExperienceForm(forms.Form):
    exported_before = forms.TypedChoiceField(
        label='Have you exported before?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect()
    )


class RegularExporterForm(forms.Form):
    regular_exporter = forms.TypedChoiceField(
        label='Is exporting a regular part of your business?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect()
    )


class OnlineMarketplaceForm(forms.Form):
    online_marketplace_user = forms.TypedChoiceField(
        label='Do you use online marketplace to sell your products?',
        label_suffix='',
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect()
    )


class CompanyForm(forms.Form):
    company_name = forms.CharField(
        max_length=1000,
        required=False
    )
    is_sole_trader = forms.BooleanField(
        label='',
        widget=CheckboxWithInlineLabel(
            label='Check here if you are a sole trader'
        ),
        required=False,
    )


class SummaryForm(forms.Form):
    pass

