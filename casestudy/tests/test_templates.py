from django.template.loader import render_to_string
from casestudy import casestudies
from directory_header_footer.context_processors import urls_processor
from bs4 import BeautifulSoup


def test_case_study_soo_link(settings):
    settings.SERVICES_SOO = 'http://soo.com'
    context = urls_processor(None)
    context['casestudy'] = casestudies.HELLO_BABY
    html = render_to_string('casestudy/hello-baby.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    soo_link = soup.find(string='Selling online overseas service').parent
    assert soo_link.attrs['href'] == 'http://soo.com'
