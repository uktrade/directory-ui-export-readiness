from unittest.mock import call, patch

from directory_cms_client.constants import (
    EXPORT_READINESS_GET_FINANCE_SLUG,
)
import pytest

from django.urls import reverse

from core.tests.helpers import create_response
from finance import views


@pytest.mark.parametrize('step,submit_url', (
    ('contact', None),
    ('your-details', None),
    ('company-details', None),
    ('help', 'submit.com'),
))
def test_ukef_lead_generation_feature_flag_on(
    client, settings, step, submit_url
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENERATION_ON': True
    }
    settings.UKEF_FORM_SUBMIT_TRACKER_URL = 'submit.com'
    settings.UKEF_PI_TRACKER_JAVASCRIPT_URL = 'js.com'
    settings.UKEF_PI_TRACKER_ACCOUNT_ID = 'account'
    settings.UKEF_PI_TRACKER_CAMPAIGN_ID = 'campaign'
    url = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': step}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data.get('form_submit_url') == submit_url
    assert response.context_data['pi_tracker_javascript_url'] == 'js.com'
    assert response.context_data['pi_tracker_account_id'] == 'account'
    assert response.context_data['pi_tracker_campaign_id'] == 'campaign'

    assert response.template_name == [
        views.GetFinanceLeadGenerationFormView.templates[step]
    ]


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
    assert response.context_data['pi_tracker_javascript_url'] == 'js.com'
    assert response.context_data['pi_tracker_account_id'] == 'account'
    assert response.context_data['pi_tracker_campaign_id'] == 'campaign'


def test_start_redirect_url(client, settings):
    url = reverse('uk-export-finance-pardot-funnel-start')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == settings.UKEF_FORM_START_TRACKER_URL


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
