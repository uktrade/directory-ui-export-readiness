import http

from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import TemplateView

from bs4 import BeautifulSoup
import pytest
import requests_mock

from core import views
from casestudy import casestudies


def test_landing_page(client, settings):
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
        'custom_persona_new': {'read': 0, 'total': 18},
        'custom_persona_occasional': {'read': 0, 'total': 38},
        'custom_persona_regular': {'read': 0, 'total': 18},
    }


def test_interstitial_page_exopps(client):
    url = reverse('export-opportunities')
    response = client.get(url)
    context = response.context_data

    assert response.status_code == 200
    assert context['exopps_url'] == settings.SERVICES_EXOPPS_ACTUAL

    heading = '<h1 class="heading-xlarge">Export opportunities</h1>'
    expected = str(BeautifulSoup(heading, 'html.parser'))
    button_text = 'Find export opportunities'
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
        (
            'about',
            'core/about.html'
        ),
        (
            'privacy-and-cookies',
            'core/privacy_cookies-domestic.html'
        ),
        (
            'privacy-and-cookies-international',
            'core/privacy_cookies-international.html'),
        (
            'terms-and-conditions',
            'core/terms_conditions-domestic.html'
        ),
        (
            'terms-and-conditions-international',
            'core/terms_conditions-international.html'
        ),
        (
            'landing-page-international',
            'core/landing_page_international.html'
        ),
        (
            'not-found',
            'core/not_found.html'
        ),
        (
            'get-finance',
            'core/get_finance.html'
        )
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


@pytest.mark.parametrize('method,expected', (
    ('get', '"aa579dae951f3cc5d696e5359261e123"'),
    ('post', None),
    ('patch', None),
    ('put', None),
    ('delete', None),
    ('head', None),
    ('options', None),
))
def test_set_etag_mixin(rf, method, expected):
    class MyView(views.SetEtagMixin, TemplateView):

        template_name = 'core/robots.txt'

        def post(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def patch(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def put(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def delete(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def head(self, *args, **kwargs):
            return super().get(*args, **kwargs)

        def options(self, *args, **kwargs):
            return super().get(*args, **kwargs)

    request = getattr(rf, method)('/')
    request.sso_user = None
    view = MyView.as_view()
    response = view(request)

    response.render()
    assert response.get('Etag') == expected


@pytest.mark.parametrize('view_class', views.SetEtagMixin.__subclasses__())
def test_cached_views_not_dynamic(rf, settings, view_class):
    # exception will be raised if the views perform http request, which are an
    # indicator that the views rely on dynamic data.
    with requests_mock.mock():
        view = view_class.as_view()
        request = rf.get('/')
        request.LANGUAGE_CODE = 'en-gb'
        # highlights if the view tries to interact with the session, which is
        # also an indicator that the view relies on dynamic data.
        request.session = None
        response = view(request)
        assert response.status_code == 200


def test_about_view(client):
    response = client.get(reverse('about'))

    assert response.status_code == 200
    assert response.template_name == [views.AboutView.template_name]


def test_privacy_view_domestic(client):
    response = client.get(reverse('privacy-and-cookies'))

    assert response.status_code == 200
    assert response.template_name == [
        views.PrivacyCookiesDomestic.template_name
    ]


def test_privacy_view_domestic_about_cookies_link_correct(client):
    response = client.get(reverse('privacy-and-cookies'))

    assert response.status_code == 200
    assert (
        '<a href="http://www.aboutcookies.org.uk">'
        'www.aboutcookies.org.uk</a>'
    ) in str(response.content)


def test_terms_and_conditions_view_domestic(client):
    response = client.get(reverse('terms-and-conditions'))

    assert response.status_code == 200
    assert response.template_name == [
        views.TermsConditionsDomestic.template_name
    ]


def test_privacy_view_international(client):
    response = client.get(reverse('privacy-and-cookies-international'))

    assert response.status_code == 200
    assert response.template_name == [
        views.PrivacyCookiesInternational.template_name
    ]


def test_terms_and_conditions_view_international(client):
    response = client.get(reverse('terms-and-conditions-international'))

    assert response.status_code == 200
    assert response.template_name == [
        views.TermsConditionsInternational.template_name
    ]
