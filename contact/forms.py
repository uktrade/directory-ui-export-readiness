from captcha.fields import ReCaptchaField
from directory_forms_api_client.forms import (
    GovNotifyActionMixin, ZendeskActionMixin
)
from directory_components import forms, fields, widgets
from directory_constants.constants import choices, urls
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html
import requests.exceptions

from django.conf import settings
from django.forms import Textarea, TextInput
from django.utils.html import mark_safe

from contact import constants, helpers


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    '<a href="{url}" target="_blank">terms and '
    'conditions</a> of the great.gov.uk service.'.format(
        url=urls.INFO_TERMS_AND_CONDITIONS)
)

COMPANY_TYPE_CHOICES = (
    ('LIMITED', 'UK private or public limited company'),
    ('OTHER', 'Other type of UK organisation'),
)
COMPANY_TYPE_OTHER_CHOICES = (
    ('CHARITY', 'Charity'),
    ('GOVERNMENT_DEPARTMENT', 'Government department'),
    ('INTERMEDIARY', 'Intermediary'),
    ('LIMITED_PARTNERSHIP', 'Limited partnership'),
    ('SOLE_TRADER', 'Sole Trader'),
    ('FOREIGH', 'UK branch of foreign company'),
    ('OTHER', 'Other'),
)
INDUSTRY_CHOICES = (
    (('', 'Please select'),) + choices.INDUSTRIES + (('OTHER', 'Other'),)
)

anti_phising_validators = [no_html, not_contains_url_or_email]


class EuExitOptionFeatureFlagMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not settings.FEATURE_FLAGS['EU_EXIT_FORMS_ON']:
            self.fields['choice'].choices = [
                (value, label) for value, label in self.CHOICES
                if value != constants.EUEXIT
            ]


class NoOpForm(forms.Form):
    pass


