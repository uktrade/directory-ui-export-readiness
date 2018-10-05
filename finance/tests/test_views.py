from unittest.mock import call, patch

from directory_cms_client.constants import (
    EXPORT_READINESS_GET_FINANCE_SLUG,
)
import pytest

from django.urls import reverse

from core.tests.helpers import create_response
from finance import forms, views


@pytest.mark.parametrize(
    'step',
    ('contact', 'your-details', 'company-details', 'help')
)
def test_ukef_lead_generation_feature_flag_on(
    client, settings, step
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENERATION_ON': True
    }
    url = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': step}
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.GetFinanceLeadGenerationFormView.templates[step]
    ]


@patch('requests.post')
def test_ukef_lead_generation_submit(
    mock_post, client, settings, captcha_stub
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENERATION_ON': True
    }
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
    assert mock_post.call_count == 1
    assert mock_post.call_args == call(
        settings.UKEF_FORM_SUBMIT_TRACKER_URL,
        {
            'categories': ['Securing upfront funding'],
            'comment': 'thing',
            'captcha': captcha_stub,
        },
        allow_redirects=False,
    )


def test_ukef_lead_generation_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENERATION_ON': False
    }
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
        'meta': {'languages': ['en-gb']},
    }
    mock_get_finance_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.GetFinance.template_name]


@pytest.mark.parametrize('enabled,slug', (
    (True, EXPORT_READINESS_GET_FINANCE_SLUG),
    (False, EXPORT_READINESS_GET_FINANCE_SLUG + '-deprecated'),
))
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_pages_cms_client_params_feature_flag(
    mock_get, client, settings, enabled, slug
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENERATION_ON': enabled
    }

    mock_get.return_value = create_response(status_code=200)
    url = reverse('get-finance')
    response = client.get(url, {'draft_token': '123'})

    assert response.status_code == 200
    assert mock_get.call_count == 1
    assert mock_get.call_args == call(
        slug=slug,
        draft_token='123',
        language_code='en-gb'
    )


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_cms_pages_cms_page_404(mock_get, client):
    mock_get.return_value = create_response(status_code=404)

    response = client.get(reverse('get-finance'))

    assert response.status_code == 404


def test_ukef_lead_generation_success_page(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENERATION_ON': True
    }
    url = reverse('uk-export-finance-lead-generation-form-success')
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.GetFinanceLeadGenerationSuccessView.template_name
    ]
