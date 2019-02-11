from directory_constants.constants import choices
from directory_components import forms, fields, widgets
from django.utils.safestring import mark_safe
from django.shortcuts import redirect

from django.forms import Select, Textarea, TextInput, ValidationError

class CurrentStatusForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    STATUS_CHOICES = (
        (1, 'My perishable goods or livestock are blocked in transit'),
        (2, 'I’m at immediate risk of missing a commercial opportunity'),
        (3, 'I’m at immediate risk of not fulfilling a contract'),
        (4, 'I need resolution quickly, but  I’m not at immediate risk of loss'),
    )

    status = fields.ChoiceField(
        label='Select which option best applies to you',
        widget=widgets.RadioSelect(
            use_nice_ids=True, attrs={'id': 'radio-one'}
        ),
        choices=((choice_code, choice) for choice_code, choice in STATUS_CHOICES)
    )

    def __init__(self, *args, **kwargs):
        super(CurrentStatusForm, self).__init__(*args, **kwargs)

        self.fields['status'].error_messages = {'required': 'Choose which option best describes your situation'}


class AboutForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    CATEGORY_CHOICES = (
        'I’m an exporter or I want to export',
        'I work for a trade association',
        'Other'
    )

    firstname = fields.CharField(label='First name')
    lastname = fields.CharField(label='Last name')
    jobtitle = fields.CharField(label='Job title')
    categories = fields.ChoiceField(
        label='Business type',
        widget=widgets.RadioSelect(
            attrs={'id': 'checkbox-single'},
            use_nice_ids=True,
        ),
        choices=((choice, choice) for choice in CATEGORY_CHOICES)
    )
    organisation_description = fields.CharField(
        label='Tell us about your organisation', 
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False
    )
    company_name = fields.CharField(label='Business or organisation name')
    email = fields.EmailField(label='Email address')
    phone = fields.CharField(label='Telephone number')

    def __init__(self, *args, **kwargs):
        super(AboutForm, self).__init__(*args, **kwargs)
        
        for field in self.fields.values():
            field.error_messages = {'required':'Enter your {fieldname}'.format(fieldname=field.label)}
        
        self.fields['categories'].error_messages = {'required': 'Tell us your business type'}


class ProblemDetailsForm(forms.Form):

    # Country choices is a list of tuples that follow the structure
    # (country_code, country_name). We don't want this
    # structure because the choice needs to always be human
    # readable for the summary and zendesk. This creates a new
    # tuple that makes tuples with the same value.
    def change_country_tuples(country_list):
        return [
            (country_name, country_name)
            for country_code, country_name in country_list
        ]

    error_css_class = 'input-field-container has-error'

    product_service = fields.CharField(
        label='What goods or services do you want to export?',
        help_text='Or tell us about an investment you want to make'
    )
    country = fields.ChoiceField(
        label='Which country do you want to export to?',
        choices=[('', 'Select a country')] +
        change_country_tuples(choices.COUNTRY_CHOICES),
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    problem_summary = fields.CharField(
        label=mark_safe(
            '<p>Tell us about your problem, including: </p> \
            <ul class="list list-bullet"> \
              <li>what’s affecting to your export or investment</li> \
              <li>when you became aware of the problem</li> \
              <li>how you came aware of the problem</li> \
              <li>if it’s a one off</li> \
              <li>any information you’ve been given or correspondence you’ve had</li> \
              <li>the HS (Harmonized System) code for your goods, if you know it</li> \
            </ul>'),
        widget=Textarea,
    )
    impact = fields.CharField(
        label='How has the problem affected your business?',
        widget=Textarea
    )
    resolve_summary = fields.CharField(
        label=mark_safe(
            '<p>Tell us about any steps you’ve taken to resolve the problem, including: </p> \
            <ul class="list list-bullet"> \
              <li>people you’ve contacted</li> \
              <li>when you contacted them</li> \
              <li>what happened</li> \
            </ul>'),
        widget=Textarea
    )
    eu_exit_related = fields.ChoiceField(
        label='Is your problem caused by or related to EU Exit?',
        widget=widgets.RadioSelect(
            use_nice_ids=True, attrs={'id': 'radio-one'}
        ),
        choices=(
            (True, 'Yes'),
            (False, 'No')
        )
    )

    def __init__(self, *args, **kwargs):
        super(ProblemDetailsForm, self).__init__(*args, **kwargs)

        required_error_messages = {
            'product_service': 'Tell us what you’re trying to export or invest in',
            'country': 'Select the country you’re trying to export to',
            'problem_summary': 'Tell us about the barrier you’re facing',
            'impact': 'Tell us how your business is being affected by the barrier',
            'resolve_summary': 'Tell us what you’ve done to resolve your problem, even if this is your first step',
            'eu_exit_related': 'Tell us if your problem related to EU Exit'
        }

        for field_name in required_error_messages:
            self.fields[field_name].error_messages = {'required': required_error_messages[field_name]}


class OtherDetailsForm(forms.Form):
    error_css_class = 'input-field-container has-error'
    other_details = fields.CharField(
        label='Do you want to tell us anything else about your problem? (optional)',
        widget=Textarea,
        required=False
    )


class SummaryForm(forms.Form):
    pass
