from unittest.mock import call, patch, Mock

from bs4 import BeautifulSoup

import pytest
from directory_constants.constants import exred_articles
from directory_components.templatetags import directory_components_tags

from django.template.loader import render_to_string
from django.urls import reverse_lazy

from article import articles, helpers, structure, views
import core.helpers
from core.mixins import EXPORT_JOURNEY_REDIRECTS

persona_lise_views_under_test = (
    (
        views.PersonaNewArticleListView,
        reverse_lazy('article-list-persona-new'),
    ),
    (
        views.PersonaOccasionalArticleListView,
        reverse_lazy('article-list-persona-occasional')
    ),
    (
        views.PersonaRegularArticleListView,
        reverse_lazy('article-list-persona-regular'),
    ),
)

guidance_views_under_test = (
    (
        views.MarketResearchArticleListView,
        reverse_lazy('article-list-market-research'),
    ),
    (
        views.CustomerInsightArticleListView,
        reverse_lazy('article-list-customer-insight'),
    ),
    (
        views.FinanceArticleListView,
        reverse_lazy('article-list-finance')
    ),
    (
        views.BusinessPlanningArticleListView,
        reverse_lazy('article-list-business-planning'),
    ),
    (
        views.GettingPaidArticleListView,
        reverse_lazy('article-list-getting-paid')
    ),
    (
        views.OperationsAndComplianceArticleListView,
        reverse_lazy('article-list-operations-and-compliance')
    )
)


