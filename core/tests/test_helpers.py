import pytest
import requests

from django.shortcuts import Http404

from core import helpers
import core.tests.helpers


def test_build_twitter_link(rf):
    request = rf.get('/')
    actual = helpers.build_twitter_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'https://twitter.com/intent/tweet'
        '?text=Export%20Readiness%20-%20Do%20research%20first%20'
        'http://testserver/'
    )


def test_build_facebook_link(rf):
    request = rf.get('/')
    actual = helpers.build_facebook_link(
        request=request,
        title='Do research first',
    )
    assert actual == (
        'https://www.facebook.com/share.php?u=http://testserver/'
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
        'title=Export%20Readiness%20-%20Do%20research%20first%20'
        '&source=LinkedIn'
    )


def test_build_email_link(rf):
    request = rf.get('/')
    actual = helpers.build_email_link(
        request=request,
        title='Do research first',
    )

    assert actual == (
        'mailto:?body=http://testserver/'
        '&subject=Export%20Readiness%20-%20Do%20research%20first%20'
    )


@pytest.mark.parametrize('status_code,exception', (
    (400, requests.exceptions.HTTPError),
    (404, Http404),
    (500, requests.exceptions.HTTPError),
))
def test_handle_cms_response_error(status_code, exception):
    response = core.tests.helpers.create_response(status_code=status_code)
    with pytest.raises(exception):
        helpers.handle_cms_response(response)


def test_handle_cms_response_ok():
    response = core.tests.helpers.create_response(
        status_code=200, json_body={'field': 'value'}
    )

    assert helpers.handle_cms_response(response) == {'field': 'value'}
