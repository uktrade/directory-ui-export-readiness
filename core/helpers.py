import urllib.parse

from directory_api_client.client import api_client
from ipware import get_client_ip

from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.urls import reverse
from django.shortcuts import Http404, redirect
from django.utils.functional import cached_property
from django.utils import translation


def build_social_link(template, request, title):
    text_to_encode = 'Export Readiness - ' + title + ' '
    return template.format(
        url=request.build_absolute_uri(),
        text=urllib.parse.quote(text_to_encode)
    )


def cms_component_is_bidi(activated_language, languages):
    if any(code == activated_language for code, _ in languages):
        return translation.get_language_info(activated_language)['bidi']
    return False


def build_twitter_link(request, title):
    template = 'https://twitter.com/intent/tweet?text={text}{url}'
    return build_social_link(template, request, title)


def build_facebook_link(request, title):
    template = 'https://www.facebook.com/share.php?u={url}'
    return build_social_link(template, request, title)


def build_linkedin_link(request, title):
    template = (
        'https://www.linkedin.com/shareArticle'
        '?mini=true&url={url}&title={text}&source=LinkedIn'
    )
    return build_social_link(template, request, title)


def build_email_link(request, title):
    template = 'mailto:?body={url}&subject={text}'
    return build_social_link(template, request, title)


def build_social_links(request, title):
    kwargs = {'request': request, 'title': title}
    return {
        'facebook': build_facebook_link(**kwargs),
        'twitter': build_twitter_link(**kwargs),
        'linkedin': build_linkedin_link(**kwargs),
        'email': build_email_link(**kwargs),
    }


def handle_cms_response(response):
    if response.status_code == 404:
        raise Http404()
    response.raise_for_status()
    return response.json()


def handle_cms_response_allow_404(response):
    if response.status_code == 404:
        return {}
    response.raise_for_status()
    return response.json()


class GeoLocationRedirector:
    DOMESTIC_COUNTRY_CODES = ['GB', 'IE']
    COUNTRY_TO_LANGUAGE_MAP = {
        'CN': 'zh-hans',
        'DE': 'de',
        'ES': 'es',
        'JP': 'ja',
    }
    COOKIE_NAME = 'disable_geoloaction'
    LANGUAGE_PARAM = 'lang'

    def __init__(self, request):
        self.request = request

    @cached_property
    def country_code(self):
        client_ip, is_routable = get_client_ip(self.request)
        if client_ip and is_routable:
            response = GeoIP2().country(client_ip)
            return response['country_code']

    @property
    def country_language(self):
        return self.COUNTRY_TO_LANGUAGE_MAP.get(
            self.country_code, settings.LANGUAGE_CODE
        )

    @property
    def should_redirect(self):
        return (
            self.COOKIE_NAME not in self.request.COOKIES and
            self.LANGUAGE_PARAM not in self.request.GET and
            self.country_code is not None and
            self.country_code not in self.DOMESTIC_COUNTRY_CODES
        )

    def get_response(self):
        params = self.request.GET.dict()
        params[self.LANGUAGE_PARAM] = self.country_language
        url = '{url}?{querystring}'.format(
            url=reverse('landing-page-international'),
            querystring=urllib.parse.urlencode(params)
        )
        response = redirect(url)
        response.set_cookie(
            key=self.COOKIE_NAME,
            value='true',
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN
        )
        return response


def get_company_profile(request):
    if request.sso_user:
        response = api_client.company.retrieve_private_profile(
            sso_session_id=request.sso_user.session_id,
        )
        if response.status_code == 200:
            return response.json()
