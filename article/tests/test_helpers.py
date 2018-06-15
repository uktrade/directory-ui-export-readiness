from unittest.mock import patch, call

from directory_constants.constants import exred_articles
import pytest

from article import articles, helpers, structure
from core.tests.helpers import create_response


@pytest.fixture
def articles_read():
    return [
        {
            'created': '2016-11-23T11:21:10.977518Z',
            'id': '1',
            'modified': '2016-11-23T11:21:10.977518Z',
            'sso_id': '999',
            'article_uuid': exred_articles.CONSIDER_HOW_PAID
        },
        {
            'created': '2016-11-23T11:21:10.977518Z',
            'id': '2',
            'modified': '2016-11-23T11:21:10.977518Z',
            'sso_id': '999',
            'article_uuid': exred_articles.INVOICE_CURRENCY_AND_CONTENTS
        },
        {
            'created': '2016-11-23T11:21:10.977518Z',
            'id': '3',
            'modified': '2016-11-23T11:21:10.977518Z',
            'sso_id': '999',
            'article_uuid': exred_articles.PLAN_THE_LOGISTICS
        }
    ]


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_create_article_read_calls_api(
    mock_bulk_create_article_read, sso_request, sso_user
):
    mock_bulk_create_article_read.return_value = create_response(200)

    manager = helpers.DatabaseArticlesViewedManager(sso_request)
    manager.persist_articles(article_uuids=['123'])

    assert mock_bulk_create_article_read.call_count == 1
    assert mock_bulk_create_article_read.call_args == call(
        article_uuids=['123'],
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_bulk_create_article_read_calls_api(
    mock_bulk_create_article_read, sso_request, sso_user
):
    mock_bulk_create_article_read.return_value = create_response(200)

    manager = helpers.DatabaseArticlesViewedManager(sso_request)
    manager.persist_articles(article_uuids=[1, 2, 3])

    assert mock_bulk_create_article_read.call_count == 1
    assert mock_bulk_create_article_read.call_args == call(
        article_uuids=[1, 2, 3],
        sso_session_id=sso_user.session_id,
    )


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_create_article_read_handle_exceptions(
    mock_bulk_create_article_read, sso_request
):
    mock_bulk_create_article_read.return_value = create_response(
        400, content='{"error": "bad"}'
    )
    manager = helpers.DatabaseArticlesViewedManager(sso_request)

    with pytest.raises(AssertionError) as execinfo:
        manager.persist_articles(article_uuids=['123'])

    assert str(execinfo.value) == '{"error": "bad"}'


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_articles_viewed_for_group(
    mock_bulk_create_article_read, sso_request, articles_read
):
    mock_bulk_create_article_read.return_value = create_response(
        200, json_body=articles_read
    )
    manager = helpers.DatabaseArticlesViewedManager(sso_request)
    # trigger the caching of the articles
    manager.persist_articles([])

    group_key = structure.GUIDANCE_GETTING_PAID_ARTICLES.name
    articles_uuids = manager.articles_viewed_for_group(group_key)
    assert sorted(list(articles_uuids)) == [
        exred_articles.CONSIDER_HOW_PAID,
        exred_articles.INVOICE_CURRENCY_AND_CONTENTS,
    ]
    assert len(articles_uuids) == 2


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_get_view_progress_for_groups(
    mock_bulk_create_article_read, sso_request, articles_read
):
    mock_bulk_create_article_read.return_value = create_response(
        200, json_body=articles_read
    )
    # trigger the caching of the articles
    sso_request.session[helpers.SessionArticlesViewedManager.SESSION_KEY] = [1]

    manager = helpers.ArticlesViewedManagerFactory(sso_request)

    actual = manager.get_view_progress_for_groups()
    assert actual == {
        'all': {'read': 3, 'total': 49},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 2, 'total': 5},
        'market_research': {'read': 0, 'total': 7},
        'operations_and_compliance': {'read': 1, 'total': 12},
        'persona_new': {'read': 2, 'total': 23},
        'persona_occasional': {'read': 2, 'total': 42},
        'persona_regular': {'read': 0, 'total': 21},
        'custom_persona_new': {'read': 2, 'total': 23},
        'custom_persona_occasional': {'read': 2, 'total': 42},
        'custom_persona_regular': {'read': 0, 'total': 21},
    }


