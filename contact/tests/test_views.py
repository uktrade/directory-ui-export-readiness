from unittest import mock

from directory_constants.constants import urls
import pytest

from django import forms
from django.conf import settings
from django.urls import reverse

from contact import constants, views


def build_wizard_url(step):
    return reverse('triage-wizard', kwargs={'step': step})


class ChoiceForm(forms.Form):
    choice = forms.CharField()


@pytest.mark.parametrize('current_step,choice,expected_url', (
    # location step
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
    # domestic step
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
        reverse('contact-us-finance-form'),
    ),
    (
        constants.DOMESTIC,
        constants.EUEXIT,
        reverse('eu-exit-domestic-contact-form'),
    ),
    (
        constants.DOMESTIC,
        constants.EVENTS,
        urls.SERVICES_EVENTS,
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
    # great services
    (
        constants.GREAT_SERVICES,
        constants.EXPORT_OPPORTUNITIES,
        build_wizard_url(constants.EXPORT_OPPORTUNITIES)
    ),
    (
        constants.GREAT_SERVICES,
        constants.GREAT_ACCOUNT,
        build_wizard_url(constants.GREAT_ACCOUNT)
    ),
    # constants.GREAT_ACCOUNT is not supported yet
    # constants.EXPORT_OPPORTUNITIES is not supported yet
    # international
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
