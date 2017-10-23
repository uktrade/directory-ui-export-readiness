from unittest.mock import patch, call

import pytest
import requests

from article import helpers
from core.tests.helpers import create_response


@patch('api_client.api_client.exportreadiness.create_article_read')
def test_database_create_article_read_calls_api(
    mock_create_article_read, sso_request, sso_user
):
    mock_create_article_read.return_value = create_response(200)

    manager = helpers.DatabaseArticlesReadManager(sso_request)
    manager.persist_article(article_uuid='123')

    assert mock_create_article_read.call_count == 1
    assert mock_create_article_read.call_args == call(
        article_uuid='123',
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.create_article_read')
def test_database_create_article_read_handle_exceptions(
    mock_create_article_read, sso_request, sso_user
):
    mock_create_article_read.return_value = create_response(400)
    manager = helpers.DatabaseArticlesReadManager(sso_request)

    with pytest.raises(requests.HTTPError):
        manager.persist_article(article_uuid='123')


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_retrieve_article_read_calls_api(
    mock_retrieve_article_read, sso_request, sso_user
):
    mock_retrieve_article_read.return_value = create_response(
        200, json_body=[
            {
                'created': '2016-11-23T11:21:10.977518Z',
                'id': '1',
                'modified': '2016-11-23T11:21:10.977518Z',
                'sso_id': '999',
                'article_uuid': '123'
            },
            {
                'created': '2016-11-23T11:21:10.977518Z',
                'id': '2',
                'modified': '2016-11-23T11:21:10.977518Z',
                'sso_id': '999',
                'article_uuid': '345'
            }
        ]
    )

    manager = helpers.DatabaseArticlesReadManager(sso_request)
    articles = manager.retrieve_articles()

    assert articles == ['123', '345']
    assert mock_retrieve_article_read.call_count == 1
    assert mock_retrieve_article_read.call_args == call(
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_retrieve_article_read_handle_exceptions(
    mock_retrieve_article_read, sso_request, sso_user
):
    mock_retrieve_article_read.return_value = create_response(400)
    manager = helpers.DatabaseArticlesReadManager(sso_request)

    with pytest.raises(requests.HTTPError):
        manager.retrieve_articles()


def test_session_article_manager_stores_in_session_no_existing_articles(
        anon_request
):
    manager = helpers.SessionArticlesReadManager(anon_request)
    manager.persist_article(article_uuid='123')

    assert anon_request.session[manager.SESSION_KEY] == ['123']


def test_session_article_manager_stores_in_session_existing_articles(
        anon_request
):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = ['123']
    assert anon_request.session[key] == ['123']

    manager = helpers.SessionArticlesReadManager(anon_request)
    manager.persist_article(article_uuid='345')

    assert anon_request.session[manager.SESSION_KEY] == ['123', '345']


def test_session_article_manager_retrieves_from_session(anon_request):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = ['123']
    assert anon_request.session[key] == ['123']

    manager = helpers.SessionArticlesReadManager(anon_request)
    answers = manager.retrieve_articles()

    assert answers == ['123']
