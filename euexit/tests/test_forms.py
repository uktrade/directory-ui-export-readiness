from unittest import mock

from directory_constants.constants import choices
import pytest

from euexit import forms


@pytest.fixture
def domestic_contact_form_data(captcha_stub):
    return {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'terms_agreed': True,
        'g-recaptcha-response': captcha_stub,
    }


@pytest.fixture
def international_contact_form_data(captcha_stub):
    return {
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
    }


@pytest.mark.parametrize('form_class', (
    forms.InternationalContactForm, forms.DomesticContactForm
))
def test_contact_form_set_field_attributes(form_class):
    form_one = form_class(
        field_attributes={},
        form_url='http://www.form.com',
        subject='subject',
        ingress_url='http://www.ingress.com',
    )
    form_two = form_class(
        field_attributes={
            'first_name': {
                'label': 'Your given name',
            },
            'last_name': {
                'label': 'Your family name'
            }
        },
        form_url='http://www.form.com',
        subject='subject',
        ingress_url='http://www.ingress.com',
    )

    assert form_one.fields['first_name'].label is None
    assert form_one.fields['last_name'].label is None
    assert form_two.fields['first_name'].label == 'Your given name'
    assert form_two.fields['last_name'].label == 'Your family name'


def test_domestic_contact_form_serialize(captcha_stub):
    form = forms.DomesticContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='domestic subject',
        data={
            'first_name': 'test',
            'last_name': 'example',
            'email': 'test@example.com',
            'organisation_type': 'COMPANY',
            'company_name': 'thing',
            'comment': 'hello',
            'terms_agreed': True,
            'g-recaptcha-response': captcha_stub,
        }
    )
    assert form.is_valid()
    assert form.serialized_data == {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'comment': 'hello',
        'form_url': 'http://www.form.com',
        'ingress_url': 'http://www.ingress.com',
    }


def test_international_contact_form_serialize(captcha_stub):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='international subject',
        data={
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
        }
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'first_name': 'test',
        'last_name': 'example',
        'email': 'test@example.com',
        'organisation_type': 'COMPANY',
        'company_name': 'thing',
        'country': choices.COUNTRY_CHOICES[1][0],
        'city': 'London',
        'comment': 'hello',
        'form_url': 'http://www.form.com',
        'ingress_url': 'http://www.ingress.com',
    }


@mock.patch.object(forms.InternationalContactForm, 'send_agent_email')
@mock.patch.object(forms.InternationalContactForm, 'send_user_email')
def test_international_form_save_calls_send_email(
    mock_send_user_email, mock_send_agent_email,
    international_contact_form_data
):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='international subject',
        data=international_contact_form_data
    )
    assert form.is_valid()

    form.save()

    assert mock_send_user_email.call_count == 1
    assert mock_send_agent_email.call_count == 1


@mock.patch.object(forms.DomesticContactForm, 'send_agent_email')
@mock.patch.object(forms.DomesticContactForm, 'send_user_email')
def test_domestic_form_save_calls_send_email(
    mock_send_user_email, mock_send_agent_email,  domestic_contact_form_data
):
    form = forms.DomesticContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='domestic subject',
        data=domestic_contact_form_data
    )

    assert form.is_valid()

    form.save()

    assert mock_send_user_email.call_count == 1
    assert mock_send_agent_email.call_count == 1


@mock.patch.object(forms.InternationalContactForm, 'action_class')
@mock.patch.object(
    forms.InternationalContactForm, 'render_email', return_value='something'
)
def test_international_send_agent_email(
    mock_render_email, mock_email_action, settings,
    international_contact_form_data
):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='international subject',
        data=international_contact_form_data
    )

    assert form.is_valid()

    form.send_agent_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == mock.call(
        recipients=[settings.EUEXIT_AGENT_EMAIL],
        subject='international subject',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )

    assert mock_render_email.call_count == 2
    assert mock_render_email.call_args_list == [
        mock.call('euexit/email-confirmation-agent.txt'),
        mock.call('euexit/email-confirmation-agent.html')
    ]
    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == mock.call(
        {'text_body':  'something', 'html_body': 'something'}
    )


@mock.patch.object(forms.DomesticContactForm, 'action_class')
@mock.patch.object(
    forms.DomesticContactForm, 'render_email', return_value='something'
)
def test_domestic_send_agent_email(
    mock_render_email, mock_email_action, settings, domestic_contact_form_data
):
    form = forms.DomesticContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='domestic subject',
        data=domestic_contact_form_data
    )

    assert form.is_valid()

    form.send_user_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == mock.call(
        recipients=[domestic_contact_form_data['email']],
        subject='domestic subject',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )

    assert mock_render_email.call_count == 1
    assert mock_render_email.call_args == mock.call(
        'euexit/email-confirmation-user.txt'
    )

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == mock.call(
        {'text_body':  'something', 'html_body': 'something'}
    )


def test_render_agent_email_context(international_contact_form_data):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='international subject',
        data=international_contact_form_data
    )

    assert form.is_valid()

    html = form.render_email('euexit/email-confirmation-agent.html')

    assert 'http://www.ingress.com' in html
    assert 'http://www.form.com' in html


@mock.patch.object(forms.InternationalContactForm, 'action_class')
@mock.patch.object(
    forms.InternationalContactForm, 'render_email', return_value='something'
)
def test_international_send_user_email(
    mock_render_email, mock_email_action, settings,
    international_contact_form_data
):
    form = forms.InternationalContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='international subject',
        data=international_contact_form_data
    )

    assert form.is_valid()

    form.send_user_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == mock.call(
        recipients=[international_contact_form_data['email']],
        subject='international subject',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )

    assert mock_render_email.call_count == 1
    assert mock_render_email.call_args == mock.call(
        'euexit/email-confirmation-user.txt'
    )

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == mock.call(
        {'text_body':  'something', 'html_body': 'something'}
    )


@mock.patch.object(forms.DomesticContactForm, 'action_class')
@mock.patch.object(
    forms.DomesticContactForm, 'render_email', return_value='something'
)
def test_domestic_send_user_email(
    mock_render_email, mock_email_action, settings, domestic_contact_form_data
):
    form = forms.DomesticContactForm(
        field_attributes={},
        form_url='http://www.form.com',
        ingress_url='http://www.ingress.com',
        subject='domestic subject',
        data=domestic_contact_form_data
    )

    assert form.is_valid()

    form.send_user_email()

    assert mock_email_action.call_count == 1
    assert mock_email_action.call_args == mock.call(
        recipients=[domestic_contact_form_data['email']],
        subject='domestic subject',
        reply_to=[settings.DEFAULT_FROM_EMAIL],
    )

    assert mock_render_email.call_count == 1
    assert mock_render_email.call_args == mock.call(
        'euexit/email-confirmation-user.txt'
    )

    assert mock_email_action().save.call_count == 1
    assert mock_email_action().save.call_args == mock.call(
        {'text_body':  'something', 'html_body': 'something'}
    )
