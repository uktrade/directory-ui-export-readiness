from unittest.mock import call, patch, Mock

from bs4 import BeautifulSoup
import pytest
import requests

from django.core.urlresolvers import reverse
from directory_constants.constants import exred_sector_names

from core.tests.helpers import create_response
from casestudy import casestudies
from triage import forms, views
from article import structure


@pytest.fixture(autouse=True)
def mock_retrive_articles_read():
    mock = patch('api_client.api_client.exportreadiness.retrieve_article_read')
    mock.return_value = create_response(200, json_body=[])
    yield mock.start()
    mock.stop()


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_regular_exporter(mock_persist_answers, client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'
    response = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'True',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANIES_HOUSE,
        view_class.COMPANIES_HOUSE + '-is_in_companies_house': True,
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
    })
    assert response.status_code == 302
    # skips the "do you use the marketplace" step
    summary_get_response = client.get(response.url)
    summary_post_response = client.post(response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert b'Create my export journey' in summary_get_response.content
    assert summary_get_response.context_data['persona'] == (
        forms.REGULAR_EXPORTER
    )
    assert summary_get_response.context_data['sector_label'] == 'Animals; live'
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'is_in_companies_house': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'regular_exporter': True,
        'sector': 'HS01',
        'company_number': None,
    }
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call({
        'company_name': 'Example corp',
        'used_online_marketplace': None,
        'exported_before': True,
        'regular_exporter': True,
        'sector': 'HS01',
        'company_number': None,
        'is_in_companies_house': True,
    })
    assert finished_response.status_code == 302
    assert finished_response.get('Location') == str(view_class.success_url)


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_occasional_exporter(mock_persist_answers, client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'
    response = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'False',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.ONLINE_MARKETPLACE,
        view_class.ONLINE_MARKETPLACE + '-used_online_marketplace': 'True',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANIES_HOUSE,
        view_class.COMPANIES_HOUSE + '-is_in_companies_house': True,
    })
    assert response.status_code == 302
    response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
        view_class.COMPANY + '-company_number': '41231231',
    })
    assert response.status_code == 302
    summary_get_response = client.get(response.url)
    summary_post_response = client.post(response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert finished_response.status_code == 302
    assert finished_response.url == str(view_class.success_url)
    assert b'Create my export journey' in summary_get_response.content
    assert summary_get_response.context_data['persona'] == (
        forms.OCCASIONAL_EXPORTER
    )
    assert summary_get_response.context_data['sector_label'] == 'Animals; live'
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'is_in_companies_house': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'used_online_marketplace': True,
        'regular_exporter': False,
        'sector': 'HS01',
        'company_number': '41231231',
    }
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call({
        'company_name': 'Example corp',
        'exported_before': True,
        'used_online_marketplace': True,
        'regular_exporter': False,
        'sector': 'HS01',
        'company_number': '41231231',
        'is_in_companies_house': True,
    })


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_submit_triage_new_exporter(mock_persist_answers, client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'
    response = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'False',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANIES_HOUSE,
        view_class.COMPANIES_HOUSE + '-is_in_companies_house': True,
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
    })
    assert response.status_code == 302
    summary_get_response = client.get(response.url)
    summary_post_response = client.post(response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert finished_response.status_code == 302
    assert finished_response.url == str(view_class.success_url)
    assert b'Create my export journey' in summary_get_response.content
    assert summary_get_response.context_data['persona'] == forms.NEW_EXPORTER
    assert summary_get_response.context_data['sector_label'] == 'Animals; live'
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'company_number': None,
        'is_in_companies_house': True,
        'company_name': 'Example corp',
        'exported_before': False,
        'sector': 'HS01',
    }
    assert mock_persist_answers.call_count == 1
    assert mock_persist_answers.call_args == call({
        'company_number': None,
        'is_in_companies_house': True,
        'company_name': 'Example corp',
        'exported_before': False,
        'sector': 'HS01',
        'used_online_marketplace': None,
        'regular_exporter': False,
    })


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_triage_manually_skip_company(mock_persist_answers, client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'
    response = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'False',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANY,
        'wizard_skip_step': True,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'triage-wizard',
        kwargs={'step': view_class.SUMMARY}
    )


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_triage_sole_trader_skip_company(mock_persist_answers, client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'
    response = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'False',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANIES_HOUSE,
        view_class.COMPANIES_HOUSE + '-is_in_companies_house': False,
    })

    assert response.status_code == 302
    assert response.url == reverse(
        'triage-wizard',
        kwargs={'step': view_class.SUMMARY}
    )


