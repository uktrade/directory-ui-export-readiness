from bs4 import BeautifulSoup

import pytest
from article import views

from django.core.urlresolvers import reverse

from article import helpers


persona_lise_views_under_test = (
    (
        views.PeronaNewArticleListView,
        reverse('article-list-persona-new'),
    ),
    (
        views.PeronaOccasionalArticleListView,
        reverse('article-list-persona-occasional')
    ),
    (
        views.PeronaRegularArticleListView,
        reverse('article-list-persona-regular'),
    ),
)

guidance_views_under_test = (
    (
        views.MarketReasearchArticleListView,
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
        reverse('meet-your-customer'),
    ),
    (
        views.ManageLanguageDifferencesView,
        reverse('manage-language-differences'),
    ),
    (
        views.UnderstandYourCustomersCultureView,
        reverse('understand-your-cutomers-culture'),
    ),
    (
        views.GetMoneyToExportView,
        reverse('get-money'),
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
        views.SetupWesbiteView,
        reverse('set-up-a-website'),
    ),
    (
        views.MatchYourWebsiteToYourAudienceView,
        reverse('match-your-website-to-your-audience'),
    ),
    (
        views.WhatInterlectualPropertyIsView,
        reverse('what-intellectual-property-is'),
    ),
    (
        views.TypesOfInterlectualPropertyView,
        reverse('types-of-intellectual-property'),
    ),
    (
        views.KnowWhatInterlectualPropertyYouHaveView,
        reverse('know-what-IP-you-have'),
    ),
    (
        views.InterlectualPropertyProtectionView,
        reverse('ip-protection-in-multiple-countries'),
    ),
)


@pytest.mark.parametrize('view_class,url', persona_lise_views_under_test)
def test_persona_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['articles'] == view_class.articles


@pytest.mark.parametrize('view_class,url', guidance_views_under_test)
def test_guidance_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['articles'] == view_class.articles


@pytest.mark.parametrize('view_class,url', article_views_under_test)
def test_articles_views(view_class, url, client):
    response = client.get(url)

    assert response.status_code == 200
    assert response.template_name == [view_class.template_name]
    assert response.context_data['article'] == view_class.article

    html = helpers.markdown_to_html(view_class.article.markdown_file_path)
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

    expected_twitter = helpers.build_twitter_link(
        request=response._request,
        title=view_class.article.title,
    )
    expected_facebook = helpers.build_facebook_link(
        request=response._request,
        title=view_class.article.title,
    )
    expected_linkedin = helpers.build_linkedin_link(
        request=response._request,
        title=view_class.article.title,
    )
    expected_email = helpers.build_email_link(
        request=response._request,
        title=view_class.article.title,
    )

    expected_twitter in str(response.content)
    expected_facebook in str(response.content)
    expected_linkedin in str(response.content)
    expected_email in str(response.content)
