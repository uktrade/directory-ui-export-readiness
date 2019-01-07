from directory_constants.constants import choices
from directory_components import forms, fields, widgets

from django.forms import Select, Textarea, ValidationError


class AboutForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    CATEGORY_CHOICES = (
        'I\'m an exporter / seeking to export',
        'I work for a trade association',
    )

    firstname = fields.CharField(label='First name')
    lastname = fields.CharField(label='Last name')
    jobtitle = fields.CharField(label='Job title')
    categories = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(
            attrs={'id': 'checkbox-single'},
            use_nice_ids=True,
        ),
        choices=((choice, choice) for choice in CATEGORY_CHOICES)
    )
    company_name = fields.CharField(label='Business name')
    email = fields.EmailField(label='Email address')
    phone = fields.CharField(label='Telephone number')


class ProblemDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    product_service = fields.CharField(
        label='What is the product or service you want to export?')
    country = fields.ChoiceField(
        label='Which country are you trying to export to?',
        choices=[('', 'Select a country')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    problem_summary = fields.CharField(
        label='Provide a brief description of the problem',
        widget=Textarea,
    )
    impact = fields.CharField(
        label='If the problem has ended, what was the impact?',
        widget=Textarea,
    )
    resolve_summary = fields.CharField(
        label='Tell us about any steps you have taken to resolve the problem',
        widget=Textarea,
    )
    eu_exit_related = fields.ChoiceField(
        label='Is this issue caused by or related to EU Exit?',
        widget=widgets.RadioSelect(
            use_nice_ids=True, attrs={'id': 'radio-one'}
        ),
        choices=((True, 'Yes'), (False, 'No'),
                 )
    )


class OtherDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    other_details = fields.CharField(
        label='Is there anything else you would like us to understand about the situation?',
        widget=Textarea,
    )


class SummaryForm(forms.Form):
    pass
