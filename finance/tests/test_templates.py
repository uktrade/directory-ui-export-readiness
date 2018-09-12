from django.template.loader import render_to_string
from django.urls import reverse


def test_deprecated_get_finance_template(settings):
    context = {
        'page': {'call_to_action_url': 'cta.com'},
    }
    html = render_to_string('finance/get_finance_deprecated.html', context)

    assert 'cta.com' in html


def test_get_finance_template():
    context = {}
    html = render_to_string('finance/get_finance.html', context)

    expected = reverse(
        'uk-export-finance-lead-generation-form', kwargs={'step': 'contact'}
    )

    assert expected in html
