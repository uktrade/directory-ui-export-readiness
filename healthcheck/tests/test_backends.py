from unittest.mock import Mock, patch

from healthcheck import backends


@patch('directory_sso_api_client.client.sso_api_client.ping',
       Mock(side_effect=Exception('oops')))
def test_single_sign_on_ping_connection_error():
    backend = backends.SingleSignOnBackend()
    backend.run_check()

    assert backend.pretty_status() == 'unavailable: (SSO proxy) oops'


@patch('directory_sso_api_client.client.sso_api_client.ping',
       Mock(return_value=Mock(status_code=500)))
def test_single_sign_on_ping_not_ok():
    backend = backends.SingleSignOnBackend()
    backend.run_check()

    assert backend.pretty_status() == (
        'unexpected result: SSO proxy returned 500 status code'
    )


@patch('directory_sso_api_client.client.sso_api_client.ping',
       Mock(return_value=Mock(status_code=200)))
def test_single_sign_on_ping_ok():
    backend = backends.SingleSignOnBackend()
    backend.run_check()

    assert backend.pretty_status() == 'working'


@patch('directory_api_client.client.api_client.ping',
       Mock(side_effect=Exception('oops')))
def test_api_ping_connection_error():
    backend = backends.APIProxyBackend()
    backend.run_check()

    assert backend.pretty_status() == 'unavailable: (API proxy) oops'


@patch('directory_api_client.client.api_client.ping',
       Mock(return_value=Mock(status_code=500)))
def test_api_ping_not_ok():
    backend = backends.APIProxyBackend()
    backend.run_check()

    assert backend.pretty_status() == (
        'unexpected result: api proxy returned 500 status code'
    )


@patch('directory_api_client.client.api_client.ping',
       Mock(return_value=Mock(status_code=200)))
def test_api_ping_ok():
    backend = backends.APIProxyBackend()
    backend.run_check()

    assert backend.pretty_status() == 'working'
