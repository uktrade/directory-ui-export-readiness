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
    assert response.context_data['article_group_read_progress'] == {
        'all': {
            'read': 0, 'total': 41
        },
        'business_planning': {
            'read': 0, 'total': 10
        },
        'customer_insights': {
            'read': 0, 'total': 4
        },
        'finance': {
            'read': 0, 'total': 7
        },
        'getting_paid': {
            'read': 0, 'total': 5
        },
        'market_research': {
            'read': 0, 'total': 5
        },
        'operations_and_compliance': {
            'read': 0, 'total': 10
        },
        'persona_new': {
            'read': 0, 'total': 14
        },
        'persona_occasional': {
            'read': 0, 'total': 34
        },
        'persona_regular': {
            'read': 0, 'total': 17
        }
    }


def test_sitemaps(client):
    url = reverse('sitemap')

    response = client.get(url)

    assert response.status_code == 200


def test_robots(client):
    url = reverse('robots')

    response = client.get(url)

    assert response.status_code == 200
