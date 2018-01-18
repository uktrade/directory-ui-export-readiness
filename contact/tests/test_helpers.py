import json

import pytest
import requests_mock

from django.urls import reverse

from contact import helpers


def test_create_zendesk_ticket(settings):
    data = {'contact_name': 'Jim example', 'contact_email': 'test@example.com'}
    with requests_mock.mock() as mock:
        mock.post(settings.CONTACT_ZENDESK_URL, status_code=201)
        helpers.create_zendesk_ticket(
            cleaned_data=data,
            service='directory',
            ingress_url='http://google.com',
        )

    request = mock.request_history[0]

    assert request.headers['Authorization'] == 'Basic ZGVidWcvdG9rZW46ZGVidWc='
    assert json.loads(request.body) == {
        'ticket': {
            'custom_fields': [{'id': 31281329, 'value': 'directory'}],
            'comment': {
                'body': (
                    'contact_name: \nJim example\n\n'
                    'contact_email: \ntest@example.com\n\n'
                    'originating_page: \nhttp://google.com\n\n'
                    'service: \ndirectory\n'
                )
            },
            'requester': {
                'email': 'test@example.com',
                'name': 'Jim example'
            }
        }
    }


agnostic_interstitial = reverse('contact-us-interstitial-service-agnostic')
service_intersticial = reverse(
    'contact-us-interstitial-service-specific', kwargs={'service': 'directory'}
)


@pytest.mark.parametrize('http_referer,session_referer,expected', (
    (None,                  None, 'Direct request'),
    (agnostic_interstitial, None, 'Direct request'),
    (service_intersticial,  None, 'Direct request'),
    ('www.google.com',      None, 'www.google.com'),
    (agnostic_interstitial, 'www.google.com', 'www.google.com'),
    (service_intersticial,  'www.google.com', 'www.google.com'),
))
def test_get_ingress_url(
    http_referer, session_referer, expected, rf, client
):
    request = rf.get('/', HTTP_REFERER=http_referer)
    request.session = client.session
    request.session[helpers.INGRESS_URL_SESSION_KEY] = session_referer

    assert helpers.get_ingress_url(request) == expected
