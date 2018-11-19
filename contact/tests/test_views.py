from unittest import mock

from directory_constants.constants import cms
import pytest

from django import forms
from django.conf import settings
from django.urls import reverse

from contact import constants, views
from core.tests.helpers import create_response


def build_wizard_url(step):
    return reverse('triage-wizard', kwargs={'step': step})


class ChoiceForm(forms.Form):
    choice = forms.CharField()


@pytest.fixture
def domestic_form_data(captcha_stub):
    return {
        'given_name': 'Test',
        'family_name': 'Example',
        'email': 'test@example.com',
        'company_type': 'LIMITED',
        'organisation_name': 'Example corp',
        'postcode': '**** ***',
        'comment': 'Help please',
        'g-recaptcha-response': captcha_stub,
        'terms_agreed': True,
    }


@pytest.mark.parametrize('current_step,choice,expected_url', (
    # location step routing
    (
        constants.LOCATION,
        constants.DOMESTIC,
        build_wizard_url(constants.DOMESTIC),
    ),
    (
        constants.LOCATION,
        constants.INTERNATIONAL,
        build_wizard_url(constants.INTERNATIONAL),
    ),
    # domestic step routing
    (
        constants.DOMESTIC,
        constants.TRADE_OFFICE,
        settings.FIND_TRADE_OFFICE_URL,
    ),
    (
        constants.DOMESTIC,
        constants.EXPORT_ADVICE,
        reverse('contact-us-export-advice'),
    ),
    (
        constants.DOMESTIC,
        constants.FINANCE,
        reverse(
            'uk-export-finance-lead-generation-form',
            kwargs={'step': 'contact'},
        )
    ),
    (
        constants.DOMESTIC,
        constants.EUEXIT,
        reverse('eu-exit-domestic-contact-form'),
    ),
    (
        constants.DOMESTIC,
        constants.EVENTS,
        reverse('contact-us-events-form'),
    ),
    (
        constants.DOMESTIC,
        constants.DSO,
        reverse('contact-us-domestic')
    ),
    (
        constants.DOMESTIC,
        constants.OTHER,
        reverse('contact-us-domestic')
    ),
    # great services guidance routing
    (
        constants.GREAT_SERVICES,
        constants.EXPORT_OPPORTUNITIES,
        build_wizard_url(constants.EXPORT_OPPORTUNITIES),
    ),
    (
        constants.GREAT_SERVICES,
        constants.GREAT_ACCOUNT,
        build_wizard_url(constants.GREAT_ACCOUNT),
    ),
    (
        constants.GREAT_SERVICES,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_EMAIL,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_MISSING_VERIFY_EMAIL_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.PASSWORD_RESET,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_PASSWORD_RESET_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.COMPANIES_HOUSE_LOGIN,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_COMPANIES_HOUSE_LOGIN_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.VERIFICATION_CODE,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_ENTER_SLUG
        ),
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.NO_VERIFICATION_LETTER,
        views.build_great_account_guidance_url(
            cms.EXPORT_READINESS_HELP_VERIFICATION_CODE_LETTER_SLUG
        )
    ),
    (
        constants.GREAT_ACCOUNT,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # Export opportunities guidance routing
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.NO_RESPONSE,
        reverse('contact-us-domestic'),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.ALERTS,
        views.build_export_opportunites_guidance_url(
            cms.EXPORT_READINESS_HELP_EXOPP_ALERTS_IRRELEVANT_SLUG
        ),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.MORE_DETAILS,
        reverse('contact-us-domestic'),
    ),
    (
        constants.EXPORT_OPPORTUNITIES,
        constants.OTHER,
        reverse('contact-us-domestic'),
    ),
    # international routing
    (
        constants.INTERNATIONAL,
        constants.INVESTING,
        settings.INVEST_CONTACT_URL,
    ),
    (
        constants.INTERNATIONAL,
        constants.BUYING,
        reverse('contact-us-find-uk-companies'),
    ),
    (
        constants.INTERNATIONAL,
        constants.EUEXIT,
        reverse('eu-exit-international-contact-form'),
    ),
    (
        constants.INTERNATIONAL,
        constants.OTHER,
        reverse('contact-us-international'),
    ),
))
def test_render_next_step(current_step, choice, expected_url):
    form = ChoiceForm(data={'choice': choice})

    view = views.RoutingFormView()
    view.steps = mock.Mock(current=current_step)
    view.storage = mock.Mock()
    view.url_name = 'triage-wizard'

    assert form.is_valid()
    assert view.render_next_step(form).url == expected_url


