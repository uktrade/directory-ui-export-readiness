from directory_components import forms, fields, widgets
from directory_constants.constants import choices, urls
from directory_forms_api_client.forms import GovNotifyActionMixin

from django.forms import Select, Textarea
from django.utils.safestring import mark_safe


class HighPotentialOpportunityForm(GovNotifyActionMixin, forms.Form):
    COMPANY_SIZE_CHOICES = [
        ('1 - 10', '1 - 10'),
        ('11 - 50', '11 - 50'),
        ('51 - 250', '51 - 250'),
        ('250+', '250+'),
    ]

    def __init__(
        self, field_attributes, opportunity_choices, *args, **kwargs
    ):
        for field_name, field in self.base_fields.items():
            attributes = field_attributes.get(field_name)
            if attributes:
                field.__dict__.update(attributes)
        self.base_fields['opportunities'].choices = opportunity_choices
        return super().__init__(*args, **kwargs)

    full_name = fields.CharField()
    role_in_company = fields.CharField()
    email_address = fields.EmailField()
    phone_number = fields.CharField()
    company_name = fields.CharField()
    website_url = fields.CharField(required=False)
    country = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    company_size = fields.ChoiceField(
        choices=COMPANY_SIZE_CHOICES
    )
    opportunities = fields.MultipleChoiceField(
        widget=widgets.CheckboxSelectInlineLabelMultiple(
            attrs={'id': 'checkbox-multiple'},
            use_nice_ids=True,
        ),
        choices=[]  # set in __init__
    )
    comment = fields.CharField(
        widget=Textarea,
    )
    terms_agreed = fields.BooleanField(
        label=mark_safe(
            'Tick this box to accept the '
            '<a href="{url}" target="_blank">terms and '
            'conditions</a> of the great.gov.uk service.'.format(
                url=urls.INFO_TERMS_AND_CONDITIONS)
        )
    )

    @property
    def serialized_data(self):
        return {
            **self.cleaned_data,
            'opportunity_urls': '\n'.join(self.cleaned_data['opportunities']),
        }
