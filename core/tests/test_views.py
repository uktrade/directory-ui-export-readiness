import http
from unittest.mock import call, patch, PropertyMock

from django.core.urlresolvers import reverse
from django.conf import settings
from django.views.generic import TemplateView

from bs4 import BeautifulSoup
import pytest
import requests_mock

from core import helpers, views
from core.tests.helpers import create_response
from casestudy import casestudies

from directory_cms_client.constants import (
    EXPORT_READINESS_TERMS_AND_CONDITIONS_SLUG,
    EXPORT_READINESS_PRIVACY_AND_COOKIES_SLUG,
)


def test_landing_page_video_url(client, settings):
    settings.LANDING_PAGE_VIDEO_URL = 'https://example.com/videp.mp4'
    url = reverse('landing-page')

    response = client.get(url)

    assert response.context_data['LANDING_PAGE_VIDEO_URL'] == (
        'https://example.com/videp.mp4'
    )
    assert b'https://example.com/videp.mp4' in response.content


@patch(
    'core.helpers.GeoLocationRedirector.should_redirect',
    PropertyMock(return_value=True)
)
@patch(
    'core.helpers.GeoLocationRedirector.country_language',
    PropertyMock(return_value='fr')
)
def test_landing_page_redirect(client):
    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 302
    assert response.url == (
        reverse('landing-page-international') + '?lang=' + 'fr'
    )
    assert response.cookies[helpers.GeoLocationRedirector.COOKIE_NAME].value


def test_landing_page(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': False,
    }

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
        'all': {'read': 0, 'total': 49},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 0, 'total': 5},
        'market_research': {'read': 0, 'total': 7},
        'operations_and_compliance': {'read': 0, 'total': 12},
        'persona_new': {'read': 0, 'total': 23},
        'persona_occasional': {'read': 0, 'total': 42},
        'persona_regular': {'read': 0, 'total': 21},
        'custom_persona_new': {'read': 0, 'total': 23},
        'custom_persona_occasional': {'read': 0, 'total': 42},
        'custom_persona_regular': {'read': 0, 'total': 21},
    }


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_landing_page_template_news_feature_flag_on(
    mock_get_page, client, settings
):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }

    page = {
        'news_title': 'News',
        'news_description': '<p>Lorem ipsum</p>',
        'articles': [
            {'article_title': 'News article 1'},
            {'article_title': 'News article 2'},
        ],
    }

    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )

    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.PrototypeLandingPageView.template_name]


def test_landing_page_template_news_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': False,
    }

    url = reverse('landing-page')

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [
        views.LandingPageView.template_name]


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
            'landing-page-international',
            'core/landing_page_international.html'
        ),
        (
            'not-found',
            '404.html'
        ),
    )
)
def test_templates(view, expected_template, client):
    url = reverse(view)

    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize(
    'view,expected_template',
    (
        (
            'terms-and-conditions',
            'core/info_page.html'
        ),
        (
            'terms-and-conditions-international',
            'core/info_page_international.html'
        ),
    )
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_terms_conditions_cms(
    mock_get_t_and_c_page, view, expected_template, client
):
    url = reverse(view)
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
    }
    mock_get_t_and_c_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


@pytest.mark.parametrize(
    'view,expected_template',
    (
        (
            'privacy-and-cookies',
            'core/info_page.html'
        ),
        (
            'privacy-and-cookies-international',
            'core/info_page_international.html'
        ),
    )
)
@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_privacy_cookies_cms(
    mock_get_p_and_c_page, view, expected_template, client
):
    url = reverse(view)
    page = {
        'title': 'the page',
        'industries': [{'title': 'good 1'}],
        'meta': {'languages': ['en-gb']},
    }
    mock_get_p_and_c_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [expected_template]


def test_international_landing_page_news_section_on(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': True,
    }
    url = reverse('landing-page-international')
    response = client.get(url)

    assert 'EU Exit updates' in str(response.content)


def test_international_landing_page_news_section_off(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'NEWS_SECTION_ON': False,
    }
    url = reverse('landing-page-international')
    response = client.get(url)

    assert 'EU Exit updates' not in str(response.content)


@pytest.mark.parametrize("lang", ['ar', 'es', 'zh-hans', 'pt', 'de', 'ja'])
def test_international_landing_view_translations(lang, client):
    response = client.get(
        reverse('landing-page-international'),
        {'lang': lang}
    )

    assert response.status_code == http.client.OK
    assert response.cookies['django_language'].value == lang


@pytest.mark.parametrize('method,expected', (
    ('get', '"b013a413446c5dddaf341792c63a88c4"'),
    ('post', None),
    ('patch', None),
    ('put', None),
    ('delete', None),
    ('head', None),
    ('options', None),
))
def test_set_etag_mixin(rf, method, expected):
    class MyView(views.SetEtagMixin, TemplateView):

        template_name = 'robots.txt'

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


cms_urls_slugs = (
    (
        reverse('privacy-and-cookies'),
        EXPORT_READINESS_PRIVACY_AND_COOKIES_SLUG,
    ),
    (
        reverse('terms-and-conditions'),
        EXPORT_READINESS_TERMS_AND_CONDITIONS_SLUG,
    ),
    (
        reverse('privacy-and-cookies-international'),
        EXPORT_READINESS_PRIVACY_AND_COOKIES_SLUG,
    ),
    (
        reverse('terms-and-conditions-international'),
        EXPORT_READINESS_TERMS_AND_CONDITIONS_SLUG,
    ),
)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@pytest.mark.parametrize('url,slug', cms_urls_slugs)
def test_cms_pages_cms_client_params(mock_get, client, url, slug):
    mock_get.return_value = create_response(status_code=200)

    response = client.get(url, {'draft_token': '123'})

    assert response.status_code == 200
    assert mock_get.call_count == 1
    assert mock_get.call_args == call(
        slug=slug,
        draft_token='123',
        language_code='en-gb'
    )


cms_urls = (
    reverse('privacy-and-cookies'),
    reverse('terms-and-conditions'),
    reverse('privacy-and-cookies-international'),
    reverse('terms-and-conditions-international'),
)


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
@pytest.mark.parametrize('url', cms_urls)
def test_cms_pages_cms_page_404(mock_get, client, url):
    mock_get.return_value = create_response(status_code=404)

    response = client.get(url)

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_performance_dashboard_cms(mock_get_page, settings, client):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PERFORMANCE_DASHBOARD_ON': True,
    }
    url = reverse('performance-dashboard')
    page = {
        'title': 'Performance dashboard',
        'heading': 'Great.gov.uk',
        'description': 'Lorem ipsum dolor sit amet.',
    }
    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert page['title'] in str(response.content)
    assert page['heading'] in str(response.content)
    assert page['description'] in str(response.content)

    assert response.status_code == 200
    assert response.template_name == ['core/performance_dashboard.html']


def test_performance_dashboard_feature_flag_off(client, settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'PERFORMANCE_DASHBOARD_ON': False
    }

    response = client.get('performance-dashboard')

    assert response.status_code == 404


@patch('directory_cms_client.client.cms_api_client.lookup_by_slug')
def test_privacy_cookies_subpage(mock_get_page, client, settings):
    url = reverse('privacy-and-cookies-subpage', kwargs={
        'slug': 'fair-processing-notice-zendesk'
    })
    page = {
        'title': 'Fair Processing Notice Zendesk',
        'body': 'Lorem ipsum dolor sit amet.',
    }
    mock_get_page.return_value = create_response(
        status_code=200,
        json_body=page
    )
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == ['core/privacy_subpage.html']

    assert page['title'] in str(response.content)
    assert page['body'] in str(response.content)
