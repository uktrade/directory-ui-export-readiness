from django.views.generic import TemplateView

from article import helpers, structure


class BaseArticleDetailView(TemplateView):
    template_name = 'article/detail-base.html'

    def get_context_data(self, *args, **kwargs):
        social_link_kwargs = {
            'request': self.request, 'title': self.article.title,
        }
        social_links = {
            'facebook': helpers.build_facebook_link(**social_link_kwargs),
            'twitter': helpers.build_twitter_link(**social_link_kwargs),
            'linkedin': helpers.build_linkedin_link(**social_link_kwargs),
            'email': helpers.build_email_link(**social_link_kwargs),
        }
        return super().get_context_data(
            *args, **kwargs,
            article=self.article,
            article_list=self.article_list,
            social_links=social_links,
        )


class BaseArticleListView(TemplateView):

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs, article_list=self.article_list
        )


class MarketReasearchArticleListView(BaseArticleListView):
    article_list = structure.ARTICLE_LIST_MARKET_RESEARCH
    template_name = 'article/list-market-reasearch.html'


class CustomerInsightArticleListView(BaseArticleListView):
    article_list = structure.ARTICLE_LIST_CUSTOMER_INSIGHT
    template_name = 'article/list-customer-insight.html'


class FinanceArticleListView(BaseArticleListView):
    article_list = structure.ARTICLE_LIST_FINANCE
    template_name = 'article/list-finance.html'


class BusinessPlanningArticleListView(BaseArticleListView):
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING
    template_name = 'article/list-business-planning.html'


class GettingPaidArticleListView(BaseArticleListView):
    article_list = structure.ARTICLE_LIST_GETTING_PAID
    template_name = 'article/list-getting-paid.html'


class OperationsAndComplianceArticleListView(BaseArticleListView):
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE
    template_name = 'article/list-operations-and-compliance.html'


class DoResearchFirstView(BaseArticleDetailView):
    article = structure.DO_RESEARCH_FIRST
    article_list = structure.ARTICLE_LIST_MARKET_RESEARCH


class DefineMarketPotentialView(BaseArticleDetailView):
    article = structure.DEFINE_MARKET_POTENTIAL
    article_list = structure.ARTICLE_LIST_MARKET_RESEARCH


class DoFieldResearchView(BaseArticleDetailView):
    article = structure.DO_FIELD_RESEARCH
    article_list = structure.ARTICLE_LIST_MARKET_RESEARCH


class AnalyseTheCompetitionView(BaseArticleDetailView):
    article = structure.ANALYSE_THE_COMPETITION
    article_list = structure.ARTICLE_LIST_MARKET_RESEARCH


class VisitTradeShowView(BaseArticleDetailView):
    article = structure.VISIT_TRADE_SHOW
    article_list = structure.ARTICLE_LIST_MARKET_RESEARCH


class KnowYourCustomerView(BaseArticleDetailView):
    article = structure.KNOW_YOUR_CUSTOMER
    article_list = structure.ARTICLE_LIST_CUSTOMER_INSIGHT


class MakeExportingPlanView(BaseArticleDetailView):
    article = structure.MAKE_EXPORTING_PLAN
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class FindARouteToMarketView(BaseArticleDetailView):
    article = structure.FIND_A_ROUTE_TO_MARKET
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class UseOverseasAgentView(BaseArticleDetailView):
    article = structure.USE_OVERSEAS_AGENT
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class UseDistributorView(BaseArticleDetailView):
    article = structure.USE_DISTRIBUTOR
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class ChoosingAgentOrDistributorView(BaseArticleDetailView):
    article = structure.CHOOSING_AGENT_OR_DISTRIBUTOR
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class LicenceAndFranchisingView(BaseArticleDetailView):
    article = structure.LICENCE_AND_FRANCHISING
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class LicenceYourProductOrServiceView(BaseArticleDetailView):
    article = structure.LICENCE_YOUR_PRODUCT_OR_SERVICE
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class FranchiseYourBusinessView(BaseArticleDetailView):
    article = structure.FRANCHISE_YOUR_BUSINESS
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class StartJointVentureView(BaseArticleDetailView):
    article = structure.START_JOINT_VENTURE
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class SetupOverseasOperationView(BaseArticleDetailView):
    article = structure.SETUP_OVERSEAS_OPERATION
    article_list = structure.ARTICLE_LIST_BUSINESS_PLANNING


