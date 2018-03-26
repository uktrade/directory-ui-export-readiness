from django.template.loader import render_to_string
from directory_components.context_processors import urls_processor
from bs4 import BeautifulSoup

import pytest


@pytest.mark.parametrize('used_online_marketplace,expected', (
    (True, 'Yes'),
    (False, 'No'),
    (None, None),
))
def test_triage_summary_online_marketplace_question(
    used_online_marketplace, expected, rf,
):
    context = {
        'all_cleaned_data': {
            'used_online_marketplace': used_online_marketplace,
        },
        'request': rf.get('/')
    }
    html = render_to_string('triage/wizard-step-summary.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find(id='triage-do-you-use-online-marketplaces-answer')

    if expected:
        assert element.text == expected
    else:
        assert element is None


@pytest.mark.parametrize('regular_exporter,expected', (
    (True, 'Yes'),
    (False, 'No'),
    (None, None),
))
def test_triage_summary_regular_exporter_question(
    regular_exporter, expected, rf
):
    context = {
        'all_cleaned_data': {
            'regular_exporter': regular_exporter,
        },
        'request': rf.get('.')
    }
    html = render_to_string('triage/wizard-step-summary.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find(id='triage-are-you-exporting-regularly-answer')

    if expected:
        assert element.text == expected
    else:
        assert element is None


@pytest.mark.parametrize('goods,services,expected', (
    (True, False, 'Goods'),
    (True, True, 'Goods and services'),
    (False, True, 'Services'),
    (False, False, None),
))
def test_triage_summary_goods_services(
    goods, services, expected, rf
):
    context = {
        'all_cleaned_data': {
            'is_exporting_goods': goods,
            'is_exporting_services': services,
        },
        'request': rf.get('.')
    }
    html = render_to_string('triage/wizard-step-summary.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find(id='triage-what-are-you-exporting-answer')

    if expected:
        assert element.text.strip() == expected
    else:
        assert element is None


@pytest.mark.parametrize('sso_is_logged_in,expected', (
    (True, False),
    (False, True),
))
def test_triage_start_user_state(sso_is_logged_in, expected, rf):
    context = {
        'sso_is_logged_in': sso_is_logged_in,
        'request': rf.get('/'),
    }
    html = render_to_string('triage/start-now.html', context)

    assert ('save your progress' in html) is expected


def test_custom_page_services_links(settings):
    settings.HEADER_FOOTER_URLS_SOO = 'http://soo.com'
    settings.HEADER_FOOTER_URLS_FAB = 'http://fab.com'
    context = {
        'section_configuration': {
            'selling_online_overseas': True,
            'trade_profile': True,
            'selling_online_overseas_and_export_opportunities': True
        },
        **urls_processor(None)
    }
    html = render_to_string('triage/custom-page.html', context)
    assert 'http://soo.com' in html
    assert 'http://fab.com' in html
