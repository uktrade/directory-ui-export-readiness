from unittest.mock import call, patch

from django.core.urlresolvers import reverse

from triage import views


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_regular_exporter(mock_persist_answers, client):
    url = reverse('triage-wizard')
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'CHOICE_1',
    })
    client.post(url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })
    client.post(url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'True',
    })
    # skips the "do you use the marketplace" step
    summary_response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-sole_trader': True,
    })
    done_response = client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    expected_data = {
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'regular_exporter': True,
        'sector': 'CHOICE_1',
    }

    assert done_response.status_code == 200
    assert done_response.content == b'success\n'
    assert summary_response.context_data['persona'] == 'Regular Exporter'
    assert summary_response.context_data['sector_label'] == 'Choice 1'
    assert summary_response.context_data['all_cleaned_data'] == expected_data
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call(expected_data)


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_occasional_exporter(mock_persist_answers, client):
    url = reverse('triage-wizard')
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'CHOICE_2',
    })
    client.post(url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })
    client.post(url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'False',
    })
    client.post(url, {
        view_name + '-current_step': view_class.ONLINE_MARKETPLACE,
        view_class.ONLINE_MARKETPLACE + '-used_online_marketplace': 'True',
    })
    summary_response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-sole_trader': True,
    })
    done_response = client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    expected_data = {
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'used_online_marketplace': True,
        'regular_exporter': False,
        'sector': 'CHOICE_2',
    }

    assert done_response.status_code == 200
    assert done_response.content == b'success\n'
    assert summary_response.context_data['persona'] == 'Occasional Exporter'
    assert summary_response.context_data['sector_label'] == 'Choice 2'
    assert summary_response.context_data['all_cleaned_data'] == expected_data
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call(expected_data)


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_new_exporter(mock_persist_answers, client):
    url = reverse('triage-wizard')
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'CHOICE_2',
    })
    client.post(url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'False',
    })
    summary_response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-sole_trader': True,
    })
    done_response = client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    expected_data = {
        'sole_trader': True,
        'company_name': 'Example corp',
        'exported_before': False,
        'sector': 'CHOICE_2',
    }

    assert done_response.status_code == 200
    assert done_response.content == b'success\n'
    assert summary_response.context_data['persona'] == 'New Exporter'
    assert summary_response.context_data['sector_label'] == 'Choice 2'
    assert summary_response.context_data['all_cleaned_data'] == expected_data
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call(expected_data)