def test_triage_skip_company_clears_previous_answers(client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'
    response = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'False',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANIES_HOUSE,
        view_class.COMPANIES_HOUSE + '-is_in_companies_house': True,
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
    })
    assert response.status_code == 302
    response = client.post(response.url, {
        view_name + '-current_step': view_class.COMPANY,
        'wizard_skip_step': True,
    })
    summary_get_response = client.get(response.url)
    summary_post_response = client.post(response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert finished_response.status_code == 302
    assert finished_response.url == str(view_class.success_url)
    assert b'Create my export journey' in summary_get_response.content
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'company_number': None,
        'is_in_companies_house': True,
        'company_name': '',
        'sector': 'HS01',
        'exported_before': False
    }


@patch('triage.helpers.SessionTriageAnswersManager.retrieve_answers')
def test_triage_skip_company_clears_previous_answers_summary(
    mocked_retrieve_answers, client
):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SUMMARY})
    view_name = 'triage_wizard_form_view'

    mocked_retrieve_answers.return_value = {
        'company_name': 'Example corp',
        'company_number': '123445',
        'exported_before': True,
        'is_in_companies_house': True,
        'regular_exporter': True,
        'sector': 'HS01',
        'used_online_marketplace': False,
    }
    client.get(url + '?result')
    url = reverse('triage-wizard', kwargs={'step': view_class.COMPANY})
    response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        'wizard_skip_step': True,
    })
    summary_get_response = client.get(response.url)
    summary_post_response = client.post(response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    assert finished_response.status_code == 302
    assert finished_response.url == str(view_class.success_url)
    assert b'Continue my export journey' in summary_get_response.content
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'company_number': None,
        'regular_exporter': True,
        'company_name': '',
        'sector': 'HS01',
        'exported_before': True,
        'is_in_companies_house': True,
    }


@patch('triage.helpers.DatabaseTriageAnswersManager.persist_answers', Mock)
@patch('triage.helpers.SessionTriageAnswersManager.retrieve_answers')
def test_triage_summary_change_answers(
    mocked_retrieve_answers, client
):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SUMMARY})
    view_name = 'triage_wizard_form_view'
    mocked_retrieve_answers.return_value = {
        'company_name': 'Acme ltd',
        'exported_before': True,
        'regular_exporter': True,
        'used_online_marketplace': False,
        'sector': 'HS01',
        'is_in_companies_house': True,
        'company_number': '123445',
        'company_name': 'Example corp',
    }
    client.get(url + '?result')
    url = reverse('triage-wizard', kwargs={'step': view_class.COMPANY})
    response = client.post(url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Other Example limited',
    })
    summary_get_response = client.get(response.url)
    summary_post_response = client.post(response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })

    assert b'Continue my export journey' in summary_get_response.content
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'company_number': None,
        'is_in_companies_house': True,
        'company_name': 'Other Example limited',
        'sector': 'HS01',
        'exported_before': True,
        'regular_exporter': True,
    }
    assert finished_response.status_code == 302
    assert finished_response.get('Location') == str(view_class.success_url)


def test_companies_house_search_validation_error(client):
    url = reverse('api-internal-companies-house-search')
    response = client.get(url)  # notice absense of `term`

    assert response.status_code == 400


@patch('triage.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_error(
    mock_search, client
):
    mock_search.return_value = create_response(400)
    url = reverse('api-internal-companies-house-search')

    with pytest.raises(requests.HTTPError):
        client.get(url, data={'term': 'thing'})