article_views_under_test = (
    (
        views.DoResearchFirstView,
        reverse_lazy('article-research-market'),
    ),
    (
        views.DefineMarketPotentialView,
        reverse_lazy('define-market-potential'),
    ),
    (
        views.DoFieldResearchView,
        reverse_lazy('do-field-research'),
    ),
    (
        views.AnalyseTheCompetitionView,
        reverse_lazy('analyse-the-competition'),
    ),
    (
        views.VisitTradeShowView,
        reverse_lazy('visit-trade-show'),
    ),
    (
        views.KnowYourCustomerView,
        reverse_lazy('know-your-customer'),
    ),
    (
        views.MeetYourCustomerView,
        reverse_lazy('meet-your-customers'),
    ),
    (
        views.ManageLanguageDifferencesView,
        reverse_lazy('manage-language-differences'),
    ),
    (
        views.UnderstandYourCustomersCultureView,
        reverse_lazy('understand-your-customers-culture'),
    ),
    (
        views.GetMoneyToExportView,
        reverse_lazy('get-money-to-export'),
    ),
    (
        views.ChooseTheRightFinanceView,
        reverse_lazy('choose-right-finance'),
    ),
    (
        views.GetExportFinanceView,
        reverse_lazy('get-export-finance'),
    ),
    (
        views.RaiseMoneyByBorrowingView,
        reverse_lazy('raise-money-by-borrowing'),
    ),
    (
        views.BorrowAgainstAssetsView,
        reverse_lazy('borrow-against-assets'),
    ),
    (
        views.RaiseMoneyWithInvestmentView,
        reverse_lazy('raise-money-with-investment'),
    ),
    (
        views.GetGovernmentFinanceSupportView,
        reverse_lazy('get-finance-support-from-government'),
    ),
    (
        views.MakeExportingPlanView,
        reverse_lazy('make-an-export-plan'),
    ),
    (
        views.FindARouteToMarketView,
        reverse_lazy('find-a-route-to-market'),
    ),
    (
        views.SellOverseasDirectlyView,
        reverse_lazy('sell-overseas-directly'),
    ),
    (
        views.UseOverseasAgentView,
        reverse_lazy('use-an-overseas-agent'),
    ),
    (
        views.UseDistributorView,
        reverse_lazy('use-a-distributor'),
    ),
    (
        views.ChoosingAgentOrDistributorView,
        reverse_lazy('choosing-an-agent-or-distributor'),
    ),
    (
        views.LicenceAndFranchisingView,
        reverse_lazy('licensing-and-franchising'),
    ),
    (
        views.LicenceYourProductOrServiceView,
        reverse_lazy('license-your-product-or-service'),
    ),
    (
        views.FranchiseYourBusinessView,
        reverse_lazy('franchise-your-business'),
    ),
    (
        views.StartJointVentureView,
        reverse_lazy('start-a-joint-venture'),
    ),
    (
        views.SetupOverseasOperationView,
        reverse_lazy('set-up-an-overseas-operation'),
    ),
    (
        views.ConsiderHowPaidView,
        reverse_lazy('consider-how-youll-get-paid'),
    ),
    (
        views.InvoiceCurrencyAndContentsView,
        reverse_lazy('invoice-currency-and-contents'),
    ),
    (
        views.DecideWhenPaidView,
        reverse_lazy('decide-when-youll-get-paid'),
    ),
    (
        views.PaymentMethodsView,
        reverse_lazy('payment-methods'),
    ),
    (
        views.InsureAgainstNonPaymentView,
        reverse_lazy('insure-against-non-payment'),
    ),
    (
        views.PlanTheLogisticsView,
        reverse_lazy('plan-the-logistics'),
    ),
    (
        views.UseFreightForwarderView,
        reverse_lazy('use-a-freight-forwarder'),
    ),
    (
        views.UseIncotermsInContractsView,
        reverse_lazy('use-incoterms-in-contracts'),
    ),
    (
        views.GetYourExportDocumentsRightView,
        reverse_lazy('get-your-export-documents-right'),
    ),
    (
        views.InternationaliseWesbiteView,
        reverse_lazy('internationalise-your-website'),
    ),
    (
        views.MatchYourWebsiteToYourAudienceView,
        reverse_lazy('match-your-website-to-your-audience'),
    ),
    (
        views.WhatIntellectualPropertyIsView,
        reverse_lazy('what-intellectual-property-is'),
    ),
    (
        views.TypesOfIntellectualPropertyView,
        reverse_lazy('types-of-intellectual-property'),
    ),
    (
        views.KnowWhatIntellectualPropertyYouHaveView,
        reverse_lazy('know-what-IP-you-have'),
    ),
    (
        views.IntellectualPropertyProtectionView,
        reverse_lazy('ip-protection-in-multiple-countries'),
    ),
    (
        views.NextStepsNewExporterView,
        reverse_lazy('next-steps-new-exporter'),
    ),
    (
        views.NextStepsOccasionalExporterView,
        reverse_lazy('next-steps-occasional-exporter'),
    ),
    (
        views.NextStepsRegularExporterView,
        reverse_lazy('next-steps-regular-exporter'),
    ),
    (
        views.DoBusinessWithIntegrityView,
        reverse_lazy('business-with-integrity'),
    ),
    (
        views.AntiBriberyAndCorruptionTrainingView,
        reverse_lazy('anti-bribery-and-corruption-training'),
    ),
    (
        views.ReportCorruptionView,
        reverse_lazy('report-corruption'),
    ),
    (
        views.KnowTheRelevantLegislationView,
        reverse_lazy('know-the-relevant-legislation'),
    ),
)


