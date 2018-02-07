from django.template.loader import render_to_string

import pytest


@pytest.mark.parametrize('template_name', (
    '400.html',
    '403.html',
    '404.html',
))
def test_error_templates(template_name, rf):
    assert render_to_string(template_name, {'request': rf.get('/')})


def test_about_page_services_links():
    context = {
        'header_footer_urls': {
            'services_soo': 'http://soo.com',
            'services_fab': 'http://fab.com',
            'services_exopps': 'http://exopps.com',
        }
    }
    html = render_to_string('core/about.html', context)
    assert 'http://soo.com' in html
    assert 'http://fab.com' in html
    assert 'http://exopps.com' in html
