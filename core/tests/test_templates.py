from django.template.loader import render_to_string
from directory_header_footer.context_processors import urls_processor


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
    settings.SERVICES_SOO = 'http://soo.com'
    settings.SERVICES_FAB = 'http://fab.com'
    settings.SERVICES_EXOPPS = 'http://exopps.com'
    context = urls_processor(None)
    html = render_to_string('core/about.html', context)
    assert 'http://fab.com' in html
    assert 'http://soo.com' in html
    assert 'http://exopps.com' in html
