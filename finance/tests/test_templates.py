import pytest

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

    assert reverse('uk-export-finance-pardot-funnel-start') in html


@pytest.mark.parametrize('template_name', (
    'finance/get_finance.html',
    'finance/lead_generation_form.html',
))
def test_tracking_code(template_name):
    context = {
        'pi_tracker_account_id': '123',
        'pi_tracker_campaign_id': '456',
        'pi_tracker_javascript_url': 'url.com',
    }
    tracking_code = render_to_string(
        'finance/lead-generation-campaign-tracking.html',
        context
    )

    assert tracking_code in render_to_string(template_name, context)
