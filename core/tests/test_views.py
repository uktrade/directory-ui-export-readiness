import http

from django.core.urlresolvers import reverse
from django.conf import settings

from bs4 import BeautifulSoup
import pytest

from core import views
from casestudy import casestudies


def test_landing_page(client):
    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [views.LandingPageView.template_name]
    assert response.context_data['casestudies'] == [
        casestudies.MARKETPLACE,
        casestudies.HELLO_BABY,
        casestudies.YORK,
    ]
    assert response.context_data['article_group_read_progress'] == {
        'all': {'read': 0, 'total': 45},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 0, 'total': 5},
        'market_research': {'read': 0, 'total': 5},
        'operations_and_compliance': {'read': 0, 'total': 10},
        'persona_new': {'read': 0, 'total': 18},
        'persona_occasional': {'read': 0, 'total': 38},
        'persona_regular': {'read': 0, 'total': 18},
    }


def test_interstitial_page_exopps(client):
    url = reverse('export-opportunities')
    response = client.get(url)
    context = response.context_data

    assert response.status_code == 200
    assert context['exopps_url'] == settings.SERVICES_EXOPPS_ACTUAL

    heading = '<h1>Export Opportunities</h1>'
    expected = str(BeautifulSoup(heading, 'html.parser'))
    button_text = 'Go to Export Opportunities'
    html_page = str(BeautifulSoup(response.content, 'html.parser'))

    assert expected in html_page
    assert button_text in html_page


def test_sitemaps(client):
    url = reverse('sitemap')

    response = client.get(url)

    assert response.status_code == 200


def test_robots(client):
    url = reverse('robots')

    response = client.get(url)

    assert response.status_code == 200


@pytest.mark.parametrize(
    'view,expected_template',
    (
        ('about', 'core/about.html'),
        ('privacy-cookies', 'core/privacy_cookies.html'),
        ('landing-page-international', 'core/landing_page_international.html'),
        ('sorry', 'core/sorry.html'),
        ('not-found', 'core/not_found.html'),
        ('terms-conditions', 'core/terms_conditions.html'),
        ('get-finance', 'core/get_finance.html')
    )
)
def test_templates(view, expected_template, client):
    url = reverse(view)

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize("lang", ['ar', 'es', 'zh-hans', 'pt', 'de', 'ja'])
def test_international_landing_view_translations(lang, client):
    response = client.get(
        reverse('landing-page-international'),
        {'lang': lang}
    )

    assert response.status_code == http.client.OK
    assert response.cookies['django_language'].value == lang


def test_international_landing_view_translations_bidi(client):
    response = client.get(
        reverse('landing-page-international'),
        {'lang': 'ar'}
    )

    assert response.status_code == http.client.OK
    assert response.template_name == [
        views.InternationalLandingPageView.template_name_bidi
    ]
