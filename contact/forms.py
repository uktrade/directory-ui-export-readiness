import abc

from captcha.fields import ReCaptchaField
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
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class ExportOpportunitiesRoutingForm(forms.Form):
    CHOICES = (
        (
            'RESPONSE',
            'I haven\'t had a response from the opportunity I applied for'
        ),
        ('ALERTS', 'My daily alerts are not relevant to me'),
        ('OPPORUNITY', 'I need more details about the opportunity'),
        ('OTHER', 'Other'),
    )
    choice = fields.ChoiceField(
        label='',
        widget=widgets.RadioSelect(),
        choices=CHOICES,
    )


class GreatAccountRoutingForm(forms.Form):
    CHOICES = (
        ('EMAIL_CONFIRMATION', 'I have not received my email confirmation'),
        ('PASSWORD_RESET', 'I need to reset my password'),
        ('COMPANIES_HOUSE_LOGIN', 'My Companies House login is not working'),
        (
            'VERIFICATION_CODE',
            'I do not know where to enter my verification code'
        ),
        (
            'VERIFICATION_LETTER',
            'I have not received my letter containing the verification code'
        ),
        ('OTHER', 'Other'),
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
        validators=[no_html, not_contains_url_or_email]
    )
    family_name = fields.CharField(
        label='Last name',
        validators=[no_html, not_contains_url_or_email]
    )
    position = fields.CharField(
        label='Position in organisation',
        validators=[no_html, not_contains_url_or_email]
    )
    email = fields.EmailField()
    phone = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
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
        validators=[no_html, not_contains_url_or_email]
    )
    address_line_one = fields.CharField(
        label='Address and street',
        validators=[no_html, not_contains_url_or_email]
    )
    address_line_two = fields.CharField(
        label='',
        validators=[no_html, not_contains_url_or_email]
    )
    city = fields.CharField(
        label='Town or city',
        validators=[no_html, not_contains_url_or_email]
    )
    postcode = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
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


class ExportAdviceContactForm(forms.Form):
    comment = fields.CharField(
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
    )


class DomesticContactForm(forms.Form):
    given_name = fields.CharField(
        label='First name',
        validators=[no_html, not_contains_url_or_email]
    )
    family_name = fields.CharField(
        label='Last name',
        validators=[no_html, not_contains_url_or_email]
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
        validators=[no_html, not_contains_url_or_email]
    )
    postcode = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    comment = fields.CharField(
        label='Tell us how we can help',
        help_text=(
            'If something is wrong, please give as much details as you can'
        ),
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )


class BuyingFromUKContactForm(forms.Form):

    SOURCE_CHOICES = (
        ('', 'Please select'),
        ('OTHER', 'Other'),
    )

    given_name = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    family_name = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    email = fields.EmailField(label='Email address')
    industry = fields.ChoiceField(
        choices=INDUSTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    organisation_name = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    country_name = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    comment = fields.CharField(
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
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
        validators=[no_html, not_contains_url_or_email]
    )
    family_name = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    email = fields.EmailField(label='Email address')
    organisation_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=ORGANISATION_TYPE_CHOICES
    )
    organisation_name = fields.CharField(
        validators=[no_html, not_contains_url_or_email]
    )
    country_name = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
    )
    city = fields.CharField(
        label='City',
        validators=[no_html, not_contains_url_or_email]
    )
    comment = fields.CharField(
        widget=Textarea,
        validators=[no_html, not_contains_url_or_email]
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=TERMS_LABEL
    )