@patch('triage.helpers.CompaniesHouseClient.search')
def test_companies_house_search_api_success(
    mock_search, client
):
    mock_search.return_value = create_response(
        200, {'items': [{'name': 'Smashing corp'}]}
    )
    url = reverse('api-internal-companies-house-search')

    response = client.get(url, data={'term': 'thing'})

    assert response.status_code == 200
    assert response.content == b'[{"name": "Smashing corp"}]'


@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers')
def test_custom_view(mocked_retrieve_answers, authed_client, sso_user):
    triage_result = {
        'company_name': 'Acme ltd',
        'created': '2016-11-23T11:21:10.977518Z',
        'exported_before': True,
        'regular_exporter': True,
        'used_online_marketplace': False,
        'id': '1',
        'modified': '2016-11-23T11:21:10.977518Z',
        'sector': exred_sector_names.SECTORS_CHOICES[0][0],
        'sector_name': exred_sector_names.SECTORS_CHOICES[0][1],
        'sso_id': sso_user.id,
        'company_number': None,
    }
    mocked_retrieve_answers.return_value = triage_result
    url = reverse('custom-page')
    response = authed_client.get(url)
    assert response.status_code == 200
    assert response.template_name == ['triage/custom-page.html']
    assert response.context_data['triage_result'] == triage_result
    assert response.context_data['article_group_read_progress'] == {
        'all': {'read': 0, 'total': 45},
        'business_planning': {'read': 0, 'total': 11},
        'customer_insights': {'read': 0, 'total': 4},
        'finance': {'read': 0, 'total': 7},
        'getting_paid': {'read': 0, 'total': 5},
        'market_research': {'read': 0, 'total': 5},
        'operations_and_compliance': {'read': 0, 'total': 10},
        'persona_new': {'read': 0, 'total': 18},
        'persona_occasional': {'read': 0, 'total': 38},
        'persona_regular': {'read': 0, 'total': 18},
        'custom_persona_new': {'read': 0, 'total': 18},
        'custom_persona_occasional': {'read': 0, 'total': 38},
        'custom_persona_regular': {'read': 0, 'total': 18},
    }


def test_triage_wizard(client):
    view_class = views.TriageWizardFormView
    response = client.get(
        reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    )

    assert response.status_code == 200
    assert response.template_name == [
        views.TriageWizardFormView.templates[views.TriageWizardFormView.SECTOR]
    ]


