from django.views.generic import TemplateView

from article import helpers, structure


class BaseArticleView(TemplateView):
    template_name = 'article/base.html'

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
            *args, **kwargs, article=self.article, social_links=social_links
        )


class DoResearchFirstView(BaseArticleView):
    article = structure.DO_RESEARCH_FIRST


class DefineMarketPotentialView(BaseArticleView):
    article = structure.DEFINE_MARKET_POTENTIAL


class DoFieldResearchView(BaseArticleView):
    article = structure.DO_FIELD_RESEARCH


class AnalyseTheCompetitionView(BaseArticleView):
    article = structure.ANALYSE_THE_COMPETITION


class VisitTradeShowView(BaseArticleView):
    article = structure.VISIT_TRADE_SHOW


class KnowYourCustomerView(BaseArticleView):
    article = structure.KNOW_YOUR_CUSTOMER


class MakeExportingPlanView(BaseArticleView):
    article = structure.MAKE_EXPORTING_PLAN


class FindARouteToMarketView(BaseArticleView):
    article = structure.FIND_A_ROUTE_TO_MARKET


class UseOverseasAgentView(BaseArticleView):
    article = structure.USE_OVERSEAS_AGENT


class UseDistributorView(BaseArticleView):
    article = structure.USE_DISTRIBUTOR


class ChoosingAgentOrDistributorView(BaseArticleView):
    article = structure.CHOOSING_AGENT_OR_DISTRIBUTOR


class LicenceAndFranchisingView(BaseArticleView):
    article = structure.LICENCE_AND_FRANCHISING


class LicenceYourProductOrServiceView(BaseArticleView):
    article = structure.LICENCE_YOUR_PRODUCT_OR_SERVICE


class FranchiseYourBusinessView(BaseArticleView):
    article = structure.FRANCHISE_YOUR_BUSINESS


class StartJointVentureView(BaseArticleView):
    article = structure.START_JOINT_VENTURE


class SetupOverseasOperationView(BaseArticleView):
    article = structure.SETUP_OVERSEAS_OPERATION


class GetMoneyToExportView(BaseArticleView):
    article = structure.GET_MONEY_TO_EXPORT


class ChooseTheRightFinanceView(BaseArticleView):
    article = structure.CHOOSE_THE_RIGHT_FINANCE


class GetExportFinanceView(BaseArticleView):
    article = structure.GET_EXPORT_FINANCE


class RaiseMoneyByBorrowingView(BaseArticleView):
    article = structure.RAISE_MONEY_BY_BORROWING


class BorrowAgainstAssetsView(BaseArticleView):
    article = structure.BORROW_AGAINST_ASSETS


class RaiseMoneyWithInvestmentView(BaseArticleView):
    article = structure.RAISE_MONEY_WITH_INVESTMENT


class GetGovernmentFinanceSupportView(BaseArticleView):
    article = structure.GET_GOVERNMENT_FINANCE_SUPPORT


class ConsiderHowPaidView(BaseArticleView):
    article = structure.CONSIDER_HOW_PAID


class InvoiceCurrencyAndContentsView(BaseArticleView):
    article = structure.INVOICE_CURRENCY_AND_CONTENTS


class DecideWhenPaidView(BaseArticleView):
    article = structure.DECIDE_WHEN_PAID


class PaymentMethodsView(BaseArticleView):
    article = structure.PAYMENT_METHODS


class InsureAgainstNonPaymentView(BaseArticleView):
    article = structure.INSURE_AGAINST_NON_PAYMENT


class PlanTheLogisticsView(BaseArticleView):
    article = structure.PLAN_THE_LOGISTICS


class UseFreightForwarderView(BaseArticleView):
    article = structure.USE_FREIGHT_FORWARDER


class UseIncotermsInContractsView(BaseArticleView):
    article = structure.USE_INCOTERMS_IN_CONTRACTS


class GetYourExportDocumentsRightView(BaseArticleView):
    article = structure.GET_YOUR_EXPORT_DOCUMENTS_RIGHT


class SetupWesbiteView(BaseArticleView):
    article = structure.SETUP_WESBITE


class MatchYourWebsiteToYourAudienceView(BaseArticleView):
    article = structure.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE


class WhatInterlectualPropertyIsView(BaseArticleView):
    article = structure.WHAT_INTERLECTUAL_PROPERTY_IS


class TypesOfInterlectualPropertyView(BaseArticleView):
    article = structure.TYPES_OF_INTERLECTUAL_PROPERTY


class KnowWhatInterlectualPropertyYouHaveView(BaseArticleView):
    article = structure.KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE


class InterlectualPropertyProtectionView(BaseArticleView):
    article = structure.INTERLECTUAL_PROPERTY_PROTECTION


class MeetYourCustomerView(BaseArticleView):
    article = structure.MEET_YOUR_CUSTOMER


class ManageLanguageDifferencesView(BaseArticleView):
    article = structure.MANAGE_LANGUAGE_DIFFERENCES


class UnderstandYourCustomersCultureView(BaseArticleView):
    article = structure.UNDERSTAND_YOUR_CUSTOMERS_CULTURE
