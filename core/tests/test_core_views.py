from django.core.urlresolvers import reverse

from core import views


def test_landing_page(client):
    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.LandingPagelView.template_name]
