from captcha.fields import ReCaptchaField
from directory_constants.constants import choices, urls
from directory_components import forms, fields, widgets

from django.forms import Select, Textarea
from django.utils.html import mark_safe


class InternationalContactForm(forms.Form):
    first_name = fields.CharField(label='Given name')
    last_name = fields.CharField(label='Family name')
    email = fields.EmailField()
    organisation_type = fields.ChoiceField(
        label='Organisation type',
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=(
            ('COMPANY', 'Company'),
            ('OTHER', 'Other type of organisation'),
        )
    )
    company_name = fields.CharField()
    country = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    city = fields.CharField()
    comment = fields.CharField(
        label='Your question',
        widget=Textarea,
    )
    captcha = ReCaptchaField(
        label='',
        label_suffix='',
    )
    terms_agreed = fields.BooleanField(
        label=mark_safe(
            'Tick this box to accept the '
            '<a href="{url}" target="_blank">terms and '
            'conditions</a> of the great.gov.uk service.'.format(
                url=urls.INFO_TERMS_AND_CONDITIONS)
        )
    )
