from unittest.mock import Mock, patch

from healthcheck import backends


@patch('sso.utils.sso_api_client.ping',
       Mock(side_effect=Exception('oops')))
def test_single_sign_on_ping_connection_error():
    backend = backends.SingleSignOnBackend()
    backend.run_check()

    assert backend.pretty_status() == 'unavailable: (SSO proxy) oops'


@patch('sso.utils.sso_api_client.ping',
       Mock(return_value=Mock(status_code=500)))
def test_single_sign_on_ping_not_ok():
    backend = backends.SingleSignOnBackend()
    backend.run_check()

    assert backend.pretty_status() == (
        'unexpected result: SSO proxy returned 500 status code'
    )


@patch('sso.utils.sso_api_client.ping',
       Mock(return_value=Mock(status_code=200)))
def test_single_sign_on_ping_ok():
    backend = backends.SingleSignOnBackend()
    backend.run_check()

    assert backend.pretty_status() == 'working'


@patch('api_client.api_client.ping', Mock(side_effect=Exception('oops')))
def test_api_ping_connection_error():
    backend = backends.APIProxyBackend()
    backend.run_check()

    assert backend.pretty_status() == 'unavailable: (API proxy) oops'


@patch('api_client.api_client.ping', Mock(return_value=Mock(status_code=500)))
def test_api_ping_not_ok():
    backend = backends.APIProxyBackend()
    backend.run_check()

    assert backend.pretty_status() == (
        'unexpected result: api proxy returned 500 status code'
    )


@patch('api_client.api_client.ping',
       Mock(return_value=Mock(status_code=200)))
def test_api_ping_ok():
    backend = backends.APIProxyBackend()
    backend.run_check()

    assert backend.pretty_status() == 'working'