class SerializeDataMixin:

    def __init__(self, form_url, ingress_url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_url = form_url
        self.ingress_url = ingress_url

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        data['form_url'] = self.form_url
        data['ingress_url'] = self.ingress_url or ''
        del data['captcha']
        del data['terms_agreed']
        return data


class LocationRoutingForm(forms.Form):
    CHOICES = (
        (constants.DOMESTIC, 'The UK'),
        (constants.INTERNATIONAL, 'Outside the UK'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class DomesticRoutingForm(EuExitOptionFeatureFlagMixin, forms.Form):

    CHOICES = (
        (constants.TRADE_OFFICE, 'Find your local trade office'),
        (constants.EXPORT_ADVICE, 'Advice to export from the UK'),
        (
            constants.GREAT_SERVICES,
            'great.gov.uk account and services support'
        ),
        (constants.FINANCE, 'UK Export Finance (UKEF)'),
        (constants.EUEXIT, 'EU exit'),  # possibly removed by mixin
        (constants.EVENTS, 'Events'),
        (constants.DSO, 'Defence and Security Organisation (DSO)'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,  # possibly update by mixin
    )


class GreatServicesRoutingForm(forms.Form):

    CHOICES = (
        (constants.EXPORT_OPPORTUNITIES, 'Export opportunities service'),
        (constants.GREAT_ACCOUNT, 'Your account on great.gov.uk'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class ExportOpportunitiesRoutingForm(forms.Form):
    CHOICES = (
        (
            constants.NO_RESPONSE,
            'I haven\'t had a response from the opportunity I applied for'
        ),
        (constants.ALERTS, 'My daily alerts are not relevant to me'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class GreatAccountRoutingForm(forms.Form):
    CHOICES = (
        (
            constants.NO_VERIFICATION_EMAIL,
            'I have not received my email confirmation'
        ),
        (constants.PASSWORD_RESET, 'I need to reset my password'),
        (
            constants.COMPANIES_HOUSE_LOGIN,
            'My Companies House login is not working'
        ),
        (
            constants.VERIFICATION_CODE,
            'I do not know where to enter my verification code'
        ),
        (
            constants.NO_VERIFICATION_LETTER,
            'I have not received my letter containing the verification code'
        ),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class InternationalRoutingForm(EuExitOptionFeatureFlagMixin, forms.Form):
    CHOICES = (
        (constants.INVESTING, 'Investing in the UK'),
        (constants.BUYING, 'Buying from the UK'),
        (constants.EUEXIT, 'EU exit'),  # possibly removed by mixin
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,  # possibly updated by mixin
    )


class FeedbackForm(SerializeDataMixin, ZendeskActionMixin, forms.Form):
    name = fields.CharField(
        validators=anti_phising_validators
    )
    email = fields.EmailField()
    comment = fields.CharField(
        label='Feedback',
        widget=Textarea,
        validators=anti_phising_validators
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )

    @property
    def full_name(self):
        assert self.is_valid()
        return self.cleaned_data['name']


class BaseShortForm(forms.Form):
    comment = fields.CharField(
        label=(
            'If something is wrong, please give as much details as you can'
        ),
        widget=Textarea,
        validators=anti_phising_validators
    )
    given_name = fields.CharField(
        label='First name',
        validators=anti_phising_validators,
    )
    family_name = fields.CharField(
        label='Last name',
        validators=anti_phising_validators
    )
    email = fields.EmailField()
    company_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    company_type_other = fields.ChoiceField(
        label_suffix='',
        choices=COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = fields.CharField(
        validators=anti_phising_validators
    )
    postcode = fields.CharField(
        validators=anti_phising_validators
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class ShortNotifyForm(SerializeDataMixin, GovNotifyActionMixin, BaseShortForm):

    @property
    def serialized_data(self):
        data = super().serialized_data
        try:
            details = helpers.retrieve_regional_office(data['postcode'])
        except requests.exceptions.RequestException:
            # post code may be incorrect or a server error may have occurred.
            # Set empty as GovUK notify errors if any variables are missing.
            data['dit_regional_office_name'] = ''
            data['dit_regional_office_email'] = ''
        else:
            data['dit_regional_office_name'] = details['name']
            data['dit_regional_office_email'] = details['email']
        return data


class ShortZendeskForm(SerializeDataMixin, ZendeskActionMixin, BaseShortForm):

    @property
    def full_name(self):
        assert self.is_valid()
        cleaned_data = self.cleaned_data
        return f'{cleaned_data["given_name"]} {cleaned_data["family_name"]}'


class InternationalContactForm(
    SerializeDataMixin, GovNotifyActionMixin, forms.Form
):

    ORGANISATION_TYPE_CHOICES = (
        ('COMPANY', 'Company'),
        ('OTHER', 'Other type of organisation'),
    )

    given_name = fields.CharField(
        validators=anti_phising_validators
    )
    family_name = fields.CharField(
        validators=anti_phising_validators
    )
    email = fields.EmailField(label='Email address')
    organisation_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=ORGANISATION_TYPE_CHOICES
    )
    organisation_name = fields.CharField(
        label='Your organisation name',
        validators=anti_phising_validators,
    )
    country_name = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
    )
    city = fields.CharField(
        label='City',
        validators=anti_phising_validators
    )
    comment = fields.CharField(
        label='Tell us how we can help',
        widget=Textarea,
        validators=anti_phising_validators
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class CommentForm(forms.Form):
    comment = fields.CharField(
        label='',
        widget=Textarea,
        validators=anti_phising_validators
    )


class PersonalDetailsForm(forms.Form):

    first_name = fields.CharField(label='First name')
    last_name = fields.CharField(label='Last name')
    position = fields.CharField(label='Position in organisation')
    email = fields.EmailField(label='Email address')
    phone = fields.CharField(label='Phone')


class BusinessDetailsForm(forms.Form):
    TURNOVER_OPTIONS = (
        ('', 'Please select'),
        ('0-25k', 'under £25,000'),
        ('25k-100k', '£25,000 - £100,000'),
        ('100k-1m', '£100,000 - £1,000,000'),
        ('1m-5m', '£1,000,000 - £5,000,000'),
        ('5m-25m', '£5,000,000 - £25,000,000'),
        ('25m-50m', '£25,000,000 - £50,000,000'),
        ('50m+', '£50,000,000+')
    )

    company_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    companies_house_number = fields.CharField(
        label='Companies House number',
        required=False,
    )
    company_type_other = fields.ChoiceField(
        label_suffix='',
        choices=(('', 'Please select'),) + COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = fields.CharField(
        validators=anti_phising_validators
    )
    postcode = fields.CharField(
        validators=anti_phising_validators
    )
    industry = fields.ChoiceField(
        choices=INDUSTRY_CHOICES,
    )
    industry_other = fields.CharField(
        label='Type in your industry',
        widget=TextInput(attrs={'class': 'js-field-other'}),
        required=False,
    )
    turnover = fields.ChoiceField(
        label='Annual turnover (optional)',
        choices=TURNOVER_OPTIONS,
    )
    employees = fields.ChoiceField(
        label='Number of employees (optional)',
        choices=(('', 'Please select'),) + choices.EMPLOYEES,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )
