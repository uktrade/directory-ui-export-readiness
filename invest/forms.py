from directory_components import forms, fields, widgets
from directory_constants.constants import choices, urls

from django.forms import Textarea
from django.utils.safestring import mark_safe


class HighPotentialOpportunityForm(forms.Form):
    def __init__(self, field_attributes={}, *args, **kwargs):
        for field_name, attributes in field_attributes.items():
            self.base_fields[field_name].__dict__.update(attributes)
        return super().__init__(*args, **kwargs)

    full_name = fields.CharField()
    role_in_company = fields.CharField()
    email_address = fields.EmailField()
    phone_number = fields.CharField()
    company_name = fields.CharField()
    website_url = fields.URLField(required=False)
    country = fields.CharField()
    company_size = fields.ChoiceField(
        choices=choices.EMPLOYEES
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
