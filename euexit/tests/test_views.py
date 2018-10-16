from unittest import mock
from urllib.parse import urljoin

from directory_constants.constants import choices
import pytest

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


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_international_form_feature_flag_on(
    mock_lookup_by_slug, client, settings
):
    mock_lookup_by_slug.return_value = create_response(status_code=200)
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


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(
    views.InternationalContactFormView.form_class, 'action_class'
)
def test_international_form_submit(
    mock_action_class, mock_lookup_by_slug, settings, client, captcha_stub
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }
    settings.EU_EXIT_ZENDESK_SUBDOMAIN = 'eu-exit-subdomain'

    url = reverse('eu-exit-international-contact-form')

    # sets referrer in the session
    client.get(url, {}, HTTP_REFERER='http://www.google.com')
    response = client.post(url, {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRY_CHOICES[1][0],
        'city': 'London',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'eu-exit-international-contact-form-success'
    )

    assert mock_action_class.call_count == 1
    assert mock_action_class.call_args == mock.call(
        email_address='test@example.com',
        full_name='test example',
        subject='EU Exit international contact form',
        subdomain='eu-exit-subdomain',
    )
    assert mock_action_class().save.call_count == 1
    assert mock_action_class().save.call_args == mock.call({
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': 'AL',
        'city': 'London',
        'comment': 'hello',
        'form_url': 'http://testserver/eu-exit/international/contact/',
        'ingress_url': 'http://www.google.com',
    })


@pytest.mark.parametrize('url,template_name', [
    (
        reverse('eu-exit-international-contact-form-success'),
        views.InternationalContactSuccessView.template_name
    ),
    (
        reverse('eu-exit-domestic-contact-form-success'),
        views.DomesticContactSuccessView.template_name
    ),
])
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_success_page(
    mock_lookup_by_slug, settings, client, url, template_name
):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={'body_text': 'what next'}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [template_name]
    assert response.context_data['page'] == {'body_text': 'what next'}


def test_domestic_form_feature_flag_off(client, settings):

    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': False
    }

    response = client.get(reverse('eu-exit-domestic-contact-form'))

    assert response.status_code == 404


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_form_feature_flag_on(
    mock_lookup_by_slug, client, settings
):
    mock_lookup_by_slug.return_value = create_response(status_code=200)
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': True
    }

    response = client.get(reverse('eu-exit-domestic-contact-form'))

    assert response.status_code == 200
    assert response.template_name == [
        views.DomesticContactFormView.template_name
    ]


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_form_not_found(
    mock_lookup_by_slug, settings, client
):
    mock_lookup_by_slug.return_value = create_response(status_code=404)
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': True
    }

    url = reverse('eu-exit-domestic-contact-form')
    response = client.get(url)

    assert response.status_code == 404


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_domestic_form_cms_retrieval_ok(
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

    url = reverse('eu-exit-domestic-contact-form')

    response = client.get(url)

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.fields['first_name'].label == 'Given name'
    assert form.fields['last_name'].label == 'Family name'


@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@mock.patch.object(views.DomesticContactFormView.form_class, 'action_class')
def test_domestic_form_submit(
    mock_action_class, mock_lookup_by_slug, settings, client, captcha_stub
):
    settings.EU_EXIT_ZENDESK_SUBDOMAIN = 'eu-exit-subdomain'
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    url = reverse('eu-exit-domestic-contact-form')

    # sets referrer in the session
    client.get(url, {}, HTTP_REFERER='http://www.google.com')
    response = client.post(url, {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'eu-exit-domestic-contact-form-success'
    )
    assert mock_action_class.call_count == 1
    assert mock_action_class.call_args == mock.call(
        email_address='test@example.com',
        full_name='test example',
        subject='EU Exit contact form',
        subdomain='eu-exit-subdomain',
    )
    assert mock_action_class().save.call_count == 1
    assert mock_action_class().save.call_args == mock.call({
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'form_url': 'http://testserver/eu-exit/contact/',
        'ingress_url': 'http://www.google.com',
    })


@pytest.mark.parametrize('url', (
    reverse('eu-exit-international-contact-form'),
    reverse('eu-exit-domestic-contact-form'),
))
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_urls(mock_lookup_by_slug, settings, client, url):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    response = client.get(url, {}, HTTP_REFERER='http://www.google.com')

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.form_url == urljoin('http://testserver', url)
    assert form.ingress_url == 'http://www.google.com'


@pytest.mark.parametrize('url', (
    reverse('eu-exit-international-contact-form'),
    reverse('eu-exit-domestic-contact-form'),
))
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_form_urls_no_referer(mock_lookup_by_slug, settings, client, url):
    mock_lookup_by_slug.return_value = create_response(
        status_code=200, json_body={}
    )
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'HIGH_POTENTIAL_OPPORTUNITIES_ON': True
    }

    response = client.get(url, {})

    assert response.status_code == 200
    form = response.context_data['form']
    assert form.form_url == urljoin('http://testserver', url)
    assert form.ingress_url is None
