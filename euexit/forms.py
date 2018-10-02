from captcha.fields import ReCaptchaField
from directory_constants.constants import choices, urls
from directory_components import forms, fields, widgets

from django.forms import Select, Textarea
from django.utils.html import mark_safe


class InternationalContactForm(forms.Form):
    def __init__(self, field_attributes, *args, **kwargs):
        for field_name, field in self.base_fields.items():
            attributes = field_attributes.get(field_name)
            if attributes:
                field.__dict__.update(attributes)
        return super().__init__(*args, **kwargs)

    first_name = fields.CharField()
    last_name = fields.CharField()
    email = fields.EmailField()
    organisation_type = fields.ChoiceField(
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