@pytest.mark.parametrize(
    'url,success_url,view_class,agent_template,user_template,agent_email', (
    (
        reverse('contact-us-events-form'),
        reverse('contact-us-events-success'),
        views.EventsFormView,
        settings.CONTACT_EVENTS_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_EVENTS_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_EVENTS_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-dso-form'),
        reverse('contact-us-dso-success'),
        views.DefenceAndSecurityOrganisationFormView,
        settings.CONTACT_DSO_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DSO_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DSO_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-domestic'),
        reverse('contact-us-domestic-success'),
        views.DomesticFormView,
        settings.CONTACT_DIT_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DIT_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-international'),
        reverse('contact-us-international-success'),
        views.InternationalFormView,
        settings.CONTACT_INTERNATIONAL_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_INTERNATIONAL_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_INTERNATIONAL_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-find-uk-companies'),
        reverse('contact-us-find-uk-companies-success'),
        views.BuyingFromUKCompaniesFormView,
        settings.CONTACT_BUYING_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_BUYING_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_BUYING_AGENT_EMAIL_ADDRESS,
    ),
    (
        reverse('contact-us-export-advice'),
        reverse('contact-us-export-advice-success'),
        views.ExportingAdviceFormView,
        settings.CONTACT_DIT_AGENT_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DIT_USER_NOTIFY_TEMPLATE_ID,
        settings.CONTACT_DIT_AGENT_EMAIL_ADDRESS,
    ),
))
def test_notify_form_submit_success(
    client, url, agent_template, user_template, view_class, agent_email,
    success_url
):
    class Form(forms.Form):
        email = forms.EmailField()
        save = mock.Mock()

    with mock.patch.object(view_class, 'form_class', Form):
        response = client.post(url, {'email': 'test@example.com'})

    assert response.status_code == 302
    assert response.url == success_url

    assert Form.save.call_count == 2
    assert Form.save.call_args_list == [
        mock.call(
            template_id=agent_template,
            email_address=agent_email,
        ),
        mock.call(
            template_id=user_template,
            email_address='test@example.com',
        )
    ]


@pytest.mark.parametrize('url,slug', (
    (
        reverse('contact-us-events-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_EVENTS_SLUG,
    ),
    (
        reverse('contact-us-dso-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_DSO_SLUG,
    ),
    (
        reverse('contact-us-export-advice-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_EXPORT_ADVICE_SLUG,
    ),
    (
        reverse('contact-us-feedback-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_FEEDBACK_SLUG,
    ),
    (
        reverse('contact-us-find-uk-companies-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_FIND_COMPANIES_SLUG,
    ),
    (
        reverse('contact-us-domestic-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_SLUG,
    ),
    (
        reverse('contact-us-international-success'),
        cms.EXPORT_READINESS_CONTACT_US_FORM_SUCCESS_INTERNATIONAL_SLUG,
    )
))
@mock.patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_success_view_cms(mock_lookup_by_slug, url, slug, client):

    mock_lookup_by_slug.return_value = create_response(
        status_code=200,
        json_body={}
    )

    response = client.get(url)

    assert response.status_code == 200
    assert mock_lookup_by_slug.call_count == 1
    assert mock_lookup_by_slug.call_args == mock.call(
        draft_token=None, language_code='en-gb', slug=slug
    )
