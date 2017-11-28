from unittest.mock import call, patch, Mock

from bs4 import BeautifulSoup

import pytest
from directory_constants.constants import exred_articles

from django.template.loader import render_to_string
from django.urls import reverse

from article import articles, helpers, structure, views
import core.helpers


persona_lise_views_under_test = (
    (
        views.PersonaNewArticleListView,
        reverse('article-list-persona-new'),
    ),
    (
        views.PersonaOccasionalArticleListView,
        reverse('article-list-persona-occasional')
    ),
    (
        views.PersonaRegularArticleListView,
        reverse('article-list-persona-regular'),
    ),
)

guidance_views_under_test = (
    (
        views.MarketResearchArticleListView,
        reverse('article-list-market-research'),
    ),
    (
        views.CustomerInsightArticleListView,
        reverse('article-list-customer-insight'),
    ),
    (
        views.FinanceArticleListView,
        reverse('article-list-finance')
    ),
    (
        views.BusinessPlanningArticleListView,
        reverse('article-list-business-planning'),
    ),
    (
        views.GettingPaidArticleListView,
        reverse('article-list-getting-paid')
    ),
    (
        views.OperationsAndComplianceArticleListView,
        reverse('article-list-operations-and-compliance')
    )
)


article_views_under_test = (
    (
        views.DoResearchFirstView,
        reverse('article-research-market'),
    ),
    (
        views.DefineMarketPotentialView,
        reverse('define-market-potential'),
    ),
    (
        views.DoFieldResearchView,
        reverse('do-field-research'),
    ),
    (
        views.AnalyseTheCompetitionView,
        reverse('analyse-the-competition'),
    ),
    (
        views.VisitTradeShowView,
        reverse('visit-trade-show'),
    ),
    (
        views.KnowYourCustomerView,
        reverse('know-your-customer'),
    ),
    (
        views.MeetYourCustomerView,
        reverse('meet-your-customers'),
    ),
    (
        views.ManageLanguageDifferencesView,
        reverse('manage-language-differences'),
    ),
    (
        views.UnderstandYourCustomersCultureView,
        reverse('understand-your-customers-culture'),
    ),
    (
        views.GetMoneyToExportView,
        reverse('get-money-to-export'),
    ),
    (
        views.ChooseTheRightFinanceView,
        reverse('choose-right-finance'),
    ),
    (
        views.GetExportFinanceView,
        reverse('get-export-finance'),
    ),
    (
        views.RaiseMoneyByBorrowingView,
        reverse('raise-money-by-borrowing'),
    ),
    (
        views.BorrowAgainstAssetsView,
        reverse('borrow-against-assets'),
    ),
    (
        views.RaiseMoneyWithInvestmentView,
        reverse('raise-money-with-investment'),
    ),
    (
        views.GetGovernmentFinanceSupportView,
        reverse('get-finance-support-from-government'),
    ),
    (
        views.MakeExportingPlanView,
        reverse('make-an-export-plan'),
    ),
    (
        views.FindARouteToMarketView,
        reverse('find-a-route-to-market'),
    ),
    (
        views.SellOverseasDirectlyView,
        reverse('sell-overseas-directly'),
    ),
    (
        views.UseOverseasAgentView,
        reverse('use-an-overseas-agent'),
    ),
    (
        views.UseDistributorView,
        reverse('use-a-distributor'),
    ),
    (
        views.ChoosingAgentOrDistributorView,
        reverse('choosing-an-agent-or-distributor'),
    ),
    (
        views.LicenceAndFranchisingView,
        reverse('licensing-and-franchising'),
    ),
    (
        views.LicenceYourProductOrServiceView,
        reverse('license-your-product-or-service'),
    ),
    (
        views.FranchiseYourBusinessView,
        reverse('franchise-your-business'),
    ),
    (
        views.StartJointVentureView,
        reverse('start-a-joint-venture'),
    ),
    (
        views.SetupOverseasOperationView,
        reverse('set-up-an-overseas-operation'),
    ),
    (
        views.ConsiderHowPaidView,
        reverse('consider-how-youll-get-paid'),
    ),
    (
        views.InvoiceCurrencyAndContentsView,
        reverse('invoice-currency-and-contents'),
    ),
    (
        views.DecideWhenPaidView,
        reverse('decide-when-youll-get-paid'),
    ),
    (
        views.PaymentMethodsView,
        reverse('payment-methods'),
    ),
    (
        views.InsureAgainstNonPaymentView,
        reverse('insure-against-non-payment'),
    ),
    (
        views.PlanTheLogisticsView,
        reverse('plan-the-logistics'),
    ),
    (
        views.UseFreightForwarderView,
        reverse('use-a-freight-forwarder'),
    ),
    (
        views.UseIncotermsInContractsView,
        reverse('use-incoterms-in-contracts'),
    ),
    (
        views.GetYourExportDocumentsRightView,
        reverse('get-your-export-documents-right'),
    ),
    (
        views.InternationaliseWesbiteView,
        reverse('internationalise-your-website'),
    ),
    (
        views.MatchYourWebsiteToYourAudienceView,
        reverse('match-your-website-to-your-audience'),
    ),
    (
        views.WhatIntellectualPropertyIsView,
        reverse('what-intellectual-property-is'),
    ),
    (
        views.TypesOfIntellectualPropertyView,
        reverse('types-of-intellectual-property'),
    ),
    (
        views.KnowWhatIntellectualPropertyYouHaveView,
        reverse('know-what-IP-you-have'),
    ),
    (
        views.IntellectualPropertyProtectionView,
        reverse('ip-protection-in-multiple-countries'),
    ),
    (
        views.NextStepsNewExporterView,
        reverse('next-steps-new-exporter'),
    ),
    (
        views.NextStepsOccasionalExporterView,
        reverse('next-steps-occasional-exporter'),
    ),
    (
        views.NextStepsRegularExporterView,
        reverse('next-steps-regular-exporter'),
    )
)


