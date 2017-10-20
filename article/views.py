from django.views.generic import TemplateView

from article import helpers, articles


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
            social_links=social_links,
        )


class BaseArticleListView(TemplateView):
    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs, articles=self.articles
        )


class PeronaNewArticleListView(BaseArticleListView):
    template_name = 'article/list-new-persona.html'
    articles = [
        articles.DO_RESEARCH_FIRST,
        articles.KNOW_YOUR_CUSTOMER,
        articles.MEET_YOUR_CUSTOMER,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.GET_MONEY_TO_EXPORT,
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CONSIDER_HOW_PAID,
        articles.PLAN_THE_LOGISTICS,
        articles.INTERNATIONALISE_WESBITE,
        articles.WHAT_INTERLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTERLECTUAL_PROPERTY,
    ]


class PeronaOccasionalArticleListView(BaseArticleListView):
    template_name = 'article/list-occasional-persona.html'
    articles = [
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.ANALYSE_THE_COMPETITION,
        articles.KNOW_YOUR_CUSTOMER,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
        articles.GET_MONEY_TO_EXPORT,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.START_JOINT_VENTURE,
        articles.CONSIDER_HOW_PAID,
        articles.INVOICE_CURRENCY_AND_CONTENTS,
        articles.DECIDE_WHEN_PAID,
        articles.PAYMENT_METHODS,
        articles.INSURE_AGAINST_NON_PAYMENT,
        articles.USE_FREIGHT_FORWARDER,
        articles.USE_INCOTERMS_IN_CONTRACTS,
        articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        articles.INTERNATIONALISE_WESBITE,
        articles.WHAT_INTERLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTERLECTUAL_PROPERTY,
        articles.KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTERLECTUAL_PROPERTY_PROTECTION,
    ]


class PeronaRegularArticleListView(BaseArticleListView):
    template_name = 'article/list-regular-persona.html'
    articles = [
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.ANALYSE_THE_COMPETITION,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.FRANCHISE_YOUR_BUSINESS,
        articles.START_JOINT_VENTURE,
        articles.SETUP_OVERSEAS_OPERATION,
        articles.INSURE_AGAINST_NON_PAYMENT,
        articles.KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTERLECTUAL_PROPERTY_PROTECTION
    ]


class MarketReasearchArticleListView(BaseArticleListView):
    template_name = 'article/list-market-research.html'
    articles = [
        articles.DO_RESEARCH_FIRST,
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.ANALYSE_THE_COMPETITION,
        articles.VISIT_TRADE_SHOW,
    ]


class CustomerInsightArticleListView(BaseArticleListView):
    template_name = 'article/list-customer-insight.html'
    articles = [
        articles.KNOW_YOUR_CUSTOMER,
        articles.MEET_YOUR_CUSTOMER,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    ]


class FinanceArticleListView(BaseArticleListView):
    template_name = 'article/list-finance.html'
    articles = [
        articles.GET_MONEY_TO_EXPORT,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
    ]


class BusinessPlanningArticleListView(BaseArticleListView):
    template_name = 'article/list-business-planning.html'
    articles = [
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        articles.LICENCE_AND_FRANCHISING,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.FRANCHISE_YOUR_BUSINESS,
        articles.START_JOINT_VENTURE,
        articles.SETUP_OVERSEAS_OPERATION,
    ]


class GettingPaidArticleListView(BaseArticleListView):
    template_name = 'article/list-getting-paid.html'
    articles = [
        articles.CONSIDER_HOW_PAID,
        articles.INVOICE_CURRENCY_AND_CONTENTS,
        articles.DECIDE_WHEN_PAID,
        articles.PAYMENT_METHODS,
        articles.INSURE_AGAINST_NON_PAYMENT,
    ]


class OperationsAndComplianceArticleListView(BaseArticleListView):
    template_name = 'article/list-operations-and-compliance.html'
    articles = [
        articles.PLAN_THE_LOGISTICS,
        articles.USE_FREIGHT_FORWARDER,
        articles.USE_INCOTERMS_IN_CONTRACTS,
        articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        articles.INTERNATIONALISE_WESBITE,
        articles.WHAT_INTERLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTERLECTUAL_PROPERTY,
        articles.KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTERLECTUAL_PROPERTY_PROTECTION,
    ]


class DoResearchFirstView(BaseArticleDetailView):
    article = articles.DO_RESEARCH_FIRST


class DefineMarketPotentialView(BaseArticleDetailView):
    article = articles.DEFINE_MARKET_POTENTIAL


class DoFieldResearchView(BaseArticleDetailView):
    article = articles.DO_FIELD_RESEARCH


class AnalyseTheCompetitionView(BaseArticleDetailView):
    article = articles.ANALYSE_THE_COMPETITION


