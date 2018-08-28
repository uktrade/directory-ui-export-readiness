from unittest.mock import patch

import pytest
from requests.exceptions import HTTPError

from django.urls import reverse

from core.tests.helpers import create_response
from invest import views


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_feature_flag_on(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-details-request-form',
        kwargs={'opportunity_slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.HighPotentialOpportunityFormView.template_name
    ]


def test_high_potential_opportunity_feature_flag_off(settings, client):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': False
    }

    url = reverse(
        'high-potential-opportunity-details-request-form',
        kwargs={'opportunity_slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_cms_retrieval_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={
            'full_name': {
                'help_text': 'full name help text'
            },
            'role_in_company': {
                'help_text': 'role help text'
            }
        }
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-details-request-form',
        kwargs={'opportunity_slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['full_name'].help_text == 'full name help text'
    assert form.fields['role_in_company'].help_text == 'role help text'


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_cms_retrieval_not_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=400)
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-details-request-form',
        kwargs={'opportunity_slug': 'rail'}
    )

    with pytest.raises(HTTPError):
        client.get(url)
