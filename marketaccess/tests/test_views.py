from django.conf import settings

from django.urls import reverse

from core.tests.helpers import create_response
from marketaccess import views


def test_form_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_FORM_ON'] = False

    response = client.get(reverse('market-access'))

    assert response.status_code == 404


def test_form_feature_flag_on(client, settings):
    settings.FEATURE_FLAGS['MARKET_ACCESS_FORM_ON'] = True

    response = client.get(reverse('market-access'))

    assert response.status_code == 200
