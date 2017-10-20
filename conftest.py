from unittest.mock import patch

import pytest

from sso.utils import SSOUser


@pytest.fixture
def sso_user():
    return SSOUser(
        id=999,
        email='test@foo.com',
        session_id=1
    )


def process_request(self, request):
    request.sso_user = sso_user()


@pytest.fixture
def authed_client(client):
    stub = patch(
        'sso.middleware.SSOUserMiddleware.process_request', process_request
    )
    stub.start()
    yield client
    stub.stop()