def test_session_get_view_progress_for_groups(anon_request, articles_read):

    key = helpers.SessionArticlesViewedManager.SESSION_KEY
    anon_request.session[key] = [i['article_uuid'] for i in articles_read]

    manager = helpers.ArticlesViewedManagerFactory(anon_request)
    actual = manager.get_view_progress_for_groups()

    assert actual == {
        'all': {'read': 3, 'total': 49},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 2, 'total': 5},
        'market_research': {'read': 0, 'total': 7},
        'operations_and_compliance': {'read': 1, 'total': 12},
        'persona_new': {'read': 2, 'total': 23},
        'persona_occasional': {'read': 2, 'total': 42},
        'persona_regular': {'read': 0, 'total': 21},
        'custom_persona_new': {'read': 2, 'total': 23},
        'custom_persona_occasional': {'read': 2, 'total': 42},
        'custom_persona_regular': {'read': 0, 'total': 21},
    }


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_article_read_manager_synchronises_articles(
    mock_bulk_create_article_read, sso_request, sso_user,
):
    session_key = helpers.SessionArticlesViewedManager.SESSION_KEY
    sso_request.session[session_key] = [1, 2, 3]
    mock_bulk_create_article_read.return_value = create_response(200)

    helpers.ArticlesViewedManagerFactory(sso_request)

    assert mock_bulk_create_article_read.call_count == 1
    assert mock_bulk_create_article_read.call_args == call(
        article_uuids=frozenset([1, 2, 3]),
        sso_session_id=sso_user.session_id,
    )

    assert sso_request.session[session_key] == []


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_article_read_manager_handles_no_read_articles_on_synchronisation(
    mock_bulk_create_article_read, sso_request, sso_user,
):
    session_key = helpers.SessionArticlesViewedManager.SESSION_KEY
    sso_request.session[session_key] = []
    mock_bulk_create_article_read.return_value = create_response(200)

    helpers.ArticlesViewedManagerFactory(sso_request)

    # call the api method anyway - because the response contains the list of
    # read articles
    assert mock_bulk_create_article_read.call_count == 1

    assert sso_request.session[session_key] == []


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_article_read_manager_not_clear_session_on_api_error(
    mock_bulk_create_article_read, sso_request, sso_user
):
    session_key = helpers.SessionArticlesViewedManager.SESSION_KEY
    sso_request.session[session_key] = [1, 2, 3]
    mock_bulk_create_article_read.return_value = create_response(
        400, content='validation error'
    )

    with pytest.raises(AssertionError) as execinfo:
        helpers.ArticlesViewedManagerFactory(sso_request)

    assert sso_request.session[session_key] == [1, 2, 3]
    assert str(execinfo.value) == 'validation error'


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_remaining_read_time_for_group(
    mock_bulk_create_article_read, sso_request, articles_read
):
    mock_bulk_create_article_read.return_value = create_response(
        200, json_body=articles_read
    )

    manager = helpers.DatabaseArticlesViewedManager(sso_request)
    # trigger the caching of the articles
    manager.persist_articles([])

    time_left = manager.remaining_read_time_for_group(
        structure.PERSONA_OCCASIONAL_ARTICLES.name
    )

    assert time_left == 5242


@patch('api_client.api_client.exportreadiness.bulk_create_article_read')
def test_database_retrieve_article_returns_bulk_create_response(
    mock_bulk_create_article_read, sso_request, sso_user, articles_read
):
    mock_bulk_create_article_read.return_value = create_response(
        200, json_body=articles_read
    )

    manager = helpers.DatabaseArticlesViewedManager(sso_request)

    # trigger the caching of the articles
    manager.persist_articles([])

    assert manager.retrieve_viewed_article_uuids() == {
        articles_read[0]['article_uuid'],
        articles_read[1]['article_uuid'],
        articles_read[2]['article_uuid'],
    }


def test_session_article_manager_stores_in_session_no_existing_articles(
        anon_request
):
    manager = helpers.SessionArticlesViewedManager(anon_request)
    manager.persist_article(article_uuid='123')

    assert anon_request.session[manager.SESSION_KEY] == ['123']


def test_session_article_manager_stores_in_session_existing_articles(
        anon_request
):
    key = helpers.SessionArticlesViewedManager.SESSION_KEY
    anon_request.session[key] = ['123']
    assert anon_request.session[key] == ['123']

    manager = helpers.SessionArticlesViewedManager(anon_request)
    manager.persist_article(article_uuid='345')

    assert anon_request.session[manager.SESSION_KEY] == ['123', '345']


def test_session_article_manager_retrieves_from_session(anon_request):
    key = helpers.SessionArticlesViewedManager.SESSION_KEY
    anon_request.session[key] = ['123']
    assert anon_request.session[key] == ['123']

    manager = helpers.SessionArticlesViewedManager(anon_request)
    answers = manager.retrieve_viewed_article_uuids()

    assert answers == {'123'}


def test_session_article_view_count_for_group(anon_request):
    key = helpers.SessionArticlesViewedManager.SESSION_KEY
    articles_uuids = [
        exred_articles.PLAN_THE_LOGISTICS,
        exred_articles.USE_FREIGHT_FORWARDER,
        exred_articles.CONSIDER_HOW_PAID
    ]
    anon_request.session[key] = articles_uuids
    assert anon_request.session[key] == articles_uuids

    group_key = structure.GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES.name
    manager = helpers.SessionArticlesViewedManager(anon_request)

    returned_articles_uuids = manager.articles_viewed_for_group(group_key)
    count = len(manager.articles_viewed_for_group(group_key))

    expected_articles_uuids = sorted([
        exred_articles.PLAN_THE_LOGISTICS,
        exred_articles.USE_FREIGHT_FORWARDER,
    ])
    assert sorted(list(returned_articles_uuids)) == expected_articles_uuids
    assert count == 2


def test_session_remaining_read_time_for_group(anon_request):
    key = helpers.SessionArticlesViewedManager.SESSION_KEY
    anon_request.session[key] = [
        exred_articles.DEFINE_MARKET_POTENTIAL,
        exred_articles.DO_FIELD_RESEARCH,
        exred_articles.ANALYSE_THE_COMPETITION
    ]
    assert anon_request.session[key] == [
        exred_articles.DEFINE_MARKET_POTENTIAL,
        exred_articles.DO_FIELD_RESEARCH,
        exred_articles.ANALYSE_THE_COMPETITION
    ]

    manager = helpers.SessionArticlesViewedManager(anon_request)
    time_left = manager.remaining_read_time_for_group(
        structure.PERSONA_OCCASIONAL_ARTICLES.name
    )

    assert time_left == 5020


def test_time_to_read_in_seconds():
    article = articles.INVOICE_CURRENCY_AND_CONTENTS
    assert helpers.time_to_read_in_seconds(
        article
    ) == 224
