from collections import namedtuple

from directory_constants.constants import exred_articles
from django.urls import reverse_lazy


Article = namedtuple(
    'Article',
    ['uuid', 'title', 'keywords', 'tasks', 'markdown_file_path', 'url',
     'parent']
)
ArticleParent = namedtuple('ArticleParent', ['uuid', 'title', 'articles'])


GUIDANCE_MARKET_RESEARCH = ArticleParent(
    uuid='GUIDANCE_MARKET_RESEARCH',
    title='Market research',
    articles=frozenset((
        exred_articles.DO_RESEARCH_FIRST,
        exred_articles.DEFINE_MARKET_POTENTIAL,
        exred_articles.DO_FIELD_RESEARCH,
        exred_articles.ANALYSE_THE_COMPETITION,
        exred_articles.VISIT_TRADE_SHOW
    ))
)

GUIDANCE_CUSTOMER_INSIGHT = ArticleParent(
    uuid='GUIDANCE_CUSTOMER_INSIGHT',
    title='Customer insight',
    articles=frozenset((
        exred_articles.KNOW_YOUR_CUSTOMER,
        exred_articles.MEET_YOUR_CUSTOMER,
        exred_articles.MANAGE_LANGUAGE_DIFFERENCES,
        exred_articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    ))
)

GUIDANCE_FINANCE = ArticleParent(
    uuid='GUIDANCE_FINANCE',
    title='Finance',
    articles=frozenset((
        exred_articles.GET_MONEY_TO_EXPORT,
        exred_articles.CHOOSE_THE_RIGHT_FINANCE,
        exred_articles.GET_EXPORT_FINANCE,
        exred_articles.RAISE_MONEY_BY_BORROWING,
        exred_articles.BORROW_AGAINST_ASSETS,
        exred_articles.RAISE_MONEY_WITH_INVESTMENT,
        exred_articles.GET_GOVERNMENT_FINANCE_SUPPORT,

    ))
)

GUIDANCE_BUSINESS_PLANNING = ArticleParent(
    uuid='GUIDANCE_BUSINESS_PLANNING',
    title='Business planning',
    articles=frozenset((
        exred_articles.MAKE_EXPORTING_PLAN,
        exred_articles.FIND_A_ROUTE_TO_MARKET,
        exred_articles.USE_OVERSEAS_AGENT,
        exred_articles.USE_DISTRIBUTOR,
        exred_articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        exred_articles.LICENCE_AND_FRANCHISING,
        exred_articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        exred_articles.FRANCHISE_YOUR_BUSINESS,
        exred_articles.START_JOINT_VENTURE,
        exred_articles.SETUP_OVERSEAS_OPERATION,
    ))
)

GUIDANCE_GETTING_PAID = ArticleParent(
    uuid='GUIDANCE_GETTING_PAID',
    title='Getting paid',
    articles=frozenset((
        exred_articles.CONSIDER_HOW_PAID,
        exred_articles.INVOICE_CURRENCY_AND_CONTENTS,
        exred_articles.DECIDE_WHEN_PAID,
        exred_articles.PAYMENT_METHODS,
        exred_articles.INSURE_AGAINST_NON_PAYMENT,
    ))
)

GUIDANCE_OPERATIONS_AND_COMPLIANCE = ArticleParent(
    uuid='GUIDANCE_OPERATIONS_AND_COMPLIANCE',
    title='Operations and compliance',
    articles=frozenset((
        exred_articles.PLAN_THE_LOGISTICS,
        exred_articles.USE_FREIGHT_FORWARDER,
        exred_articles.USE_INCOTERMS_IN_CONTRACTS,
        exred_articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        exred_articles.INTERNATIONALISE_WESBITE,
        exred_articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        exred_articles.WHAT_INTELLECTUAL_PROPERTY_IS,
        exred_articles.TYPES_OF_INTELLECTUAL_PROPERTY,
        exred_articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
        exred_articles.INTELLECTUAL_PROPERTY_PROTECTION,
    ))
)


