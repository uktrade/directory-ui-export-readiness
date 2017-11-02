from django.core.urlresolvers import reverse

from core import views
from casestudy import casestudies


def test_landing_page(client):
    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.LandingPagelView.template_name]
    assert response.context_data['casestudies'] == [
        casestudies.MARKETPLACE,
        casestudies.HELLO_BABY,
        casestudies.YORK,
    ]


def test_sitemaps(client):
    url = reverse('sitemap')

    response = client.get(url)

    assert response.status_code == 200


def test_robots(client):
    url = reverse('robots')

    response = client.get(url)

    assert response.status_code == 200


def test_about(client):
    url = reverse('about')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.AboutView.template_name]