@pytest.mark.parametrize('view_class,url', persona_lise_views_under_test)
def test_persona_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article_group'] == view_class.article_group


@pytest.mark.parametrize('view_class,url', guidance_views_under_test)
def test_guidance_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article_group'] == view_class.article_group


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article'] == view_class.article
    assert response.context_data['article_group'] == structure.ALL_ARTICLES

    html = helpers.markdown_to_html(
        markdown_file_path=view_class.article.markdown_file_path,
        context=response.context[-1].flatten(),
    )
    expected = str(BeautifulSoup(html, 'html.parser'))
    assert expected in str(BeautifulSoup(response.content, 'html.parser'))


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_title_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]

    html = '<h1>' + view_class.article.title + '</h1>'
    expected = str(BeautifulSoup(html, 'html.parser'))

    assert expected in str(BeautifulSoup(response.content, 'html.parser'))


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_share_links(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]

    expected_twitter = core.helpers.build_twitter_link(
        request=response._request,
        title=view_class.article.title,
    )
    expected_facebook = core.helpers.build_facebook_link(
        request=response._request,
        title=view_class.article.title,
    )
    expected_linkedin = core.helpers.build_linkedin_link(
        request=response._request,
        title=view_class.article.title,
    )
    expected_email = core.helpers.build_email_link(
        request=response._request,
        title=view_class.article.title,
    )
    soup = BeautifulSoup(response.content, 'html.parser')

    assert soup.find(id='share-twitter').attrs['href'] == expected_twitter
    assert soup.find(id='share-facebook').attrs['href'] == expected_facebook
    assert soup.find(id='share-linkedin').attrs['href'] == expected_linkedin
    assert soup.find(id='share-email').attrs['href'] == expected_email


# skip the last group - it does not have a page, it's a list of all articles.
# skip CUSTOM_PAGE_* groups - they're tested elsewhere as they need settting up
@pytest.mark.parametrize('group', structure.ALL_GROUPS[:-4])
def test_article_links_include_next_param(client, group):
    response = client.get(group.url)
    soup = BeautifulSoup(response.content, 'html.parser')

    article_links = soup.findAll('a', {'class': 'article'})

    assert len(article_links) == len(group.articles)

    for article, article_link_element in zip(group.articles, article_links):
        assert article_link_element.attrs['href'] == (
            str(article.url) + '?source=' + group.name
        )


@pytest.mark.parametrize('group', [
    structure.CUSTOM_PAGE_NEW_ARTICLES,
    structure.CUSTOM_PAGE_REGULAR_ARTICLES,
    structure.CUSTOM_PAGE_OCCASIONAL_ARTICLES,
])
def test_article_link_custom_page_exporter_articles(group):
    html = render_to_string('triage/custom-page.html', {
        'section_configuration': {
            'persona_article_group': group,
        },
        'article_group': group,
        'article_group_progress': {
            'time_left_to_read': 0,
        }
    })
    soup = BeautifulSoup(html, 'html.parser')

    article_links = soup.findAll('a', {'class': 'article'})

    assert len(article_links) == len(group.articles)

    for article, article_link_element in zip(group.articles, article_links):
        assert article_link_element.attrs['href'] == (
            str(article.url) + '?source=' + group.name
        )


