from directory_components.context_processors import urls_processor
import pytest

from django.template.loader import render_to_string
from django.urls import reverse


def test_error_templates(rf):
    template_name = '404.html'
    assert render_to_string(template_name, {'request': rf.get('/')})


def test_404_custom_template(settings, client):
    settings.DEBUG = False
    response = client.get('/this-is-not-a-valid-url/')
    assert response.status_code == 404
    expected_text = bytes(
        'If you entered a web address please check'
        ' it’s correct.', 'utf8')
    assert expected_text in response.content


def test_about_page_services_links(settings):
    settings.HEADER_FOOTER_URLS_SOO = 'http://soo.com'
    settings.HEADER_FOOTER_URLS_FAB = 'http://fab.com'
    context = urls_processor(None)
    html = render_to_string('core/about.html', context)
    assert 'http://fab.com' in html
    assert 'http://soo.com' in html


def test_international_beta_banner():
    html = render_to_string('core/landing_page_international.html')
    assert 'beta' in html
    assert 'This is a new service' in html


@pytest.mark.parametrize('is_enabled', (True, False))
def test_international_footer_feature_flaged_link(is_enabled, settings):
    template_name = 'core/includes/international_footer.html'
    context = {
        'features': {'EU_EXIT_FORMS_ON': is_enabled}
    }

    html = render_to_string(template_name, context)

    assert (reverse('contact-page-international') in html) is is_enabled
