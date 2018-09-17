from unittest.mock import call, patch

from directory_constants.constants import choices
import pytest
from requests.exceptions import HTTPError

from django.urls import reverse

from core.tests.helpers import create_response
from invest import views


@patch('invest.helpers.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_feature_flag_on(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_body={'opportunity_list': []}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.HighPotentialOpportunityFormView.template_name
    ]


def test_high_potential_opportunity_form_feature_flag_off(settings, client):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': False
    }

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 404


@patch('invest.helpers.cms_api_client.lookup_by_slug')
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
            },
            'opportunity_list': [
                {
                    'pdf_document_url': 'http://www.example.com/a',
                    'heading': 'some great opportunity',
                }
            ]
        }
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['full_name'].help_text == 'full name help text'
    assert form.fields['role_in_company'].help_text == 'role help text'
    assert form.fields['opportunities'].choices == [
        ('http://www.example.com/a', 'some great opportunity'),
    ]


@patch('invest.helpers.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_cms_retrieval_not_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=400)
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    with pytest.raises(HTTPError):
        client.get(url)


@patch('invest.helpers.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail_feature_flag_on(
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
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.HighPotentialOpportunityDetailView.template_name
    ]


def test_high_potential_opportunity_detail_feature_flag_off(settings, client):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': False
    }

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 404


@patch('invest.helpers.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail_cms_retrieval_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={'title': '1234'}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert response.context_data['page'] == {'title': '1234'}


@patch('invest.helpers.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_detail_cms_retrieval_not_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=400)
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-details',
        kwargs={'slug': 'rail'}
    )

    with pytest.raises(HTTPError):
        client.get(url)


@patch('invest.forms.HighPotentialOpportunityForm.save')
@patch('invest.helpers.cms_api_client.lookup_by_slug')
def test_high_potential_opportunity_form_submmit_cms_retrieval_ok(
    mock_lookup_by_slug, mock_save, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_body={
            'opportunity_list': [
                {
                    'pdf_document_url': 'http://www.example.com/a',
                    'heading': 'some great opportunity',
                }
            ]
        }
    )
    mock_save.return_value = create_response(status_code=200)

    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse(
        'high-potential-opportunity-request-form',
        kwargs={'slug': 'rail'}
    )

    response = client.post(url, {
        'full_name': 'Jim Example',
        'role_in_company': 'Chief chief',
        'email_address': 'test@example.com',
        'phone_number': '555',
        'company_name': 'Example corp',
        'website_url': 'example.com',
        'country': choices.COUNTRY_CHOICES[1][0],
        'company_size': '1 - 10',
        'opportunities': [
            'http://www.example.com/a',
        ],
        'comment': 'hello',
        'terms_agreed': True,
    })

    assert response.status_code == 200
    assert response.template_name == (
        views.HighPotentialOpportunityFormView.success_template_name
    )
    assert response.context_data['page']
    assert mock_save.call_count == 1
    assert mock_save.call_args == call(
        template_id=settings.HPO_GOV_NOTIFY_TEMPLATE_ID,
        email_address='test@example.com',
    )