class VisitTradeShowView(BaseArticleDetailView):
    article = articles.VISIT_TRADE_SHOW


class KnowYourCustomerView(BaseArticleDetailView):
    article = articles.KNOW_YOUR_CUSTOMER


class MakeExportingPlanView(BaseArticleDetailView):
    article = articles.MAKE_EXPORTING_PLAN


class FindARouteToMarketView(BaseArticleDetailView):
    article = articles.FIND_A_ROUTE_TO_MARKET


class UseOverseasAgentView(BaseArticleDetailView):
    article = articles.USE_OVERSEAS_AGENT


class UseDistributorView(BaseArticleDetailView):
    article = articles.USE_DISTRIBUTOR


class ChoosingAgentOrDistributorView(BaseArticleDetailView):
    article = articles.CHOOSING_AGENT_OR_DISTRIBUTOR


class LicenceAndFranchisingView(BaseArticleDetailView):
    article = articles.LICENCE_AND_FRANCHISING


class LicenceYourProductOrServiceView(BaseArticleDetailView):
    article = articles.LICENCE_YOUR_PRODUCT_OR_SERVICE


class FranchiseYourBusinessView(BaseArticleDetailView):
    article = articles.FRANCHISE_YOUR_BUSINESS


class StartJointVentureView(BaseArticleDetailView):
    article = articles.START_JOINT_VENTURE


class SetupOverseasOperationView(BaseArticleDetailView):
    article = articles.SETUP_OVERSEAS_OPERATION


class GetMoneyToExportView(BaseArticleDetailView):
    article = articles.GET_MONEY_TO_EXPORT


class ChooseTheRightFinanceView(BaseArticleDetailView):
    article = articles.CHOOSE_THE_RIGHT_FINANCE


class GetExportFinanceView(BaseArticleDetailView):
    article = articles.GET_EXPORT_FINANCE


class RaiseMoneyByBorrowingView(BaseArticleDetailView):
    article = articles.RAISE_MONEY_BY_BORROWING


class BorrowAgainstAssetsView(BaseArticleDetailView):
    article = articles.BORROW_AGAINST_ASSETS


class RaiseMoneyWithInvestmentView(BaseArticleDetailView):
    article = articles.RAISE_MONEY_WITH_INVESTMENT


class GetGovernmentFinanceSupportView(BaseArticleDetailView):
    article = articles.GET_GOVERNMENT_FINANCE_SUPPORT


class ConsiderHowPaidView(BaseArticleDetailView):
    article = articles.CONSIDER_HOW_PAID


class InvoiceCurrencyAndContentsView(BaseArticleDetailView):
    article = articles.INVOICE_CURRENCY_AND_CONTENTS


class DecideWhenPaidView(BaseArticleDetailView):
    article = articles.DECIDE_WHEN_PAID


class PaymentMethodsView(BaseArticleDetailView):
    article = articles.PAYMENT_METHODS


class InsureAgainstNonPaymentView(BaseArticleDetailView):
    article = articles.INSURE_AGAINST_NON_PAYMENT


class PlanTheLogisticsView(BaseArticleDetailView):
    article = articles.PLAN_THE_LOGISTICS


class UseFreightForwarderView(BaseArticleDetailView):
    article = articles.USE_FREIGHT_FORWARDER


class UseIncotermsInContractsView(BaseArticleDetailView):
    article = articles.USE_INCOTERMS_IN_CONTRACTS


class GetYourExportDocumentsRightView(BaseArticleDetailView):
    article = articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT


class SetupWesbiteView(BaseArticleDetailView):
    article = articles.INTERNATIONALISE_WESBITE


class MatchYourWebsiteToYourAudienceView(BaseArticleDetailView):
    article = articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE


class WhatInterlectualPropertyIsView(BaseArticleDetailView):
    article = articles.WHAT_INTERLECTUAL_PROPERTY_IS


class TypesOfInterlectualPropertyView(BaseArticleDetailView):
    article = articles.TYPES_OF_INTERLECTUAL_PROPERTY


class KnowWhatInterlectualPropertyYouHaveView(BaseArticleDetailView):
    article = articles.KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE


class InterlectualPropertyProtectionView(BaseArticleDetailView):
    article = articles.INTERLECTUAL_PROPERTY_PROTECTION


class MeetYourCustomerView(BaseArticleDetailView):
    article = articles.MEET_YOUR_CUSTOMER


class ManageLanguageDifferencesView(BaseArticleDetailView):
    article = articles.MANAGE_LANGUAGE_DIFFERENCES


class UnderstandYourCustomersCultureView(BaseArticleDetailView):
    article = articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE
