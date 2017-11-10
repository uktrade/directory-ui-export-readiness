from django.conf import settings
from directory_constants.constants import urls as default_urls


def feature_flags(request):
    return {
        'features': {
        }
    }


def analytics(request):
    return {
        'analytics': {
            'GOOGLE_TAG_MANAGER_ID': settings.GOOGLE_TAG_MANAGER_ID,
            'GOOGLE_TAG_MANAGER_ENV': settings.GOOGLE_TAG_MANAGER_ENV,
            'UTM_COOKIE_DOMAIN': settings.UTM_COOKIE_DOMAIN,
        }
    }


def external_service_urls(request):
    return {
        'external_services': {
            'FEEDBACK_URL': settings.EXTERNAL_SERVICE_FEEDBACK_URL
        }
    }
