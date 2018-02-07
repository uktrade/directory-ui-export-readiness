from django.template.loader import render_to_string
from django.conf import settings
from casestudy import casestudies


def test_case_study_soo_link():
    settings.STATICFILES_STORAGE = (
        'django.contrib.staticfiles.storage.StaticFilesStorage')
    context = {
        'header_footer_urls': {
            'services_soo': 'http://soo.com',
        },
        'casestudy': casestudies.HELLO_BABY
    }
    html = render_to_string('casestudy/hello-baby.html', context)
    assert 'http://soo.com' in html
