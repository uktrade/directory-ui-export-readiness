from unittest.mock import ANY, call, Mock, patch

import pytest

from django.urls import reverse

from contact import helpers, views


def test_service_agnostic_interstitial_view_remembers_referer(client):
    response = client.get(
        reverse('contact-us-interstitial-service-agnostic'),
        {},
        HTTP_REFERER='example.com',
    )

    assert response.status_code == 200
    assert response.template_name == [views.InterstitialView.template_name]
    assert client.session[helpers.INGRESS_URL_SESSION_KEY] == 'example.com'


def test_service_specific_interstitial_view_remembers_referer(client):
    response = client.get(
        reverse(
            'contact-us-interstitial-service-specific',
            kwargs={'service': 'directory'},
        ),
        {},
        HTTP_REFERER='example.com',
    )

    assert response.status_code == 200
    assert response.template_name == [views.InterstitialView.template_name]
    assert client.session[helpers.INGRESS_URL_SESSION_KEY] == 'example.com'


@patch('contact.helpers.create_zendesk_ticket')
@patch('captcha.fields.ReCaptchaField.clean', Mock)
def test_submit_triage(mock_create_zendesk_ticket, client, captcha_stub):
    view = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    
    url = reverse(
        'contact-us-triage-wizard', kwargs={'service': 'directory'}
    )
    response = client.post(url, {
        view_name + '-current_step': view.BUSINESS,
        view.BUSINESS + '-company_name': 'Example corp',
        view.BUSINESS + '-company_number': '1234567',
        view.BUSINESS + '-soletrader': 'True',
        view.BUSINESS + '-company_postcode': 'dn55 2ds',
        view.BUSINESS + '-website_address': 'http://www.goo.com',
    })
    assert response.status_code == 200
    assert response.template_name == [view.templates[view.DETAILS]]

    response = client.post(url, {
        view_name + '-current_step': view.DETAILS,
        view.DETAILS + '-turnover': 'Under 100k',
        view.DETAILS + '-sku_count': '2',
        view.DETAILS + '-trademarked': 'True',
    })
    assert response.status_code == 200
    assert response.template_name == [view.templates[view.EXPERIENCE]]

    response = client.post(url, {
        view_name + '-current_step': view.EXPERIENCE,
        view.EXPERIENCE + '-experience': 'Yes, regularly',
        view.EXPERIENCE + '-description': 'good',
    })
    assert response.status_code == 200
    assert response.template_name == [view.templates[view.CONTACT]]

    response = client.post(url, {
        view_name + '-current_step': view.CONTACT,
        view.CONTACT + '-contact_name': 'Jim Example',
        view.CONTACT + '-contact_email': 'jim@example.com',
        view.CONTACT + '-contact_phone': '07504747474',
        view.CONTACT + '-email_pref': 'True',
        'recaptcha_response_field': captcha_stub,
    })
    assert response.status_code == 200
    assert response.template_name == view.templates[view.SUCCESS]

    assert mock_create_zendesk_ticket.call_count == 1
    assert mock_create_zendesk_ticket.call_args == call(
        cleaned_data={
            'turnover': 'Under 100k',
            'contact_email': 'jim@example.com',
            'contact_name': 'Jim Example',
            'trademarked': True,
            'company_name': 'Example corp',
            'contact_phone': '07504747474',
            'sku_count': '2',
            'experience': 'Yes, regularly',
            'website_address': 'http://www.goo.com',
            'description': 'good',
            'soletrader': True,
            'company_number': '01234567',
            'email_pref': True,
            'company_postcode': 'dn55 2ds',
            'captcha': ANY,
        },
        ingress_url='Direct request',
        service='directory'
    )


@pytest.mark.parametrize('url,service', (
    (
        reverse('contact-us-service-specific', kwargs={'service': 'invest'}),
        'invest'
    ),
    (
        reverse('contact-us-service-agnostic'),
        None
    )
))
@patch('captcha.fields.ReCaptchaField.clean', Mock)
@patch('contact.helpers.create_zendesk_ticket')
def test_submit_feedback(
    mock_create_zendesk_ticket, url, service, client, captcha_stub
):
    view = views.FeedbackWizardFormView
    view_name = 'feedback_wizard_form_view'

    response = client.post(url, {
        view_name + '-current_step': view.FEEDBACK,
        view.FEEDBACK + '-contact_name': 'Jim example',
        view.FEEDBACK + '-contact_email': 'jim@example.com',
        view.FEEDBACK + '-feedback': 'hello',
        'recaptcha_response_field': captcha_stub,
    })

    assert response.status_code == 200
    assert response.template_name == view.templates[view.SUCCESS]

    assert mock_create_zendesk_ticket.call_count == 1
    assert mock_create_zendesk_ticket.call_args == call(
        cleaned_data={
            'contact_email': 'jim@example.com',
            'contact_name': 'Jim example',
            'captcha': ANY,
            'feedback': 'hello'
        },
        ingress_url='Direct request',
        service=service,
    )
