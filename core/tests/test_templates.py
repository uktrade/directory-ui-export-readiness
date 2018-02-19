from django.template.loader import render_to_string
from directory_header_footer.context_processors import urls_processor


def test_error_templates(rf):
    template_name = 'core/404.html'
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
