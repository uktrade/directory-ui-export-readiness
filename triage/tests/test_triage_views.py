from unittest.mock import call, patch

import pytest
import requests

from django.core.urlresolvers import reverse
from directory_constants.constants import exred_sector_names

from core.tests.helpers import create_response
from triage import views


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_regular_exporter(mock_persist_answers, client):
    url = reverse('triage-wizard')
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    client.post(url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })
    client.post(url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'True',
    })
    # skips the "do you use the marketplace" step
    summary_response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-sole_trader': True,
    })
    done_response = client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert done_response.status_code == 200
    assert done_response.content == b'success\n'
    assert summary_response.context_data['persona'] == 'Regular Exporter'
    assert summary_response.context_data['sector_label'] == 'Animals; live'
    assert summary_response.context_data['all_cleaned_data'] == {
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'regular_exporter': True,
        'sector': 'HS01',
        'company_number': '',
    }
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call({
        'sole_trader': True,
        'company_name': 'Example corp',
        'used_online_marketplace': None,
        'exported_before': True,
        'regular_exporter': True,
        'sector': 'HS01',
        'company_number': '',
    })


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_occasional_exporter(mock_persist_answers, client):
    url = reverse('triage-wizard')
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    client.post(url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })
    client.post(url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'False',
    })
    client.post(url, {
        view_name + '-current_step': view_class.ONLINE_MARKETPLACE,
        view_class.ONLINE_MARKETPLACE + '-used_online_marketplace': 'True',
    })
    summary_response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-sole_trader': True,
    })
    done_response = client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert done_response.status_code == 200
    assert done_response.content == b'success\n'
    assert summary_response.context_data['persona'] == 'Occasional Exporter'
    assert summary_response.context_data['sector_label'] == 'Animals; live'
    assert summary_response.context_data['all_cleaned_data'] == {
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'used_online_marketplace': True,
        'regular_exporter': False,
        'sector': 'HS01',
        'company_number': '',
    }
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call({
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'used_online_marketplace': True,
        'regular_exporter': False,
        'sector': 'HS01',
        'company_number': '',
    })


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_new_exporter(mock_persist_answers, client):
    url = reverse('triage-wizard')
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    client.post(url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'False',
    })
    summary_response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-sole_trader': True,
    })
    done_response = client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert done_response.status_code == 200
    assert done_response.content == b'success\n'
    assert summary_response.context_data['persona'] == 'New Exporter'
    assert summary_response.context_data['sector_label'] == 'Animals; live'
    assert summary_response.context_data['all_cleaned_data'] == {
        'company_number': '',
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': False,
        'sector': 'HS01',
    }
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call({
        'company_number': '',
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': False,
        'sector': 'HS01',
        'used_online_marketplace': None,
        'regular_exporter': False,
    })


def test_companies_house_search_validation_error(client):
    url = reverse('api-internal-companies-house-search')
    response = client.get(url)  # notice absense of `term`

    assert response.status_code == 400


@patch('triage.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_error(
    mock_search, client
):
    mock_search.return_value = create_response(400)
    url = reverse('api-internal-companies-house-search')

    with pytest.raises(requests.HTTPError):
        client.get(url, data={'term': 'thing'})


@patch('triage.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_success(
    mock_search, client
):
    mock_search.return_value = create_response(
        200, {'items': [{'name': 'Smashing corp'}]}
    )
    url = reverse('api-internal-companies-house-search')

    response = client.get(url, data={'term': 'thing'})

    assert response.status_code == 200
    assert response.content == b'[{"name": "Smashing corp"}]'


@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers')
def test_custom_view(mocked_retrieve_answers, authed_client, sso_user):
    triage_result = {
        'company_name': 'Acme ltd',
        'created': '2016-11-23T11:21:10.977518Z',
        'exported_before': True,
        'regular_exporter': True,
        'used_online_marketplace': False,
        'id': '1',
        'modified': '2016-11-23T11:21:10.977518Z',
        'sector': exred_sector_names.SECTORS_CHOICES[0][0],
        'sector_name': exred_sector_names.SECTORS_CHOICES[0][1],
        'sole_trader': False,
        'sso_id': sso_user.id,
        'company_number': None,
    }
    mocked_retrieve_answers.return_value = triage_result
    url = reverse('custom-page')
    response = authed_client.get(url)
    assert response.status_code == 200
    assert response.template_name == ['triage/custom-page.html']
    assert response.context_data['persona'] == (
        'REGULAR_EXPORTER',
        'Regular Exporter'
    )
    assert response.context_data['triage_result'] == triage_result


@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers')
def test_custom_view_no_triage_result_found(mocked_retrieve_answers,
                                            authed_client):
    mocked_retrieve_answers.return_value = {}
    url = reverse('custom-page')
    response = authed_client.get(url)
    assert response.status_code == 302
    assert response.url == reverse('triage-wizard')
