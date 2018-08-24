from django.urls import reverse

from invest import views


def test_high_potential_opportunity_feature_flag_on(settings, client):

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
