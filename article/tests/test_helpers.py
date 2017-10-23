from unittest.mock import patch, call

import pytest
import requests

from article import helpers
from core.tests.helpers import create_response


def test_build_twitter_link(rf):
    request = rf.get('/')
    actual = helpers.build_twitter_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'https://twitter.com/intent/tweet'
        '?text=Export Readiness - Do research first http://testserver/'
    )


def test_build_facebook_link(rf):
    request = rf.get('/')
    actual = helpers.build_facebook_link(
        request=request,
        title='Do research first',
    )
    assert actual == (
        'http://www.facebook.com/share.php?u=http://testserver/'
    )


def test_build_linkedin_link(rf):
    request = rf.get('/')
    actual = helpers.build_linkedin_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'https://www.linkedin.com/shareArticle?mini=true&'
        'url=http://testserver/&'
        'title=Export Readiness - Do research first&source=LinkedIn'
    )


def test_build_email_link(rf):
    request = rf.get('/')
    actual = helpers.build_email_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'mailto:?body=Export Readiness - Do research first'
        '&subject=http://testserver/'
    )


@patch('api_client.api_client.exportreadiness.create_article_read')
def test_database_create_article_read_calls_api(
    mock_create_article_read, sso_request, sso_user
):
    mock_create_article_read.return_value = create_response(200)

    article = {'key', 'value'}
    manager = helpers.DatabaseArticlesReadManager(sso_request)
    manager.persist_article(article)

    assert mock_create_article_read.call_count == 1
    assert mock_create_article_read.call_args == call(
        form_data=article,
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.create_article_read')
def test_database_create_article_read_handle_exceptions(
    mock_create_article_read, sso_request, sso_user
):
    mock_create_article_read.return_value = create_response(400)
    manager = helpers.DatabaseArticlesReadManager(sso_request)

    with pytest.raises(requests.HTTPError):
        manager.persist_article({'key', 'value'})


@patch('api_client.api_client.exportreadiness.retrieve_article_read')
def test_database_retrieve_article_read_calls_api(
    mock_retrieve_article_read, sso_request, sso_user
):
    mock_retrieve_article_read.return_value = create_response(200)

    manager = helpers.DatabaseArticlesReadManager(sso_request)
    manager.retrieve_articles()

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
    data = {'article_uuid': '123'}
    manager = helpers.SessionArticlesReadManager(anon_request)
    manager.persist_article(data)

    assert anon_request.session[manager.SESSION_KEY] == [
        {'article_uuid': '123'}
    ]


def test_session_article_manager_stores_in_session_existing_articles(
        anon_request
):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = [{'article_uuid': '123'}]
    assert anon_request.session[key] == [{'article_uuid': '123'}]

    data = {'article_uuid': '345'}
    manager = helpers.SessionArticlesReadManager(anon_request)
    manager.persist_article(data)

    assert anon_request.session[manager.SESSION_KEY] == [
        {'article_uuid': '123'},
        {'article_uuid': '345'}
    ]


def test_session_article_manager_retrieves_from_session(anon_request):
    key = helpers.SessionArticlesReadManager.SESSION_KEY
    anon_request.session[key] = [{'article_uuid': '123'}]
    assert anon_request.session[key] == [{'article_uuid': '123'}]

    manager = helpers.SessionArticlesReadManager(anon_request)
    answers = manager.retrieve_articles()

    assert answers == [{'article_uuid': '123'}]