@patch('triage.helpers.DatabaseTriageAnswersManager.persist_answers', Mock)
@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers')
def test_triage_wizard_summary_view(
    mocked_retrieve_answers, authed_client
):
    view_class = views.TriageWizardFormView
    view_name = 'triage_wizard_form_view'
    mocked_retrieve_answers.return_value = {
        'company_name': 'Acme ltd',
        'exported_before': True,
        'regular_exporter': True,
        'used_online_marketplace': False,
        'sector': 'HS01',
        'company_number': '33123445',
        'company_name': 'Example corp',
        'is_in_companies_house': True,
    }
    url = reverse('triage-wizard', kwargs={'step': view_class.SUMMARY})
    authed_client.get(url + '?result')
    summary_get_response = authed_client.get(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    summary_post_response = authed_client.post(url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    finished_response = authed_client.post(summary_post_response.url, {
        view_name + '-current_step': view_class.SUMMARY,
    })
    assert b'Continue my export journey' in summary_get_response.content
    assert summary_get_response.status_code == 200
    assert summary_get_response.template_name == [
        views.TriageWizardFormView.templates[view_class.SUMMARY]
    ]
    assert summary_get_response.context_data['persona'] == (
        forms.REGULAR_EXPORTER
    )
    assert summary_get_response.context_data['sector_label'] == 'Animals; live'
    assert summary_get_response.context_data['all_cleaned_data'] == {
        'is_in_companies_house': True,
        'company_name': 'Example corp',
        'exported_before': True,
        'regular_exporter': True,
        'sector': 'HS01',
        'company_number': '33123445',
        'company_name': 'Example corp',
    }
    assert finished_response.status_code == 302
    assert finished_response.url == str(view_class.success_url)


@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers')
def test_custom_view_no_triage_result_found(
    mocked_retrieve_answers, authed_client
):
    view_class = views.TriageWizardFormView
    mocked_retrieve_answers.return_value = {}
    url = reverse('custom-page')
    response = authed_client.get(url)
    assert response.status_code == 302
    assert response.url == reverse(
        'triage-wizard',
        kwargs={'step': view_class.SECTOR}
    )


@pytest.mark.parametrize('is_in_companies_house,expected', (
    (
        True,
        {
            'persona_article_group': structure.CUSTOM_PAGE_NEW_ARTICLES,
            'trade_profile': True,
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        },
    ),
    (
        False,
        {
            'persona_article_group': structure.CUSTOM_PAGE_NEW_ARTICLES,
            'trade_profile': False,
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        },
    ),
))
@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers',
       Mock(return_value={'sector': 'HS01'}))
@patch('triage.forms.get_persona', Mock(return_value=forms.NEW_EXPORTER))
def test_custom_view_new_exporter(
    is_in_companies_house, expected, authed_client
):
    with patch(
        'triage.forms.get_is_in_companies_house',
        return_value=is_in_companies_house
    ):
        url = reverse('custom-page')
        response = authed_client.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        assert response.status_code == 200
        assert response.context_data['section_configuration'] == expected
        assert response.context_data['casestudies'] == [
            casestudies.MARKETPLACE,
            casestudies.HELLO_BABY,
            casestudies.YORK,
        ]
        assert soup.find('h1').text.replace('\n', '') == (
            'Use your'
            'potential -'
            'start'
            'exporting'
        )


@pytest.mark.parametrize('in_companies_house,is_marketplace_user,expected', (
    (
        True,
        False,
        {
            'persona_article_group': structure.CUSTOM_PAGE_OCCASIONAL_ARTICLES,
            'trade_profile': True,
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        },
    ),
    (
        False,
        False,
        {
            'persona_article_group': structure.CUSTOM_PAGE_OCCASIONAL_ARTICLES,
            'trade_profile': False,
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        },
    ),
    (
        True,
        True,
        {
            'persona_article_group': structure.CUSTOM_PAGE_OCCASIONAL_ARTICLES,
            'trade_profile': True,
            'selling_online_overseas': True,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        },
    ),
    (
        False,
        True,
        {
            'persona_article_group': structure.CUSTOM_PAGE_OCCASIONAL_ARTICLES,
            'trade_profile': False,
            'selling_online_overseas': True,
            'selling_online_overseas_and_export_opportunities': False,
            'articles_resources': False,
            'case_studies': True,
        },
    ),
))
@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers',
       Mock(return_value={'sector': 'HS01'}))
@patch('triage.forms.get_persona',
       Mock(return_value=forms.OCCASIONAL_EXPORTER))
def test_custom_view_occasional_exporter(
    in_companies_house, is_marketplace_user, expected, authed_client
):
    with patch(
        'triage.forms.get_is_in_companies_house',
        return_value=in_companies_house
    ):
        with patch(
            'triage.forms.get_used_marketplace',
            return_value=is_marketplace_user
        ):
            url = reverse('custom-page')
            response = authed_client.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            assert response.status_code == 200
            assert response.context_data['section_configuration'] == expected
            assert response.context_data['casestudies'] == [
                casestudies.MARKETPLACE,
                casestudies.HELLO_BABY,
                casestudies.YORK,
            ]
            assert soup.find('h1').text.replace('\n', '') == (
                'New customers'
                'are waiting -'
                'promote your'
                'business'
            )


@pytest.mark.parametrize('is_in_companies_house,expected', (
    (
        True,
        {
            'persona_article_group': [],
            'trade_profile': True,
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': True,
            'articles_resources': True,
            'case_studies': False,
        },
    ),
    (
        False,
        {
            'persona_article_group': [],
            'trade_profile': False,
            'selling_online_overseas': False,
            'selling_online_overseas_and_export_opportunities': True,
            'articles_resources': True,
            'case_studies': False,
        },
    ),
))
@patch('triage.helpers.DatabaseTriageAnswersManager.retrieve_answers',
       Mock(return_value={'sector': 'HS01'}))
