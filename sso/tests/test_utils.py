from django.views import View
from django.http.response import HttpResponse

from sso import utils


def test_sso_login_required_mixin_redirect_to_sso(settings, rf):
    class TestView(utils.SSOLoginRequiredMixin, View):
        def get(self, request):
            return HttpResponse()

    request = rf.get('/')
    request.sso_user = None

    response = TestView.as_view()(request)

    assert response.url == (
        f'{settings.SSO_PROXY_LOGIN_URL}?next=http%3A//testserver/'
    )


def test_sso_signup_required_mixin_redirect_to_sso(settings, rf):
    class TestView(utils.SSOSignUpRequiredMixin, View):
        def get(self, request):
            return HttpResponse()

    request = rf.get('/')
    request.sso_user = None

    response = TestView.as_view()(request)

    assert response.url == (
        f'{settings.SSO_PROXY_SIGNUP_URL}?next=http%3A//testserver/'
    )
