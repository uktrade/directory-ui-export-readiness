from django.template.loader import render_to_string
from bs4 import BeautifulSoup

import pytest


@pytest.mark.parametrize('used_online_marketplace,expected', (
    (True, 'Yes'),
    (False, 'No'),
    (None, None),
))
def test_triage_summary_online_marketplace_question(
    used_online_marketplace, expected
):
    context = {
        'all_cleaned_data': {
            'used_online_marketplace': used_online_marketplace,
        },
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
def test_triage_summary_regular_exporer_question(regular_exporter, expected):
    context = {
        'all_cleaned_data': {
            'regular_exporter': regular_exporter,
        },
    }
    html = render_to_string('triage/wizard-step-summary.html', context)
    soup = BeautifulSoup(html, 'html.parser')
    element = soup.find(id='regular_exporter')

    if expected:
        assert element.text == expected
    else:
        assert element is None
