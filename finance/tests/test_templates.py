import pytest

from django.template.loader import render_to_string
from django.urls import reverse

from directory_components.context_processors import feature_flags


def test_get_finance_template_feature_flag_off(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENEATION_ON': False
    }
    context = {
        'page': {'call_to_action_url': 'cta.com'},
        **feature_flags(None),
    }
    html = render_to_string('finance/get_finance.html', context)

    assert 'cta.com' in html


def test_get_finance_template_feature_flag_on(settings):
    settings.FEATURE_FLAGS = {
        **settings.FEATURE_FLAGS,
        'UKEF_LEAD_GENEATION_ON': True
    }
    context = {
        'call_to_action_url': 'cta.com',
        **feature_flags(None),
    }
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
