from directory_constants.constants import choices
from directory_components import forms, fields, widgets
from django.utils.safestring import mark_safe

from django.forms import Select, Textarea


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

    def change_country_tuples(country_list):
        return [
            (country_name, country_name)
            for country_code, country_name in country_list
        ]

    error_css_class = 'input-field-container has-error'
    # Country choices is a list of tuples that follow the structure
    # (country_code, country_name). We don't want this
    # structure because the choice needs to always be human
    # readable for the summary and zendesk. This creates a new
    # tuple that makes tuples with the same value.

    product_service = fields.CharField(
        label='What is the product or service you want to export?')
    country = fields.ChoiceField(
        label='Which country are you trying to export to?',
        choices=[('', 'Select a country')] +
        change_country_tuples(choices.COUNTRY_CHOICES),
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    problem_summary = fields.CharField(
        label=mark_safe(
            '<p>Provide a brief description of the problem, including: </p> \
            <ul class="list list-bullet"> \
              <li>what is affecting your export</li> \
              <li>when it started</li> \
              <li>if it’s a one off</li> \
              <li>any correspondence you have received about the problem</li> \
            </ul>'),
        widget=Textarea,
    )
    impact = fields.CharField(
        label='If the problem has ended, what was the impact?',
        widget=Textarea,
    )
    resolve_summary = fields.CharField(
        label=mark_safe(
            '<p>Tell us about any steps you have taken to resolve the problem, \
            including: </p> \
            <ul class="list list-bullet"> \
              <li>people you have contacted</li> \
              <li>when you contacted them</li> \
              <li>what happened</li> \
            </ul>'),
        widget=Textarea,
    )
    eu_exit_related = fields.ChoiceField(
        label='Is this issue caused by or related to EU Exit?',
        widget=widgets.RadioSelect(
            use_nice_ids=True, attrs={'id': 'radio-one'}
        ),
        choices=(
            (True, 'Yes'),
            (False, 'No')
        )
    )


class OtherDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    other_details = fields.CharField(
        label='Is there anything else you would like \
            us to understand about the situation?',
        widget=Textarea,
    )


class SummaryForm(forms.Form):
    pass
