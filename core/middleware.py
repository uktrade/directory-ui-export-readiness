from django.conf import settings
from django.middleware.locale import LocaleMiddleware
from django.utils import translation


class NoCacheMiddlware:
    """Tell the browser to not cache the pages.

    Information that should be kept private can be viewed by anyone
    with access to the files in the browser's cache directory.

    """

    def __init__(self, *args, **kwargs):
        # `NoCacheMiddleware` depends on `request.sso_user`, which comes from
        # `SSOUserMiddleware
        assert (
            'sso.middleware.SSOUserMiddleware' in settings.MIDDLEWARE_CLASSES
        )
        super().__init__(*args, **kwargs)

    def process_response(self, request, response):
        if getattr(request, 'sso_user', None):
            response['Cache-Control'] = 'no-store, no-cache'
        return response


class LocaleQuerystringMiddleware(LocaleMiddleware):

    @staticmethod
    def get_language_from_querystring(request):
        language_code = request.GET.get('lang')
        language_codes = translation.trans_real.get_languages()
        if language_code and language_code in language_codes:
            return language_code

    def process_request(self, request):
        super().process_request(request)
        language_code = self.get_language_from_querystring(request)
        if language_code:
            translation.activate(language_code)
            request.LANGUAGE_CODE = translation.get_language()


class PersistLocaleMiddleware:
    def process_response(self, request, response):
        response.set_cookie(
            key=settings.LANGUAGE_COOKIE_NAME,
            value=translation.get_language(),
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN
        )
        return response


class ForceDefaultLocale:
    """
    Force translation to English before view is called, then putting the user's
    original language back after the view has been called, laying the ground
    work for`TranslationsMixin` to turn on the desired locale. This
    provides per-view translations.

    """

    def process_request(self, request):
        translation.activate(settings.LANGUAGE_CODE)

    def process_response(self, request, response):
        if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            translation.activate(request.LANGUAGE_CODE)
        return response

    def process_exception(self, request, exception):
        if hasattr(request, 'LANGUAGE_CODE') and request.LANGUAGE_CODE:
            translation.activate(request.LANGUAGE_CODE)
