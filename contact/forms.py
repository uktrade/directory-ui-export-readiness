from captcha.fields import ReCaptchaField

from django import forms

from core.widgets import CheckboxWithInlineLabel, RadioSelect
from core.fields import PaddedCharField


class FeedbackForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'input-field-container has-error'

    contact_name = forms.CharField(label_suffix='')
    contact_email = forms.EmailField(label_suffix='')
    feedback = forms.CharField(label_suffix='', widget=forms.Textarea)
    captcha = ReCaptchaField()


class YourBusinessForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'input-field-container has-error'

    company_name = forms.CharField(
        label='Company name',
        label_suffix='',
        help_text=(
            "Enter the legal name of your business (not the trading name) "
            "then use 'Search Companies House' and select your company from "
            "the list. It will then prefill your company number and postcode."
        ),
        required=False,
        widget=forms.TextInput(
            attrs={'id': 'js-typeahead-company-name'}
        ),
    )
    company_number = PaddedCharField(
        label='Company number:',
        max_length=8,
        fillchar='0',
        widget=forms.HiddenInput(attrs={'id': 'js-typeahead-company-number'}),
        required=False,
    )
    soletrader = forms.BooleanField(
        label='',
        widget=CheckboxWithInlineLabel(
            label="I don't have a company number",
        ),
        required=False,
    )
    company_postcode = forms.CharField(
        label='Business postcode',
        label_suffix='',
        required=False,
    )
    website_address = forms.URLField(
        label='Company website',
        label_suffix='',
        help_text='Website address, where we can see your products online.',
    )


class BusinessDetailsForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'input-field-container has-error'

    turnover = forms.ChoiceField(
        label='Turnover last year',
        label_suffix='',
        help_text=(
            "You may use 12 months rolling or last year's annual turnover."
        ),
        choices=[
            ('Under 100k', 'Under £100,000'),
            ('100k-500k', '£100,000 to £500,000'),
            ('500k-2m', '£500,001 and £2million'),
            ('2m+', 'More than £2million'),
        ],
        widget=RadioSelect(),
    )
    sku_count = forms.CharField(
        label='How many stock keeping units (SKUs) do you have?',
        label_suffix='',
        help_text=(
            'A stock keeping unit is an individual item, such as a product or '
            'a service that is offered for sale.'
        ),
        widget=forms.NumberInput,
    )
    trademarked = forms.TypedChoiceField(
        label='Are your products trademarked in your target countries?',
        label_suffix='',
        help_text=(
            "Some marketplaces will only sell products that are trademarked."
        ),
        coerce=lambda x: x == 'True',
        choices=[(True, 'Yes'), (False, 'No')],
        widget=RadioSelect(),
    )


class YourExperienceForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'input-field-container has-error'

    experience = forms.ChoiceField(
        label='Have you sold products online to customers outside the UK?',
        label_suffix='',
        choices=[
            ('Not yet', 'Not yet'),
            ('Yes, sometimes', 'Yes, sometimes'),
            ('Yes, regularly', 'Yes, regularly'),
        ],
        widget=RadioSelect(),
    )
    description = forms.CharField(
        label='Pitch your business to this marketplace',
        label_suffix='',
        help_text=(
            "Your pitch is important and the information you provide may be "
            "used to introduce you to the marketplace. You could describe "
            "your business, including your products, your customers and how "
            "you market your products in a few paragraphs."
        ),
        widget=forms.Textarea,
    )


class ContactDetailsForm(forms.Form):
    use_required_attribute = False
    error_css_class = 'input-field-container has-error'

    contact_name = forms.CharField(
        label='Contact name',
        label_suffix='',
    )
    contact_email = forms.CharField(
        label='Email address',
        label_suffix='',
    )
    contact_phone = forms.CharField(
        label='Telephone number',
        label_suffix='',
    )
    email_pref = forms.BooleanField(
        label='',
        widget=CheckboxWithInlineLabel(
            label='I prefer to be contacted by email'
        ),
        required=False,
    )