@patch('triage.forms.get_persona', Mock(return_value=forms.REGULAR_EXPORTER))
def test_custom_view_regular_exporter(
    is_in_companies_house, expected, authed_client
):
    with patch(
        'triage.forms.get_is_in_companies_house',
        return_value=is_in_companies_house
    ):
        url = reverse('custom-page')
        response = authed_client.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        assert response.status_code == 200
        assert response.context_data['section_configuration'] == expected
        assert response.context_data['casestudies'] == [
            casestudies.MARKETPLACE,
            casestudies.HELLO_BABY,
            casestudies.YORK,
        ]
        assert soup.find('h1').text.replace('\n', '') == (
            'Choose your'
            'next market -'
            'Find new'
            'customers'
        )


@pytest.mark.parametrize('sector_code', exred_sector_names.CODES_SECTORS_DICT)
def test_custom_page_top_markets(sector_code, client):
    mock_path = 'triage.helpers.SessionTriageAnswersManager.retrieve_answers'
    with patch(mock_path) as mock:
        mock.return_value = {
            'company_name': 'Acme ltd',
            'exported_before': True,
            'regular_exporter': True,
            'used_online_marketplace': False,
            'sector': sector_code,
            'company_number': '123445',
            'company_name': 'Example corp',
        }
        url = reverse('custom-page')
        response = client.get(url)
        assert response.status_code == 200

        soup = BeautifulSoup(response.content, 'html.parser')
        top_import_name = soup.find(id='top_importer_name')

        # data is not available for service codes, only for Harmonised
        # System codes.
        if not sector_code.startswith('HS'):
            assert top_import_name is None
        else:
            top_import_value = soup.find(id='top_importer_global_trade_value')
            top_country_row = soup.find(id='row-' + top_import_name.text)
            # there is no guarantee that the "country that imports the most" is
            # in the "top 10 countries for buying British goods"
            if top_country_row:
                top_country_row_import_value = top_country_row.find(
                    class_='cell-global_trade_value'
                )
                assert (
                    top_country_row_import_value.text == top_import_value.text
                )


@patch('triage.helpers.SessionTriageAnswersManager.persist_answers')
def test_triage_step_labels(mock_persist_answers, client):
    view_class = views.TriageWizardFormView
    url = reverse('triage-wizard', kwargs={'step': view_class.SECTOR})
    view_name = 'triage_wizard_form_view'

    response_one_get = client.get(url)
    response_one = client.post(url, {
        view_name + '-current_step': view_class.SECTOR,
        view_class.SECTOR + '-sector': 'HS01',
    })

    response_two_get = client.get(response_one.url)
    response_two = client.post(response_one.url, {
        view_name + '-current_step': view_class.EXPORTED_BEFORE,
        view_class.EXPORTED_BEFORE + '-exported_before': 'True',
    })

    response_three_get = client.get(response_two.url)
    response_three = client.post(response_two.url, {
        view_name + '-current_step': view_class.REGULAR_EXPORTER,
        view_class.REGULAR_EXPORTER + '-regular_exporter': 'True',
    })

    response_four_get = client.get(response_three.url)
    response_four = client.post(response_three.url, {
        view_name + '-current_step': view_class.COMPANIES_HOUSE,
        view_class.COMPANIES_HOUSE + '-is_in_companies_house': True,
    })

    response_five_get = client.get(response_four.url)
    client.post(response_four.url, {
        view_name + '-current_step': view_class.COMPANY,
        view_class.COMPANY + '-company_name': 'Example corp',
    })

    assert b'Question 1' in response_one_get.content
    assert b'Question 2' in response_two_get.content
    assert b'Question 3' in response_three_get.content
    assert b'Question 4' in response_four_get.content
    assert b'Question 5' in response_five_get.content
