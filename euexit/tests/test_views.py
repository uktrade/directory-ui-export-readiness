from unittest import mock

from django.urls import reverse

from core.tests.helpers import create_response
from euexit import views


def test_international_form_feature_flag_off(client, settings):

    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': False
    }

    response = client.get(reverse('eu-exit-international-contact-form'))

    assert response.status_code == 404


def test_international_form_feature_flag_on(client, settings):

    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': True
    }

    response = client.get(reverse('eu-exit-international-contact-form'))

    assert response.status_code == 200
    assert response.template_name == [
        views.InternationalContactFormView.template_name
    ]


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_form_not_found(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=404)
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': True
    }

    url = reverse('eu-exit-international-contact-form')
    response = client.get(url)

    assert response.status_code == 404


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_form_cms_retrieval_ok(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={
            'first_name': {
                'label': 'Given name'
            },
            'last_name': {
                'label': 'Family name'
            },
        }
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse('eu-exit-international-contact-form')

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['first_name'].label == 'Given name'
    assert form.fields['last_name'].label == 'Family name'