CATEGORIES_LOOKUP = {
    'GUIDANCE_MARKET_RESEARCH': GUIDANCE_MARKET_RESEARCH,
    'GUIDANCE_CUSTOMER_INSIGHT': GUIDANCE_CUSTOMER_INSIGHT,
    'GUIDANCE_FINANCE': GUIDANCE_FINANCE,
    'GUIDANCE_BUSINESS_PLANNING': GUIDANCE_BUSINESS_PLANNING,
    'GUIDANCE_GETTING_PAID': GUIDANCE_GETTING_PAID,
    'GUIDANCE_OPERATIONS_AND_COMPLIANCE': GUIDANCE_OPERATIONS_AND_COMPLIANCE
}


DO_RESEARCH_FIRST = Article(
    uuid=exred_articles.DO_RESEARCH_FIRST,
    title='Do research first',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/01_do-research-first.md',
    url=reverse_lazy('article-research-market'),
    parent=GUIDANCE_MARKET_RESEARCH,
)
DEFINE_MARKET_POTENTIAL = Article(
    uuid=exred_articles.DEFINE_MARKET_POTENTIAL,
    title='Define market potential',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/02_define-market-potential.md',
    url=reverse_lazy('define-market-potential'),
    parent=GUIDANCE_MARKET_RESEARCH,
)
DO_FIELD_RESEARCH = Article(
    uuid=exred_articles.DO_FIELD_RESEARCH,
    title='Do field research',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/02_define-market-potential.md',
    url=reverse_lazy('do-field-research'),
    parent=GUIDANCE_MARKET_RESEARCH,
)
ANALYSE_THE_COMPETITION = Article(
    uuid=exred_articles.ANALYSE_THE_COMPETITION,
    title='Analyse the competition',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/04_analyse-the-competition.md',
    url=reverse_lazy('analyse-the-competition'),
    parent=GUIDANCE_MARKET_RESEARCH,
)
VISIT_TRADE_SHOW = Article(
    uuid=exred_articles.VISIT_TRADE_SHOW,
    title='Visit a trade show',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/05_visit-a-trade-show.md',
    url=reverse_lazy('visit-trade-show'),
    parent=GUIDANCE_MARKET_RESEARCH,
)
KNOW_YOUR_CUSTOMER = Article(
    uuid=exred_articles.KNOW_YOUR_CUSTOMER,
    title='Know your customers',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/05_know-your-customers.md',
    url=reverse_lazy('know-your-customer'),
    parent=GUIDANCE_CUSTOMER_INSIGHT,
)
MAKE_EXPORTING_PLAN = Article(
    uuid=exred_articles.MAKE_EXPORTING_PLAN,
    title='Make an export plan',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/06_make-an-export-plan.md',
    url=reverse_lazy('make-an-export-plan'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
FIND_A_ROUTE_TO_MARKET = Article(
    uuid=exred_articles.FIND_A_ROUTE_TO_MARKET,
    title='Find a route to market',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/07_find-a-route-to-market.md',
    url=reverse_lazy('find-a-route-to-market'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
USE_OVERSEAS_AGENT = Article(
    uuid=exred_articles.USE_OVERSEAS_AGENT,
    title='Use an overseas agent',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/10_use-an-overseas-agent.md',
    url=reverse_lazy('use-an-overseas-agent'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
USE_DISTRIBUTOR = Article(
    uuid=exred_articles.USE_DISTRIBUTOR,
    title='Use a distributor',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/11_use-a-distributor.md',
    url=reverse_lazy('use-a-distributor'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
CHOOSING_AGENT_OR_DISTRIBUTOR = Article(
    uuid=exred_articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
    title='Choosing an agent or distributor',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/12_choosing-an-agent-or-distributor.md'
    ),
    url=reverse_lazy('choosing-an-agent-or-distributor'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
LICENCE_AND_FRANCHISING = Article(
    uuid=exred_articles.LICENCE_AND_FRANCHISING,
    title='Licensing and franchising',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/13_licensing-and-franchising.md',
    url=reverse_lazy('licensing-and-franchising'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
LICENCE_YOUR_PRODUCT_OR_SERVICE = Article(
    uuid=exred_articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
    title='License your product or service',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/14_license-your-product-or-service.md'
    ),
    url=reverse_lazy('license-your-product-or-service'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
FRANCHISE_YOUR_BUSINESS = Article(
    uuid=exred_articles.FRANCHISE_YOUR_BUSINESS,
    title='Franchise your business',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/15_franchise-your-business.md',
    url=reverse_lazy('franchise-your-business'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
START_JOINT_VENTURE = Article(
    uuid=exred_articles.START_JOINT_VENTURE,
    title='Start a joint venture',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/16_start-a-joint-venture.md',
    url=reverse_lazy('start-a-joint-venture'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
SETUP_OVERSEAS_OPERATION = Article(
    uuid=exred_articles.SETUP_OVERSEAS_OPERATION,
    title='Set up an overseas operation',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/17_set-up-an-overseas-operation.md',
    url=reverse_lazy('set-up-an-overseas-operation'),
    parent=GUIDANCE_BUSINESS_PLANNING,
)
GET_MONEY_TO_EXPORT = Article(
    uuid=exred_articles.GET_MONEY_TO_EXPORT,
    title='Get money to export',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/18_get-money-to-export.md',
    url=reverse_lazy('get-money'),
    parent=GUIDANCE_FINANCE,
)
CHOOSE_THE_RIGHT_FINANCE = Article(
    uuid=exred_articles.CHOOSE_THE_RIGHT_FINANCE,
    title='Choose the right finance',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/19_choose-the-right-finance.md',
    url=reverse_lazy('choose-right-finance'),
    parent=GUIDANCE_FINANCE,
)
GET_EXPORT_FINANCE = Article(
    uuid=exred_articles.GET_EXPORT_FINANCE,
    title='Get export finance',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/20_get-export-finance.md',
    url=reverse_lazy('get-export-finance'),
    parent=GUIDANCE_FINANCE,
)
RAISE_MONEY_BY_BORROWING = Article(
    uuid=exred_articles.RAISE_MONEY_BY_BORROWING,
    title='Raise money by borrowing',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/21_raise-money-by-borrowing.md',
    url=reverse_lazy('raise-money-by-borrowing'),
    parent=GUIDANCE_FINANCE,
)
BORROW_AGAINST_ASSETS = Article(
    uuid=exred_articles.BORROW_AGAINST_ASSETS,
    title='Borrow against assets',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/22_borrow-against-assets.md',
    url=reverse_lazy('borrow-against-assets'),
    parent=GUIDANCE_FINANCE,
)
RAISE_MONEY_WITH_INVESTMENT = Article(
    uuid=exred_articles.RAISE_MONEY_WITH_INVESTMENT,
    title='Raise money with investment',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/23_raise-money-with-investment.md',
    url=reverse_lazy('raise-money-with-investment'),
    parent=GUIDANCE_FINANCE
)
GET_GOVERNMENT_FINANCE_SUPPORT = Article(
    uuid=exred_articles.GET_GOVERNMENT_FINANCE_SUPPORT,
    title='Get government finance support',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/24_get-government-finance-support.md'
    ),
    url=reverse_lazy('get-finance-support-from-government'),
    parent=GUIDANCE_FINANCE,
)
CONSIDER_HOW_PAID = Article(
    uuid=exred_articles.CONSIDER_HOW_PAID,
    title="Consider how you'll get paid",
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/25_consider-how-youll-get-paid.md',
    url=reverse_lazy('consider-how-youll-get-paid'),
    parent=GUIDANCE_GETTING_PAID,
)
INVOICE_CURRENCY_AND_CONTENTS = Article(
    uuid=exred_articles.INVOICE_CURRENCY_AND_CONTENTS,
    title='Invoice currency and contents',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/26_invoice-currency-and-contents.md',
    url=reverse_lazy('invoice-currency-and-contents'),
    parent=GUIDANCE_GETTING_PAID,
)
DECIDE_WHEN_PAID = Article(
    uuid=exred_articles.DECIDE_WHEN_PAID,
    title="Decide when you'll get paid",
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/27_decide-when-youll-get-paid.md',
    url=reverse_lazy('decide-when-youll-get-paid'),
    parent=GUIDANCE_GETTING_PAID,
)
PAYMENT_METHODS = Article(
    uuid=exred_articles.PAYMENT_METHODS,
    title='Payment methods',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/28_payment-methods.md',
    url=reverse_lazy('payment-methods'),
    parent=GUIDANCE_GETTING_PAID,
)
INSURE_AGAINST_NON_PAYMENT = Article(
    uuid=exred_articles.INSURE_AGAINST_NON_PAYMENT,
    title='Insure against non-payment',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/29_insure-against-non-payment.md',
    url=reverse_lazy('insure-against-non-payment'),
    parent=GUIDANCE_GETTING_PAID,
)
PLAN_THE_LOGISTICS = Article(
    uuid=exred_articles.PLAN_THE_LOGISTICS,
    title='Plan the logistics',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/30_plan-the-logistics.md',
    url=reverse_lazy('plan-the-logistics'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
USE_FREIGHT_FORWARDER = Article(
    uuid=exred_articles.USE_FREIGHT_FORWARDER,
    title='Use a freight forwarder',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/31_use-a-freight-forwarder.md',
    url=reverse_lazy('use-a-freight-forwarder'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
USE_INCOTERMS_IN_CONTRACTS = Article(
    uuid=exred_articles.USE_INCOTERMS_IN_CONTRACTS,
    title='User incoterms in contracts',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/32_use-incoterms-in-contracts.md',
    url=reverse_lazy('use-incoterms-in-contracts'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
GET_YOUR_EXPORT_DOCUMENTS_RIGHT = Article(
    uuid=exred_articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
    title='Get your export documents right',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/33_get-your-export-documents-right.md'
    ),
    url=reverse_lazy('get-your-export-documents-right'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
INTERNATIONALISE_WESBITE = Article(
    uuid=exred_articles.INTERNATIONALISE_WESBITE,
    title='Internationalise your website',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/34_internationalise-your-website.md',
    url=reverse_lazy('set-up-a-website'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE = Article(
    uuid=exred_articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
    title='Match your website to your audience',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/35_match-your-website-to-your-audience.md'
    ),
    url=reverse_lazy('match-your-website-to-your-audience'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
WHAT_INTELLECTUAL_PROPERTY_IS = Article(
    uuid=exred_articles.WHAT_INTELLECTUAL_PROPERTY_IS,
    title='What intellectual property is',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/37_what-intellectual-property-is.md'
    ),
    url=reverse_lazy('what-intellectual-property-is'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
TYPES_OF_INTELLECTUAL_PROPERTY = Article(
    uuid=exred_articles.TYPES_OF_INTELLECTUAL_PROPERTY,
    title='Types of intellectual property',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/38_types-of-intellectual-property.md'
    ),
    url=reverse_lazy('types-of-intellectual-property'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE = Article(
    uuid=exred_articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
    title='Know what IP you have',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/39_know-what-IP-you-have.md',
    url=reverse_lazy('know-what-IP-you-have'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE,
)
INTELLECTUAL_PROPERTY_PROTECTION = Article(
    uuid=exred_articles.INTELLECTUAL_PROPERTY_PROTECTION,
    title='IP protection in multiple countries',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/40_ip-protection-in-multiple-countries.md'
    ),
    url=reverse_lazy('ip-protection-in-multiple-countries'),
    parent=GUIDANCE_OPERATIONS_AND_COMPLIANCE
)
MEET_YOUR_CUSTOMER = Article(
    uuid=exred_articles.MEET_YOUR_CUSTOMER,
    title='Meet your customers',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/43_meet-your-customers.md',
    url=reverse_lazy('meet-your-customer'),
    parent=GUIDANCE_CUSTOMER_INSIGHT,
)
MANAGE_LANGUAGE_DIFFERENCES = Article(
    uuid=exred_articles.MANAGE_LANGUAGE_DIFFERENCES,
    title='Manage language differences',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/44_manage-language-differences.md',
    url=reverse_lazy('manage-language-differences'),
    parent=GUIDANCE_CUSTOMER_INSIGHT,
)
UNDERSTAND_YOUR_CUSTOMERS_CULTURE = Article(
    uuid=exred_articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    title="Understand your customer's culture",
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/45_understand-your-customers-culture.md'
    ),
    url=reverse_lazy('understand-your-customers-culture'),
    parent=GUIDANCE_CUSTOMER_INSIGHT,
)