@pytest.mark.parametrize('group', structure.ALL_GROUPS)
def test_inferred_next_articles(client, group):
    for article, next_article in zip(group.articles, group.articles[1:]):
        response = client.get(article.url + '?source=' + group.name)
        soup = BeautifulSoup(response.content, 'html.parser')
        next_article_element = soup.find(id='next-article-link')

        if next_article:
            assert response.context_data['next_article'] == next_article
            assert response.context_data['article_group'] == group
            assert response.context_data['next_article_group'] == group
            assert next_article_element.attrs['href'] == (
                str(next_article.url) + '?source=' + group.name
            )
            assert next_article_element.text == next_article.title
        else:
            next_group_top_article = group.next_guidance_group.articles[0]
            assert next_article_element == next_group_top_article
            assert response.context_data['next_article_group'] == \
                group.next_guidance_group


# skip the last group - it does not have a page, it's a list of all articles.
@pytest.mark.parametrize('group', structure.ALL_GROUPS[:-1])
def test_inferred_return_to_article(client, group):
    for article in group.articles:
        response = client.get(article.url + '?source=' + group.name)
        soup = BeautifulSoup(response.content, 'html.parser')
        category_element = soup.find(id='category-link')

        assert category_element.attrs['href'] == str(group.url)
        assert category_element.text == group.title


@patch('article.helpers.DatabaseArticlesReadManager.retrieve_article_uuids',
       Mock(return_value=set()))
@patch('article.helpers.DatabaseArticlesReadManager.persist_article')
def test_article_view_persist_article_logged_in_user(
    mocked_persist_articles, authed_client
):
    url = reverse('article-research-market')
    response = authed_client.get(url)

    assert response.status_code == 200
    assert mocked_persist_articles.call_count == 1
    assert mocked_persist_articles.call_args == call(
        exred_articles.DO_RESEARCH_FIRST
    )


@patch('article.helpers.SessionArticlesReadManager.persist_article')
def test_article_view_persist_article_anon_user(
        mocked_persist_articles,
        client
):
    url = reverse('article-research-market')
    response = client.get(url)

    assert response.status_code == 200
    assert mocked_persist_articles.call_count == 1
    assert mocked_persist_articles.call_args == call(
        exred_articles.DO_RESEARCH_FIRST
    )


@pytest.mark.parametrize('url,read_count,total_count,title,time,uuids', [
    (
        reverse('article-research-market'),
        3,
        len(structure.ALL_ARTICLES.articles),
        '',
        6147,
        frozenset([
           articles.USE_DISTRIBUTOR.uuid,
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
    (
        reverse('article-research-market') + '?source=finance',
        2,
        len(structure.GUIDANCE_FINANCE_ARTICLES.articles),
        structure.GUIDANCE_FINANCE_ARTICLES.title,
        852,
        frozenset([
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
    (
        reverse('get-export-finance'),
        3,
        len(structure.ALL_ARTICLES.articles),
        '',
        6147,
        frozenset([
           articles.USE_DISTRIBUTOR.uuid,
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
    (
        reverse('get-export-finance') + '?source=finance',
        2,
        len(structure.GUIDANCE_FINANCE_ARTICLES.articles),
        structure.GUIDANCE_FINANCE_ARTICLES.title,
        852,
        frozenset([
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
])
@patch('article.helpers.SessionArticlesReadManager.persist_article', Mock)
@patch('article.helpers.SessionArticlesReadManager.retrieve_article_uuids')
def test_article_group_read_counter_with_source(
    mock_retrieve, client, url, read_count, total_count, title, time, uuids
):
    mock_retrieve.return_value = {
       articles.USE_DISTRIBUTOR.uuid,
       articles.GET_EXPORT_FINANCE.uuid,
       articles.GET_MONEY_TO_EXPORT.uuid,
    }
    response = client.get(url)

    assert response.context_data['article_group_progress'] == {
        'read_count': read_count,
        'total_articles_count': total_count,
        'time_left_to_read': time,
        'read_article_uuids': uuids,
    }
    assert response.context_data.get('article_group_title') == title
