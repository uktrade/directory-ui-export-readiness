from captcha.fields import ReCaptchaField
from directory_forms_api_client.forms import ZendeskActionMixin
from directory_components import forms, fields, widgets
from directory_constants.constants import choices, urls
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html

from django.forms import Select, Textarea
from django.utils.html import mark_safe

from contact import constants


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
    ('FOREIGH', 'UK branch of foreign company (BR)'),
    ('OTHER', 'Other'),
)
INDUSTRY_CHOICES = (
    (('', 'Please select'),) + choices.INDUSTRIES + (('OTHER', 'Other'),)
)


anti_phising_validators = [no_html, not_contains_url_or_email]


class NoOpForm(forms.Form):
    pass


class SerializeDataMixin:
    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
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


class DomesticRoutingForm(forms.Form):
    CHOICES = (
        (constants.TRADE_OFFICE, 'Find your local trade office'),
        (constants.EXPORT_ADVICE, 'Advice to export from the UK'),
        (constants.GREAT_SERVICES, 'Great.gov.uk services'),
        (constants.FINANCE, 'Finance'),
        (constants.EUEXIT, 'EU Exit'),
        (constants.EVENTS, 'Events'),
        (constants.DSO, 'Defence and Security Organisation (DSO)'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
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
        (constants.MORE_DETAILS, 'I need more details about the opportunity'),
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


class InternationalRoutingForm(forms.Form):
    CHOICES = (
        (constants.INVESTING, 'Investing in the UK'),
        (constants.BUYING, 'Buying from the UK'),
        (constants.EUEXIT, 'EU Exit'),
        (constants.OTHER, 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class FinanceInfomationChoicesForm(forms.Form):
    CHOICES = (
        ('UPFRONT_FUNDING', 'Securing upfront funding'),
        ('PAYMENT_TERMS', 'Offering competitive but secure payment terms'),
        ('INSURANCE', 'Guidance on export finance and insurance'),

    )
    choices = fields.MultipleChoiceField(
        label_suffix='',
        widget=widgets.CheckboxSelectInlineLabelMultiple(),
        choices=CHOICES,
    )


class FinancePersonalDetailsForm(forms.Form):
    given_name = fields.CharField(
        label='First name',
        validators=anti_phising_validators
    )
    family_name = fields.CharField(
        label='Last name',
        validators=anti_phising_validators
    )
    position = fields.CharField(
        label='Position in organisation',
        validators=anti_phising_validators
    )
    email = fields.EmailField()
    phone = fields.CharField(
        validators=anti_phising_validators
    )


class FinanceBusinessDetailsForm(forms.Form):
    EXPORT_STATUS_CHOICES = [
        ('EXPORT', 'I export outside the UK'),
        ('SUPPLY', 'I supply UK companies that sell overseas'),
        ('NO', 'I don\'t currently export or supply businesses that export'),
    ]

    company_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_CHOICES,
    )
    company_type_other = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = fields.CharField(
        validators=anti_phising_validators
    )
    address_line_one = fields.CharField(
        label='Address and street',
        validators=anti_phising_validators
    )
    address_line_two = fields.CharField(
        label='',
        validators=anti_phising_validators
    )
    city = fields.CharField(
        label='Town or city',
        validators=anti_phising_validators
    )
    postcode = fields.CharField(
        validators=anti_phising_validators
    )
    industry = fields.ChoiceField(
        choices=INDUSTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    export_status = fields.MultipleChoiceField(
        label_suffix='Do you currently export',
        help_text='Select all that apply',
        widget=widgets.CheckboxSelectInlineLabelMultiple(),
        choices=EXPORT_STATUS_CHOICES,
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


class DomesticContactForm(SerializeDataMixin, ZendeskActionMixin, forms.Form):
    given_name = fields.CharField(
        label='First name',
        validators=anti_phising_validators
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
        widget=widgets.RadioSelect(),
        choices=COMPANY_TYPE_OTHER_CHOICES,
        required=False,
    )
    organisation_name = fields.CharField(
        validators=anti_phising_validators
    )
    postcode = fields.CharField(
        validators=anti_phising_validators
    )
    comment = fields.CharField(
        label='Tell us how we can help',
        help_text=(
            'If something is wrong, please give as much details as you can'
        ),
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
        cleaned_data = self.cleaned_data
        return f'{cleaned_data["given_name"]} {cleaned_data["family_name"]}'


class BuyingFromUKContactForm(forms.Form):

    SOURCE_CHOICES = (
        ('', 'Please select'),
        ('OTHER', 'Other'),
    )

    given_name = fields.CharField(
        validators=anti_phising_validators
    )
    family_name = fields.CharField(
        validators=anti_phising_validators
    )
    email = fields.EmailField(label='Email address')
    industry = fields.ChoiceField(
        choices=INDUSTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    organisation_name = fields.CharField(
        validators=anti_phising_validators
    )
    country_name = fields.CharField(
        validators=anti_phising_validators
    )
    comment = fields.CharField(
        widget=Textarea,
        validators=anti_phising_validators
    )
    source = fields.ChoiceField(
        label='Where did you hear about great.gov.uk?',
        choices=SOURCE_CHOICES,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class InternationalContactForm(forms.Form):

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
        validators=anti_phising_validators
    )
    country_name = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
    )
    city = fields.CharField(
        label='City',
        validators=anti_phising_validators
    )
    comment = fields.CharField(
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
