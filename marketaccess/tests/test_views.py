from unittest import mock

from django.conf import settings

from django.urls import reverse

from core.tests.helpers import create_response
from marketaccess import views


def test_form_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_FORM_ON'] = False

    response = client.get(reverse('market-access'))

    assert response.status_code == 404


def test_form_feature_flag_on(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_FORM_ON'] = True

    response = client.get(reverse('market-access'))

    assert response.status_code == 200


@mock.patch('directory_forms_api_client.actions.ZendeskAction')
def test_form_submission(mock_zendesk_action, client):
    url_name = 'report-ma-barrier'
    view_name = 'report_market_access_barrier_form_view'

    response = client.post(
        reverse(url_name, kwargs={'step': 'about'}),
        {
            view_name + '-current_step': 'about',
            'about-firstname': 'Craig',
            'about-lastname': 'Smith',
            'about-jobtitle': 'Musician',
            'about-categories': "I'm an exporter / seeking to export",
            'about-company_name': 'Craig Music',
            'about-email': 'craig@craigmusic.com',
            'about-phone': '0123456789',
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'problem-details'}),
        {
            view_name + '-current_step': 'problem-details',
            'problem-details-country': 'Angola',
            'problem-details-problem_summary': 'problem summary',
            'problem-details-impact': 'problem impact',
            'problem-details-resolve_summary': 'steps in resolving',
            'problem-details-eu_exit_related': False,

        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'other-details'}),
        {
            view_name + '-current_step': 'other-details',
            'other-details-other_details': 'additional details'
        }
    )
    assert response.status_code == 302

    response = client.post(
        reverse(url_name, kwargs={'step': 'summary'}),
        {
            view_name + '-current_step': 'summary',
        }
    )
    assert response.status_code == 302

    assert response.url == reverse(
        'report-barrier-form-success'
    )
    assert mock_zendesk_action.call_count == 1
    subject = f"{settings.MARKET_ACCESS_ZENDESK_SUBJECT}: Angola: Craig Music"
    assert mock_zendesk_action.call_args == mock.call(
        subject=subject,
        full_name='Craig Smith',
        email_address='craig@craigmusic.com',
        service_name='market_access',
        form_url=reverse(
            'report-ma-barrier', kwargs={'step': 'about'}
        )
    )
    assert mock_zendesk_action().save.call_count == 1
    assert mock_zendesk_action().save.call_args == mock.call({
        'firstname': 'Craig',
        'lastname': 'Smith',
        'jobtitle': 'job',
        'categories': "I'm an exporter / seeking to export",
        'company_name': 'Craig Music',
        'email': 'craig@craigmusic.com',
        'phone': '0123456789',
        'product_service': 'something',
        'country': 'Angola',
        'problem_summary': 'problem summary',
        'impact': 'problem impact',
        'resolve_summary': 'steps in resolving',
        'eu_exit_related': 'False',
        'other_details': 'additional details'
    })


def test_form_initial_data(client):
    response_one = client.get(
        reverse('report-ma-barrier', kwargs={'step': 'about'}),
    )
    assert response_one.context_data['form'].initial == {}

    response_two = client.get(
        reverse('report-ma-barrier', kwargs={'step': 'problem-details'}),
    )
    assert response_two.context_data['form'].initial == {}

    response_four = client.get(
        reverse('report-ma-barrier', kwargs={'step': 'other-details'}),
    )
    assert response_four.context_data['form'].initial == {}
