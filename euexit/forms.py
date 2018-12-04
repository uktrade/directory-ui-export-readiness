from captcha.fields import ReCaptchaField
from directory_constants.constants import choices, urls
from directory_components import forms, fields, widgets
from directory_forms_api_client import actions
from directory_validators.common import not_contains_url_or_email
from directory_validators.company import no_html

from django.conf import settings
from django.forms import Select, Textarea
from django.template.loader import render_to_string
from django.utils.html import mark_safe

from euexit.helpers import eu_exit_forms_api_client


COMPANY = 'COMPANY'

COMPANY_CHOICES = (
    (COMPANY, 'Company'),
    ('OTHER', 'Other type of organisation'),
)


TERMS_LABEL = mark_safe(
    'Tick this box to accept the '
    f'<a href="{urls.TERMS_AND_CONDITIONS}" target="_blank">terms and '
    'conditions</a> of the great.gov.uk service.'
)


class FieldsMutationMixin:
    def __init__(self, field_attributes, disclaimer, *args, **kwargs):
        for field_name, field in self.base_fields.items():
            attributes = field_attributes.get(field_name)
            if attributes:
                field.__dict__.update(attributes)
        super().__init__(*args, **kwargs)
        widget = self.fields['terms_agreed'].widget
        widget.label = mark_safe(f'{widget.label}  {disclaimer}')


class SerializeMixin:
    def __init__(self, form_url, ingress_url, subject, *args, **kwargs):
        self.form_url = form_url
        self.ingress_url = ingress_url
        self.subject = subject
        super().__init__(*args, **kwargs)

    @property
    def serialized_data(self):
        data = self.cleaned_data.copy()
        data['form_url'] = self.form_url
        data['ingress_url'] = self.ingress_url
        del data['captcha']
        del data['terms_agreed']
        return data


class EuExitActionMixin:
    """Submit the ticket to the eu-exit zendesk account."""

    def render_email(self, template_name):
        context = {'form_data': self.serialized_data}
        return render_to_string(template_name, context)

    def send_user_email(self):
        action = actions.GovNotifyAction(
            client=eu_exit_forms_api_client,
            template_id=settings.EUEXIT_GOV_NOTIFY_TEMPLATE_ID,
            email_address=self.cleaned_data['email'],
            email_reply_to_id=settings.EUEXIT_GOV_NOTIFY_REPLY_TO_ID,
        )
        response = action.save(self.serialized_data)
        response.raise_for_status()

    def send_agent_email(self):
        action = actions.EmailAction(
            client=eu_exit_forms_api_client,
            recipients=[settings.EUEXIT_AGENT_EMAIL],
            subject=self.subject,
            reply_to=[settings.DEFAULT_FROM_EMAIL],
        )
        text_body = self.render_email('euexit/email-confirmation-agent.txt')
        html_body = self.render_email('euexit/email-confirmation-agent.html')
        response = action.save({
            'text_body': text_body, 'html_body': html_body,
        })
        response.raise_for_status()

    def save(self):
        self.send_agent_email()
        self.send_user_email()


class InternationalContactForm(
    FieldsMutationMixin, SerializeMixin, EuExitActionMixin, forms.Form
):
    first_name = fields.CharField()
    last_name = fields.CharField()
    email = fields.EmailField()
    organisation_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_CHOICES,
    )
    company_name = fields.CharField()
    country = fields.ChoiceField(
        choices=[('', 'Please select')] + choices.COUNTRY_CHOICES,
        widget=Select(attrs={'id': 'js-country-select'}),
    )
    city = fields.CharField()
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


class DomesticContactForm(
    FieldsMutationMixin, SerializeMixin, EuExitActionMixin, forms.Form
):

    first_name = fields.CharField()
    last_name = fields.CharField()
    email = fields.EmailField()
    organisation_type = fields.ChoiceField(
        label_suffix='',
        widget=widgets.RadioSelect(),
        choices=COMPANY_CHOICES
    )
    company_name = fields.CharField()
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
