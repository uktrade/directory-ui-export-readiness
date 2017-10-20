from unittest.mock import call, patch

import pytest
import requests
import requests_mock

from core.tests.helpers import create_response
from triage import helpers


def test_search():
    with requests_mock.mock() as mock:
        mock.get(
            'https://api.companieshouse.gov.uk/search/companies',
            status_code=200,
        )
        response = helpers.CompaniesHouseClient.search(term='green')
        assert response.status_code == 200

    request = mock.request_history[0]

    assert request.query == 'q=green'


def test_search_unauthorized():
    with requests_mock.mock() as mock:
        mock.get(
            'https://api.companieshouse.gov.uk/search/companies',
            status_code=401,
        )
        with pytest.raises(requests.HTTPError):
            helpers.CompaniesHouseClient.search(term='green')


def test_triage_manager_sso_user_returns_database(sso_request):
    manager = helpers.TriageAnswersManager(sso_request)

    assert isinstance(manager, helpers.DatabaseTriageAnswersManager)


def test_triage_manager_anon_user_returns_session(anon_request):
    manager = helpers.TriageAnswersManager(anon_request)

    assert isinstance(manager, helpers.SessionTriageAnswersManager)


@patch('api_client.api_client.exportreadiness.create_triage_result')
def test_database_answer_manager_calls_api(
    mock_create_triage_result, sso_request, sso_user
):
    mock_create_triage_result.return_value = create_response(200)

    data = {'field': 'value'}
    manager = helpers.DatabaseTriageAnswersManager(sso_request)
    manager.persist_answers(data)

    assert mock_create_triage_result.call_count == 1
    assert mock_create_triage_result.call_args == call(
        form_data=data,
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.create_triage_result')
def test_database_create_answer_manager_handles_api_error(
    mock_create_triage_result, sso_request, sso_user
):
    mock_create_triage_result.return_value = create_response(400)

    data = {'field': 'value'}
    manager = helpers.DatabaseTriageAnswersManager(sso_request)

    with pytest.raises(requests.HTTPError):
        manager.persist_answers(data)


@patch('api_client.api_client.exportreadiness.retrieve_triage_result')
def test_database_retrieve_manager_calls_api(
    mock_retrieve_answers, sso_request, sso_user
):
    mock_retrieve_answers.return_value = create_response(200, {'key': 'value'})

    manager = helpers.DatabaseTriageAnswersManager(sso_request)
    answers = manager.retrieve_answers()

    assert mock_retrieve_answers.call_count == 1
    assert mock_retrieve_answers.call_args == call(
        sso_session_id=sso_user.session_id,
    )
    assert answers == {'key': 'value'}


@patch('api_client.api_client.exportreadiness.retrieve_triage_result')
def test_database_retrieve_answer_manager_handles_api_error(
    mock_retrieve_answers, sso_request, sso_user
):
    mock_retrieve_answers.return_value = create_response(400)

    manager = helpers.DatabaseTriageAnswersManager(sso_request)

    with pytest.raises(requests.HTTPError):
        manager.retrieve_answers()


@patch('api_client.api_client.exportreadiness.retrieve_triage_result')
def test_database_retrieve_answer_manager_handles_404(
    mock_retrieve_answers, sso_request, sso_user
):
    mock_retrieve_answers.return_value = create_response(404)

    manager = helpers.DatabaseTriageAnswersManager(sso_request)

    assert manager.retrieve_answers() == {}


def test_session_answer_manager_stores_in_session(anon_request):
    data = {'field': 'value'}
    manager = helpers.SessionTriageAnswersManager(anon_request)
    manager.persist_answers(data)

    assert anon_request.session[manager.SESSION_KEY] == data


def test_session_retrieve_manager_retrieves_from_session(anon_request):
    data = {'field': 'value'}
    key = helpers.SessionTriageAnswersManager.SESSION_KEY

    anon_request.session[key] = data
    assert anon_request.session[key] == data

    manager = helpers.SessionTriageAnswersManager(anon_request)
    answers = manager.retrieve_answers()

    assert answers == data