class GetMoneyToExportView(BaseArticleDetailView):
    article = structure.GET_MONEY_TO_EXPORT
    article_list = structure.ARTICLE_LIST_FINANCE


class ChooseTheRightFinanceView(BaseArticleDetailView):
    article = structure.CHOOSE_THE_RIGHT_FINANCE
    article_list = structure.ARTICLE_LIST_FINANCE


class GetExportFinanceView(BaseArticleDetailView):
    article = structure.GET_EXPORT_FINANCE
    article_list = structure.ARTICLE_LIST_FINANCE


class RaiseMoneyByBorrowingView(BaseArticleDetailView):
    article = structure.RAISE_MONEY_BY_BORROWING
    article_list = structure.ARTICLE_LIST_FINANCE


class BorrowAgainstAssetsView(BaseArticleDetailView):
    article = structure.BORROW_AGAINST_ASSETS
    article_list = structure.ARTICLE_LIST_FINANCE


class RaiseMoneyWithInvestmentView(BaseArticleDetailView):
    article = structure.RAISE_MONEY_WITH_INVESTMENT
    article_list = structure.ARTICLE_LIST_FINANCE


class GetGovernmentFinanceSupportView(BaseArticleDetailView):
    article = structure.GET_GOVERNMENT_FINANCE_SUPPORT
    article_list = structure.ARTICLE_LIST_FINANCE


class ConsiderHowPaidView(BaseArticleDetailView):
    article = structure.CONSIDER_HOW_PAID
    article_list = structure.ARTICLE_LIST_GETTING_PAID


class InvoiceCurrencyAndContentsView(BaseArticleDetailView):
    article = structure.INVOICE_CURRENCY_AND_CONTENTS
    article_list = structure.ARTICLE_LIST_GETTING_PAID


class DecideWhenPaidView(BaseArticleDetailView):
    article = structure.DECIDE_WHEN_PAID
    article_list = structure.ARTICLE_LIST_GETTING_PAID


class PaymentMethodsView(BaseArticleDetailView):
    article = structure.PAYMENT_METHODS
    article_list = structure.ARTICLE_LIST_GETTING_PAID


class InsureAgainstNonPaymentView(BaseArticleDetailView):
    article = structure.INSURE_AGAINST_NON_PAYMENT
    article_list = structure.ARTICLE_LIST_GETTING_PAID


class PlanTheLogisticsView(BaseArticleDetailView):
    article = structure.PLAN_THE_LOGISTICS
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class UseFreightForwarderView(BaseArticleDetailView):
    article = structure.USE_FREIGHT_FORWARDER
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class UseIncotermsInContractsView(BaseArticleDetailView):
    article = structure.USE_INCOTERMS_IN_CONTRACTS
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class GetYourExportDocumentsRightView(BaseArticleDetailView):
    article = structure.GET_YOUR_EXPORT_DOCUMENTS_RIGHT
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class SetupWesbiteView(BaseArticleDetailView):
    article = structure.INTERNATIONALISE_WESBITE
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class MatchYourWebsiteToYourAudienceView(BaseArticleDetailView):
    article = structure.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class WhatInterlectualPropertyIsView(BaseArticleDetailView):
    article = structure.WHAT_INTERLECTUAL_PROPERTY_IS
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class TypesOfInterlectualPropertyView(BaseArticleDetailView):
    article = structure.TYPES_OF_INTERLECTUAL_PROPERTY
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class KnowWhatInterlectualPropertyYouHaveView(BaseArticleDetailView):
    article = structure.KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class InterlectualPropertyProtectionView(BaseArticleDetailView):
    article = structure.INTERLECTUAL_PROPERTY_PROTECTION
    article_list = structure.ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE


class MeetYourCustomerView(BaseArticleDetailView):
    article = structure.MEET_YOUR_CUSTOMER
    article_list = structure.ARTICLE_LIST_CUSTOMER_INSIGHT


class ManageLanguageDifferencesView(BaseArticleDetailView):
    article = structure.MANAGE_LANGUAGE_DIFFERENCES
    article_list = structure.ARTICLE_LIST_CUSTOMER_INSIGHT


class UnderstandYourCustomersCultureView(BaseArticleDetailView):
    article = structure.UNDERSTAND_YOUR_CUSTOMERS_CULTURE
    article_list = structure.ARTICLE_LIST_CUSTOMER_INSIGHT
