from django.template.loader import render_to_string
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
    element = soup.find(id='used_online_marketplace')

    if expected:
        assert element.text == expected
    else:
        assert element is None


@pytest.mark.parametrize('regular_exporter,expected', (
    (True, 'Yes'),
    (False, 'No'),
    (None, None),
))
def test_triage_summary_regular_exporer_question(
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
    element = soup.find(id='regular_exporter')

    if expected:
        assert element.text == expected
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


def test_custom_page_services_links():
    context = {
        'header_footer_urls': {
            'services_soo': 'http://soo.com',
            'services_fab': 'http://fab.com',
            'services_exopps': 'http://exopps.com',
        }
    }
    html = render_to_string('triage/custom-page.html', context)
    assert 'http://soo.com' in html
    assert 'http://fab.com' in html
    assert 'http://exopps.com' in html
