from django.urls import reverse

from euexit import views


def test_international_page_feature_flag_off(client, settings):

    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': False
    }

    response = client.get(reverse('eu-exit-international-contact-form'))

    assert response.status_code == 404


def test_international_page_feature_flag_on(client, settings):

    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'EU_EXIT_FORMS_ON': True
    }

    response = client.get(reverse('eu-exit-international-contact-form'))

    assert response.status_code == 200
    assert response.template_name == [
        views.InternationalContactFormView.template_name
    ]
