import logging
import json
from urllib.parse import urlparse

import requests

from django.conf import settings
from django.urls import resolve, Resolver404


logger = logging.getLogger(__name__)

DIRECT_REQUEST = 'Direct request'
INGRESS_URL_SESSION_KEY = 'ingress_url'
INTERSTITIAL_URL_NAMES = [
    'contact-us-interstitial-service-agnostic',
    'contact-us-interstitial-service-specific',
]


def create_zendesk_ticket(cleaned_data, service, ingress_url):
    auth = requests.auth.HTTPBasicAuth(
        '{0}/token'.format(settings.CONTACT_ZENDESK_USER),
        settings.CONTACT_ZENDESK_TOKEN,
    )
    data = get_ticket_data(
        cleaned_data=cleaned_data,
        service=service,
        ingress_url=ingress_url,
    )
    response = requests.post(
        url=settings.CONTACT_ZENDESK_URL,
        data=json.dumps(data),
        auth=auth,
        headers={'content-type': 'application/json'},
    )
    if response.status_code != 201:
        logger.error('Zendesk submission error', extra={
            'body': data,
            'response_code': response.status_code,
            'response_reason': response.reason
        })
    return response


def get_ticket_data(cleaned_data, service, ingress_url):
    """
    Return the entire ticket data that will be sent to the Zendesk API.
    If extra fields (beyond comment, custom_fields, and requester) are
    required in the ticket creation, inheriting
    classes will need to override this method to add the extra properties.

    See the Zendesk API docs for the structure of the request data:
    https://developer.zendesk.com/rest_api/docs/core/

    """

    form_fields = list(cleaned_data.items())
    extra_fields = [('originating_page', ingress_url), ('service', service)]
    fields = form_fields + extra_fields
    body = ['{0}: \n{1}\n'.format(name, value) for name, value in fields]

    return {
        'ticket': {
            'comment': {'body': '\n'.join(body)},
            'custom_fields': [{'id': 31281329, 'value': service}],
            'requester': {
                'name': cleaned_data.get('contact_name'),
                'email': cleaned_data.get('contact_email')
            },
        }
    }


def get_ingress_url(request):
    referer_header_url = request.META.get('HTTP_REFERER')
    ingress_url = None

    if referer_header_url is None:
        ingress_url = DIRECT_REQUEST
    elif is_url_interstitial(referer_header_url):
        ingress_url = request.session[INGRESS_URL_SESSION_KEY]
    return ingress_url or referer_header_url


def is_url_internal(url):
    try:
        resolve(urlparse(url).path)
    except Resolver404:
        is_internal = False
    else:
        is_internal = True
    return is_internal


def is_url_interstitial(url):
    if not is_url_internal(url):
        return False
    resolved = resolve(urlparse(url).path)
    return resolved.url_name in INTERSTITIAL_URL_NAMES
