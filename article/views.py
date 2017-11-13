from django.views.generic import TemplateView
from django.utils.functional import cached_property

from article import articles, structure
from core.helpers import build_social_links
from core.views import ArticleReadMixin


class BaseArticleDetailView(ArticleReadMixin, TemplateView):
    template_name = 'article/detail-base.html'

    def get(self, request, *args, **kwargs):
        self.record_article_visit()
        return super().get(request, *args, **kwargs)

    def record_article_visit(self):
        self.request.article_read_manager.persist_article(self.article.uuid)

    def get_context_data(self, *args, **kwargs):
        social_links = build_social_links(
            request=self.request, title=self.article.title
        )
        return super().get_context_data(
            *args, **kwargs,
            article=self.article,
            next_article=self.next_article,
            next_group=self.next_group,
            article_group=self.article_group,
            social_links=social_links,
            article_group_title=self.article_group.title,
        )

    @property
    def next_article(self):
        return structure.get_next_article(
            article_group=self.article_group,
            current_article=self.article,
        )

    @property
    def next_group(self):
        return structure.get_next_group(
            article_group=self.article_group,
            current_article=self.article,
        )

    @cached_property
    def article_group(self):
        return structure.get_article_group(
            group_name=self.request.GET.get('source', 'all'),
        )


class BaseArticleListView(ArticleReadMixin, TemplateView):

    def get_context_data(self, *args, **kwargs):
        return super().get_context_data(
            *args, **kwargs, article_group=self.article_group,
        )


class PeronaNewArticleListView(BaseArticleListView):
    template_name = 'article/list-new-persona.html'
    article_group = structure.PERSONA_NEW_ARTICLES


class PeronaOccasionalArticleListView(BaseArticleListView):
    template_name = 'article/list-occasional-persona.html'
    article_group = structure.PERSONA_OCCASIONAL_ARTICLES


class PeronaRegularArticleListView(BaseArticleListView):
    template_name = 'article/list-regular-persona.html'
    article_group = structure.PERSONA_REGULAR_ARTICLES


class MarketReasearchArticleListView(BaseArticleListView):
    template_name = 'article/list-market-research.html'
    article_group = structure.GUIDANCE_MARKET_RESEARCH_ARTICLES


class CustomerInsightArticleListView(BaseArticleListView):
    template_name = 'article/list-customer-insight.html'
    article_group = structure.GUIDANCE_CUSTOMER_INSIGHT_ARTICLES


class FinanceArticleListView(BaseArticleListView):
    template_name = 'article/list-finance.html'
    article_group = structure.GUIDANCE_FINANCE_ARTICLES


class BusinessPlanningArticleListView(BaseArticleListView):
    template_name = 'article/list-business-planning.html'
    article_group = structure.GUIDANCE_BUSINESS_PLANNING_ARTICLES


class GettingPaidArticleListView(BaseArticleListView):
    template_name = 'article/list-getting-paid.html'
    article_group = structure.GUIDANCE_GETTING_PAID_ARTICLES


class OperationsAndComplianceArticleListView(BaseArticleListView):
    template_name = 'article/list-operations-and-compliance.html'
    article_group = structure.GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES


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


class SellOverseasDirectlyView(BaseArticleDetailView):
    article = articles.SELL_OVERSEAS_DIRECTLY


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


class InternationaliseWesbiteView(BaseArticleDetailView):
    article = articles.INTERNATIONALISE_WESBITE


class MatchYourWebsiteToYourAudienceView(BaseArticleDetailView):
    article = articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE


class WhatInterlectualPropertyIsView(BaseArticleDetailView):
    article = articles.WHAT_INTELLECTUAL_PROPERTY_IS


class TypesOfInterlectualPropertyView(BaseArticleDetailView):
    article = articles.TYPES_OF_INTELLECTUAL_PROPERTY


class KnowWhatInterlectualPropertyYouHaveView(BaseArticleDetailView):
    article = articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE


class InterlectualPropertyProtectionView(BaseArticleDetailView):
    article = articles.INTELLECTUAL_PROPERTY_PROTECTION


class MeetYourCustomerView(BaseArticleDetailView):
    article = articles.MEET_YOUR_CUSTOMER


class ManageLanguageDifferencesView(BaseArticleDetailView):
    article = articles.MANAGE_LANGUAGE_DIFFERENCES


class UnderstandYourCustomersCultureView(BaseArticleDetailView):
    article = articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE


class NextStepsNewExporterView(BaseArticleDetailView):
    article = articles.NEXT_STEPS_NEW_EXPORTER


class NextStepsOccasionalExporterView(BaseArticleDetailView):
    article = articles.NEXT_STEPS_OCCASIONAL_EXPORTER


class NextStepsRegularExporterView(BaseArticleDetailView):
    article = articles.NEXT_STEPS_REGULAR_EXPORTER
