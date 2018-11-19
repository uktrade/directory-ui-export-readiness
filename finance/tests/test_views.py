from unittest.mock import call, patch

import pytest

from django.urls import reverse

from core.tests.helpers import create_response
from finance import forms, views


@pytest.mark.parametrize(
    'step',
    ('contact', 'your-details', 'company-details', 'help')
)
def test_ukef_lead_generation_feature_flag_on(client, settings, step):
    settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON'] = True
    url = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': step}
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.GetFinanceLeadGenerationFormView.templates[step]
    ]


@patch('captcha.fields.ReCaptchaField.clean')
@patch('finance.views.PardotAction')
def test_ukef_lead_generation_captcha_revalidation(
    mock_action, mock_clean, client, settings, captcha_stub
):
    settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON'] = True

    url_name = 'uk-export-finance-lead-generation-form'
    view_name = 'get_finance_lead_generation_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'contact'}),
        {
            view_name + '-current_step': 'contact',
            'contact-categories': 'Securing upfront funding',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'your-details'}),
        {
            view_name + '-current_step': 'your-details',
            'your-details-firstname': 'test',
            'your-details-lastname': 'test',
            'your-details-position': 'test',
            'your-details-email': 'test@example.com',
            'your-details-phone': 'test',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'company-details'}),
        {
            view_name + '-current_step': 'company-details',
            'company-details-trading_name': 'test',
            'company-details-company_number': 'test',
            'company-details-address_line_one': 'test',
            'company-details-address_line_two': 'test',
            'company-details-address_town_city': 'test',
            'company-details-address_county': 'test',
            'company-details-address_post_code': 'test',
            'company-details-industry': 'Other',
            'company-details-industry_other': 'test',
            'company-details-export_status': 'I have customers outside the UK',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'help'}),
        {
            view_name + '-current_step': 'help',
            'help-comment': 'test',
            'help-terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert response.status_code == 302

    response = client.get(response.url)

    assert response.status_code == 302
    assert response.url == reverse(
        'uk-export-finance-lead-generation-form-success'
    )
    assert mock_clean.call_count == 1


@patch('finance.views.PardotAction')
def test_ukef_lead_generation_submit(
    mock_action, client, settings, captcha_stub
):
    settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON'] = True
    settings.UKEF_FORM_SUBMIT_TRACKER_URL = 'submit.com'

    view = views.GetFinanceLeadGenerationFormView()

    form_one = forms.CategoryForm(data={
        'categories': ['Securing upfront funding']
    })
    form_two = forms.HelpForm(data={
        'comment': 'thing',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    })

    assert form_one.is_valid()
    assert form_two.is_valid()

    response = view.done([form_one, form_two])

    assert response.status_code == 302
    assert response.url == str(view.success_url)

    assert mock_action.call_count == 1
    assert mock_action.call_args == call(
        pardot_url=settings.UKEF_FORM_SUBMIT_TRACKER_URL
    )

    assert mock_action().save.call_count == 1
    assert mock_action().save.call_args == call({
        'categories': ['Securing upfront funding'],
        'comment': 'thing',
        'captcha': captcha_stub,
    })


def test_ukef_lead_generation_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON'] = False
    url = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': 'contact'}
    )

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_get_finance_cms(mock_get_finance_page, client, settings):
    settings.UKEF_FORM_SUBMIT_TRACKER_URL = 'submit'
    settings.UKEF_PI_TRACKER_JAVASCRIPT_URL = 'js.com'
    settings.UKEF_PI_TRACKER_ACCOUNT_ID = 'account'
    settings.UKEF_PI_TRACKER_CAMPAIGN_ID = 'campaign'

    url = reverse('get-finance')
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': [['en-gb', 'English']]},
    }
    mock_get_finance_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.GetFinanceView.template_name]


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_pages_cms_page_404(mock_get, client):
    mock_get.return_value = create_response(status_code=404)

    response = client.get(reverse('get-finance'))

    assert response.status_code == 404


def test_ukef_lead_generation_success_page(client, settings):
    settings.FEATURE_FLAGS['UKEF_LEAD_GENERATION_ON'] = True
    url = reverse('uk-export-finance-lead-generation-form-success')
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.GetFinanceLeadGenerationSuccessView.template_name
    ]
