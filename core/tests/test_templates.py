from django.template.loader import render_to_string
from directory_header_footer.context_processors import urls_processor

import pytest


@pytest.mark.parametrize('template_name', (
    '400.html',
    '403.html',
    '404.html',
))
def test_error_templates(template_name, rf):
    assert render_to_string(template_name, {'request': rf.get('/')})


def test_about_page_services_links(settings):
    settings.SERVICES_SOO = 'http://soo.com'
    settings.SERVICES_FAB = 'http://fab.com'
    settings.SERVICES_EXOPPS = 'http://exopps.com'
    context = urls_processor(None)
    html = render_to_string('core/about.html', context)
    assert 'http://fab.com' in html
    assert 'http://soo.com' in html
    assert 'http://exopps.com' in html