@pytest.mark.parametrize('view_class,url', persona_lise_views_under_test)
def test_persona_views(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article_group'] == view_class.article_group
    assert response.context_data['paginate_articles'] is True


@pytest.mark.parametrize('view_class,url', persona_lise_views_under_test)
def test_persona_views_feature_flag_off(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.parametrize('view_class,url', guidance_views_under_test)
def test_guidance_views(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article_group'] == view_class.article_group
    assert response.context_data['paginate_articles'] is False


@pytest.mark.parametrize('view_class,url', guidance_views_under_test)
def test_guidance_views_feature_flag_off(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_views(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article'] == view_class.article
    assert response.context_data['article_group'] == structure.ALL_ARTICLES

    html = helpers.markdown_to_html(
        markdown_file_path=view_class.article.markdown_file_path,
        context=response.context[-1].flatten(),
    )
    html = directory_components_tags.add_export_elements_classes(html)
    expected = str(BeautifulSoup(html, 'html.parser'))
    assert expected in str(BeautifulSoup(response.content, 'html.parser'))


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_views_feature_flag_off(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    response = client.get(url)

    assert response.status_code == 302
    assert response.url == EXPORT_JOURNEY_REDIRECTS[url]


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_title_views(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]

    html = '<h1 class="heading-xlarge">' + view_class.article.title + '</h1>'
    expected = str(BeautifulSoup(html, 'html.parser'))

    assert expected in str(BeautifulSoup(response.content, 'html.parser'))


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_title_views_feature_flag_off(
    view_class, url, client, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = False
    response = client.get(url)

    assert response.status_code == 302


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_share_links(view_class, url, client, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
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
def test_article_links_include_next_param(client, group, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
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
def test_article_link_custom_page_exporter_articles(
    group, anon_request, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    html = render_to_string('triage/custom-page.html', {
        'section_configuration': {
            'persona_article_group': group,
        },
        'article_group': group,
        'article_group_progress': {
            'time_left_to_read': 0,
        },
        'request': anon_request,
    })
    soup = BeautifulSoup(html, 'html.parser')

    article_links = soup.findAll('a', {'class': 'article'})

    assert len(article_links) == len(group.articles)

    for article, article_link_element in zip(group.articles, article_links):
        assert article_link_element.attrs['href'] == (
            str(article.url) + '?source=' + group.name
        )


@pytest.mark.parametrize('group', structure.ALL_GROUPS)
def test_inferred_next_articles(client, group, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
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
def test_inferred_return_to_article(client, group, settings):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    for article in group.articles:
        response = client.get(article.url + '?source=' + group.name)
        soup = BeautifulSoup(response.content, 'html.parser')
        category_element = soup.find(id='category-link')

        assert category_element.attrs['href'] == str(group.url)
        assert category_element.text == group.title


@patch('article.helpers.DatabaseArticlesViewedManager.'
       'retrieve_viewed_article_uuids', Mock(return_value=set()))
@patch('article.helpers.DatabaseArticlesViewedManager.persist_articles')
def test_article_view_persist_article_logged_in_user(
    mock_persist_articles, authed_client, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    url = reverse_lazy('article-research-market')
    response = authed_client.get(url)

    assert response.status_code == 200
    assert mock_persist_articles.call_count == 1
    assert mock_persist_articles.call_args == call(
        set([exred_articles.DO_RESEARCH_FIRST]),
    )


@patch('article.helpers.SessionArticlesViewedManager.persist_article')
def test_article_view_persist_article_anon_user(
    mock_persist_articles, client, settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
    url = reverse_lazy('article-research-market')
    response = client.get(url)

    assert response.status_code == 200
    assert mock_persist_articles.call_count == 1
    assert mock_persist_articles.call_args == call(
        exred_articles.DO_RESEARCH_FIRST
    )


@pytest.mark.parametrize('url,read_count,total_count,title,time,uuids', [
    (
        reverse_lazy('article-research-market'),
        3,
        len(structure.ALL_ARTICLES.articles),
        '',
        5769,
        frozenset([
           articles.USE_DISTRIBUTOR.uuid,
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
    (
        reverse_lazy('article-research-market') + '?source=finance',
        2,
        len(structure.GUIDANCE_FINANCE_ARTICLES.articles),
        structure.GUIDANCE_FINANCE_ARTICLES.title,
        751,
        frozenset([
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
    (
        reverse_lazy('get-export-finance'),
        3,
        len(structure.ALL_ARTICLES.articles),
        '',
        5769,
        frozenset([
           articles.USE_DISTRIBUTOR.uuid,
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
    (
        reverse_lazy('get-export-finance') + '?source=finance',
        2,
        len(structure.GUIDANCE_FINANCE_ARTICLES.articles),
        structure.GUIDANCE_FINANCE_ARTICLES.title,
        751,
        frozenset([
           articles.GET_EXPORT_FINANCE.uuid,
           articles.GET_MONEY_TO_EXPORT.uuid,
        ]),
    ),
])
@patch('article.helpers.SessionArticlesViewedManager.persist_article', Mock)
@patch(
    'article.helpers.SessionArticlesViewedManager.'
    'retrieve_viewed_article_uuids'
)
def test_article_group_read_counter_with_source(
    mock_retrieve, client, url, read_count, total_count, title, time, uuids,
    settings
):
    settings.FEATURE_FLAGS['EXPORT_JOURNEY_ON'] = True
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
        'viewed_article_uuids': uuids,
    }
    assert response.context_data.get('article_group_title') == title
