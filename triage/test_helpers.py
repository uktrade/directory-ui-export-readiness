from unittest.mock import call, patch

import pytest
import requests

from sso.utils import SSOUser
from triage import helpers


def create_response(status_code, json_body={}):
    response = requests.Response()
    response.status_code = status_code
    response.json = lambda: json_body
    return response


@pytest.fixture
def sso_user():
    return SSOUser(
        id=1,
        email='test@example.com',
        session_id='123',
    )


@pytest.fixture
def sso_request(rf, sso_user):
    request = rf.get('/')
    request.sso_user = sso_user
    return request


@pytest.fixture
def anon_request(rf, client):
    request = rf.get('/')
    request.sso_user = None
    request.session = client.session
    return request


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
