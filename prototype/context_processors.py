from django.conf import settings


def get_url(url_name):
    return getattr(settings, url_name, None) or '#'


def prototype_home_link(request):
    return {
        'prototype_home_link': get_url('PROTOTYPE_HOME_LINK'),
    }
