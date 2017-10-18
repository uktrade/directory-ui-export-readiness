from django.views.generic import TemplateView


class BaseArticleView(TemplateView):
    template_name = 'article/base.html'

    def get_context_data(self, *args, **kwargs):
        article = {
            'markdown_file_path': self.markdown_file_path
        }
        return super().get_context_data(*args, **kwargs, article=article)


class DoResearchFirstView(BaseArticleView):
    markdown_file_path = 'article/markdown/01_do-research-first.md'


class DefineMarketPotentialView(BaseArticleView):
    markdown_file_path = 'article/markdown/02_define-market-potential.md'


class DoFieldResearchView(BaseArticleView):
    markdown_file_path = 'article/markdown/03_do-field-research.md'


class AnalyseTheCompetitionView(BaseArticleView):
    markdown_file_path = 'article/markdown/04_analyse-the-competition.md'


class VisitTradeShowView(BaseArticleView):
    markdown_file_path = 'article/markdown/05_visit-a-trade-show.md'


class KnowYourCustomerView(BaseArticleView):
    markdown_file_path = 'article/markdown/05_know-your-customers.md'


class MakeExportingPlanView(BaseArticleView):
    markdown_file_path = 'article/markdown/06_make-an-export-plan.md'


class FindARouteToMarketView(BaseArticleView):
    markdown_file_path = 'article/markdown/07_find-a-route-to-market.md'


class UseOverseasAgentView(BaseArticleView):
    markdown_file_path = 'article/markdown/10_use-an-overseas-agent.md'


class UseDistributorView(BaseArticleView):
    markdown_file_path = 'article/markdown/11_use-a-distributor.md'


class ChoosingAgentOrDistributorView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/12_choosing-an-agent-or-distributor.md'
    )


class LicenceAndFranchisingView(BaseArticleView):
    markdown_file_path = 'article/markdown/13_licensing-and-franchising.md'


class LicenceYourProductOrServiceView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/14_license-your-product-or-service.md'
    )


class FranchiseYourBusinessView(BaseArticleView):
    markdown_file_path = 'article/markdown/15_franchise-your-business.md'


class StartJointVentureView(BaseArticleView):
    markdown_file_path = 'article/markdown/16_start-a-joint-venture.md'


class SetupOverseasOperationView(BaseArticleView):
    markdown_file_path = 'article/markdown/17_set-up-an-overseas-operation.md'


class GetMoneyToExportView(BaseArticleView):
    markdown_file_path = 'article/markdown/18_get-money-to-export.md'


class ChooseTheRightFinanceView(BaseArticleView):
    markdown_file_path = 'article/markdown/19_choose-the-right-finance.md'


class GetExportFinanceView(BaseArticleView):
    markdown_file_path = 'article/markdown/20_get-export-finance.md'


class RaiseMoneyByBorrowingView(BaseArticleView):
    markdown_file_path = 'article/markdown/21_raise-money-by-borrowing.md'


class BorrowAgainstAssetsView(BaseArticleView):
    markdown_file_path = 'article/markdown/22_borrow-against-assets.md'


class RaiseMoneyWithInvestmentView(BaseArticleView):
    markdown_file_path = 'article/markdown/23_raise-money-with-investment.md'


class GetGovernmentFinanceSupportView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/24_get-government-finance-support.md'
    )


class ConsiderHowPaidView(BaseArticleView):
    markdown_file_path = 'article/markdown/25_consider-how-youll-get-paid.md'


class InvoiceCurrencyAndContentsView(BaseArticleView):
    markdown_file_path = 'article/markdown/26_invoice-currency-and-contents.md'


class DecideWhenPaidView(BaseArticleView):
    markdown_file_path = 'article/markdown/27_decide-when-youll-get-paid.md'


class PaymentMethodsView(BaseArticleView):
    markdown_file_path = 'article/markdown/28_payment-methods.md'


class InsureAgainstNonPaymentView(BaseArticleView):
    markdown_file_path = 'article/markdown/29_insure-against-non-payment.md'


class PlanTheLogisticsView(BaseArticleView):
    markdown_file_path = 'article/markdown/30_plan-the-logistics.md'


class UseFreightForwarderView(BaseArticleView):
    markdown_file_path = 'article/markdown/31_use-a-freight-forwarder.md'


class UseIncotermsInContractsView(BaseArticleView):
    markdown_file_path = 'article/markdown/32_use-incoterms-in-contracts.md'


class GetYourExportDocumentsRightView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/33_get-your-export-documents-right.md'
    )


class SetupWesbiteView(BaseArticleView):
    markdown_file_path = 'article/markdown/35_set-up-a-website.md'


class MatchYourWebsiteToYourAudienceView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/35_match-your-website-to-your-audience.md'
    )


class WhatInterlectualPropertyIsView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/37_what-intellectual-property-is.md'
    )


class TypesOfInterlectualPropertyView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/38_types-of-intellectual-property.md'
    )


class KnowWhatInterlectualPropertyYouHaveView(BaseArticleView):
    markdown_file_path = 'article/markdown/39_know-what-IP-you-have.md'


class InterlectualPropertyProtectionView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/40_ip-protection-in-multiple-countries.md'
    )


class MeetYourCustomerView(BaseArticleView):
    markdown_file_path = 'article/markdown/43_meet-your-customers.md'


class ManageLanguageDifferencesView(BaseArticleView):
    markdown_file_path = 'article/markdown/44_manage-language-differences.md'


class UnderstandYourCustomersCultureView(BaseArticleView):
    markdown_file_path = (
        'article/markdown/45_understand-your-customers-culture.md'
    )
