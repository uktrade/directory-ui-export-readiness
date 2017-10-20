from collections import namedtuple

from django.core.urlresolvers import reverse_lazy


Article = namedtuple(
    'Article',
    ['uuid', 'title', 'keywords', 'tasks', 'markdown_file_path', 'url']
)
ArticleList = namedtuple('ArticleList', ['uuid', 'title', 'articles', 'url'])

DO_RESEARCH_FIRST = Article(
    uuid='DO_RESEARCH_FIRST',
    title='Do research first',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/01_do-research-first.md',
    url=reverse_lazy('article-research-market')
)
DEFINE_MARKET_POTENTIAL = Article(
    uuid='DEFINE_MARKET_POTENTIAL',
    title='Define market potential',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/02_define-market-potential.md',
    url=reverse_lazy('define-market-potential'),
)
DO_FIELD_RESEARCH = Article(
    uuid='DO_FIELD_RESEARCH',
    title='Do field research',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/02_define-market-potential.md',
    url=reverse_lazy('do-field-research'),
)
ANALYSE_THE_COMPETITION = Article(
    uuid='ANALYSE_THE_COMPETITION',
    title='Analyse the competition',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/04_analyse-the-competition.md',
    url=reverse_lazy('analyse-the-competition'),
)
VISIT_TRADE_SHOW = Article(
    uuid='VISIT_TRADE_SHOW',
    title='Visit a trade show',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/05_visit-a-trade-show.md',
    url=reverse_lazy('visit-trade-show'),
)
KNOW_YOUR_CUSTOMER = Article(
    uuid='KNOW_YOUR_CUSTOMER',
    title='Know your customers',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/05_know-your-customers.md',
    url=reverse_lazy('know-your-customer'),
)
MAKE_EXPORTING_PLAN = Article(
    uuid='MAKE_EXPORTING_PLAN',
    title='Make an export plan',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/06_make-an-export-plan.md',
    url=reverse_lazy('make-an-export-plan'),
)
FIND_A_ROUTE_TO_MARKET = Article(
    uuid='FIND_A_ROUTE_TO_MARKET',
    title='Find a route to market',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/07_find-a-route-to-market.md',
    url=reverse_lazy('find-a-route-to-market'),
)
USE_OVERSEAS_AGENT = Article(
    uuid='USE_OVERSEAS_AGENT',
    title='Use an overseas agent',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/10_use-an-overseas-agent.md',
    url=reverse_lazy('use-an-overseas-agent'),
)
USE_DISTRIBUTOR = Article(
    uuid='USE_DISTRIBUTOR',
    title='Use a distributor',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/11_use-a-distributor.md',
    url=reverse_lazy('use-a-distributor'),
)
CHOOSING_AGENT_OR_DISTRIBUTOR = Article(
    uuid='CHOOSING_AGENT_OR_DISTRIBUTOR',
    title='Choosing an agent or distributor',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/12_choosing-an-agent-or-distributor.md'
    ),
    url=reverse_lazy('choosing-an-agent-or-distributor'),
)
LICENCE_AND_FRANCHISING = Article(
    uuid='LICENCE_AND_FRANCHISING',
    title='Licensing and franchising',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/13_licensing-and-franchising.md',
    url=reverse_lazy('licensing-and-franchising'),
)
LICENCE_YOUR_PRODUCT_OR_SERVICE = Article(
    uuid='LICENCE_YOUR_PRODUCT_OR_SERVICE',
    title='License your product or service',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/14_license-your-product-or-service.md'
    ),
    url=reverse_lazy('license-your-product-or-service'),
)
FRANCHISE_YOUR_BUSINESS = Article(
    uuid='FRANCHISE_YOUR_BUSINESS',
    title='Franchise your business',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/15_franchise-your-business.md',
    url=reverse_lazy('franchise-your-business'),
)
START_JOINT_VENTURE = Article(
    uuid='START_JOINT_VENTURE',
    title='Start a joint venture',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/16_start-a-joint-venture.md',
    url=reverse_lazy('start-a-joint-venture'),
)
SETUP_OVERSEAS_OPERATION = Article(
    uuid='SETUP_OVERSEAS_OPERATION',
    title='Set up an overseas operation',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/17_set-up-an-overseas-operation.md',
    url=reverse_lazy('set-up-an-overseas-operation'),
)
GET_MONEY_TO_EXPORT = Article(
    uuid='GET_MONEY_TO_EXPORT',
    title='Get money to export',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/18_get-money-to-export.md',
    url=reverse_lazy('get-money'),
)
CHOOSE_THE_RIGHT_FINANCE = Article(
    uuid='CHOOSE_THE_RIGHT_FINANCE',
    title='Choose the right finance',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/19_choose-the-right-finance.md',
    url=reverse_lazy('choose-right-finance'),
)
GET_EXPORT_FINANCE = Article(
    uuid='GET_EXPORT_FINANCE',
    title='Get export finance',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/20_get-export-finance.md',
    url=reverse_lazy('get-export-finance'),
)
RAISE_MONEY_BY_BORROWING = Article(
    uuid='RAISE_MONEY_BY_BORROWING',
    title='Raise money by borrowing',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/21_raise-money-by-borrowing.md',
    url=reverse_lazy('raise-money-by-borrowing'),
)
BORROW_AGAINST_ASSETS = Article(
    uuid='BORROW_AGAINST_ASSETS',
    title='Borrow against assets',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/22_borrow-against-assets.md',
    url=reverse_lazy('borrow-against-assets'),
)
RAISE_MONEY_WITH_INVESTMENT = Article(
    uuid='RAISE_MONEY_WITH_INVESTMENT',
    title='Raise money with investment',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/23_raise-money-with-investment.md',
    url=reverse_lazy('raise-money-with-investment'),
)
GET_GOVERNMENT_FINANCE_SUPPORT = Article(
    uuid='GET_GOVERNMENT_FINANCE_SUPPORT',
    title='Get government finance support',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/24_get-government-finance-support.md'
    ),
    url=reverse_lazy('get-finance-support-from-government'),
)
CONSIDER_HOW_PAID = Article(
    uuid='CONSIDER_HOW_PAID',
    title="Consider how you'll get paid",
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/25_consider-how-youll-get-paid.md',
    url=reverse_lazy('consider-how-youll-get-paid'),
)
INVOICE_CURRENCY_AND_CONTENTS = Article(
    uuid='INVOICE_CURRENCY_AND_CONTENTS',
    title='Invoice currency and contents',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/26_invoice-currency-and-contents.md',
    url=reverse_lazy('invoice-currency-and-contents'),
)
DECIDE_WHEN_PAID = Article(
    uuid='DECIDE_WHEN_PAID',
    title="Decide when you'll get paid",
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/27_decide-when-youll-get-paid.md',
    url=reverse_lazy('decide-when-youll-get-paid'),
)
PAYMENT_METHODS = Article(
    uuid='PAYMENT_METHODS',
    title='Payment methods',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/28_payment-methods.md',
    url=reverse_lazy('payment-methods'),
)
INSURE_AGAINST_NON_PAYMENT = Article(
    uuid='INSURE_AGAINST_NON_PAYMENT',
    title='Insure against non-payment',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/29_insure-against-non-payment.md',
    url=reverse_lazy('insure-against-non-payment'),
)
PLAN_THE_LOGISTICS = Article(
    uuid='PLAN_THE_LOGISTICS',
    title='Plan the logistics',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/30_plan-the-logistics.md',
    url=reverse_lazy('plan-the-logistics'),
)
USE_FREIGHT_FORWARDER = Article(
    uuid='USE_FREIGHT_FORWARDER',
    title='Use a freight forwarder',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/31_use-a-freight-forwarder.md',
    url=reverse_lazy('use-a-freight-forwarder'),
)
USE_INCOTERMS_IN_CONTRACTS = Article(
    uuid='USE_INCOTERMS_IN_CONTRACTS',
    title='User incoterms in contracts',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/32_use-incoterms-in-contracts.md',
    url=reverse_lazy('use-incoterms-in-contracts'),
)
GET_YOUR_EXPORT_DOCUMENTS_RIGHT = Article(
    uuid='GET_YOUR_EXPORT_DOCUMENTS_RIGHT',
    title='Get your export documents right',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/33_get-your-export-documents-right.md'
    ),
    url=reverse_lazy('get-your-export-documents-right'),
)
INTERNATIONALISE_WESBITE = Article(
    uuid='INTERNATIONALISE_WESBITE',
    title='Internationalise your website',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/34_internationalise-your-website.md',
    url=reverse_lazy('set-up-a-website'),
)
MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE = Article(
    uuid='MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE',
    title='Match your website to your audience',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/35_match-your-website-to-your-audience.md'
    ),
    url=reverse_lazy('match-your-website-to-your-audience'),
)
WHAT_INTERLECTUAL_PROPERTY_IS = Article(
    uuid='WHAT_INTERLECTUAL_PROPERTY_IS',
    title='What intellectual property is',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/37_what-intellectual-property-is.md'
    ),
    url=reverse_lazy('what-intellectual-property-is'),
)
TYPES_OF_INTERLECTUAL_PROPERTY = Article(
    uuid='TYPES_OF_INTERLECTUAL_PROPERTY',
    title='Types of intellectual property',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/38_types-of-intellectual-property.md'
    ),
    url=reverse_lazy('types-of-intellectual-property'),
)
KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE = Article(
    uuid='KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE',
    title='Know what IP you have',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/39_know-what-IP-you-have.md',
    url=reverse_lazy('know-what-IP-you-have'),
)
INTERLECTUAL_PROPERTY_PROTECTION = Article(
    uuid='INTERLECTUAL_PROPERTY_PROTECTION',
    title='IP protection in multiple countries',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/40_ip-protection-in-multiple-countries.md'
    ),
    url=reverse_lazy('ip-protection-in-multiple-countries'),
)
MEET_YOUR_CUSTOMER = Article(
    uuid='MEET_YOUR_CUSTOMER',
    title='Meet your customers',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/43_meet-your-customers.md',
    url=reverse_lazy('meet-your-customer'),
)
MANAGE_LANGUAGE_DIFFERENCES = Article(
    uuid='MANAGE_LANGUAGE_DIFFERENCES',
    title='Manage language differences',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/44_manage-language-differences.md',
    url=reverse_lazy('manage-language-differences'),
)
UNDERSTAND_YOUR_CUSTOMERS_CULTURE = Article(
    uuid='UNDERSTAND_YOUR_CUSTOMERS_CULTURE',
    title="Understand your customer's culture",
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/45_understand-your-customers-culture.md'
    ),
    url=reverse_lazy('understand-your-cutomers-culture'),
)

ARTICLE_LIST_MARKET_RESEARCH = ArticleList(
    uuid='ARTICLE_LIST_MARKET_RESEARCH',
    title='Market research',
    articles=[
        DO_RESEARCH_FIRST,
        DEFINE_MARKET_POTENTIAL,
        DO_FIELD_RESEARCH,
        ANALYSE_THE_COMPETITION,
        VISIT_TRADE_SHOW,
    ],
    url=reverse_lazy('article-list-market-research'),
)

ARTICLE_LIST_CUSTOMER_INSIGHT = ArticleList(
    uuid='ARTICLE_LIST_CUSTOMER_INSIGHT',
    title='Customer insight',
    articles=[
        KNOW_YOUR_CUSTOMER,
        MEET_YOUR_CUSTOMER,
        MANAGE_LANGUAGE_DIFFERENCES,
        UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    ],
    url=reverse_lazy('article-list-customer-insight'),
)
ARTICLE_LIST_FINANCE = ArticleList(
    uuid='ARTICLE_LIST_FINANCE',
    title='Finance',
    articles=[
        GET_MONEY_TO_EXPORT,
        CHOOSE_THE_RIGHT_FINANCE,
        GET_EXPORT_FINANCE,
        RAISE_MONEY_BY_BORROWING,
        BORROW_AGAINST_ASSETS,
        RAISE_MONEY_WITH_INVESTMENT,
        GET_GOVERNMENT_FINANCE_SUPPORT,
    ],
    url=reverse_lazy('article-list-finance'),
)
ARTICLE_LIST_BUSINESS_PLANNING = ArticleList(
    uuid='ARTICLE_LIST_BUSINESS_PLANNING',
    title='Business planning',
    articles=[
        MAKE_EXPORTING_PLAN,
        FIND_A_ROUTE_TO_MARKET,
        USE_OVERSEAS_AGENT,
        USE_DISTRIBUTOR,
        CHOOSING_AGENT_OR_DISTRIBUTOR,
        LICENCE_AND_FRANCHISING,
        LICENCE_YOUR_PRODUCT_OR_SERVICE,
        FRANCHISE_YOUR_BUSINESS,
        START_JOINT_VENTURE,
        SETUP_OVERSEAS_OPERATION,
    ],
    url=reverse_lazy('article-list-business-planning'),
)
ARTICLE_LIST_GETTING_PAID = ArticleList(
    uuid='ARTICLE_LIST_GETTING_PAID',
    title='Getting paid',
    articles=[
        CONSIDER_HOW_PAID,
        INVOICE_CURRENCY_AND_CONTENTS,
        DECIDE_WHEN_PAID,
        PAYMENT_METHODS,
        INSURE_AGAINST_NON_PAYMENT,
    ],
    url=reverse_lazy('article-list-getting-paid')
)
ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE = ArticleList(
    uuid='ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE',
    title='Operations and compliance',
    articles=[
        PLAN_THE_LOGISTICS,
        USE_FREIGHT_FORWARDER,
        USE_INCOTERMS_IN_CONTRACTS,
        GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        INTERNATIONALISE_WESBITE,
        WHAT_INTERLECTUAL_PROPERTY_IS,
        TYPES_OF_INTERLECTUAL_PROPERTY,
        KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE,
        INTERLECTUAL_PROPERTY_PROTECTION,
    ],
    url=reverse_lazy('article-list-operations-and-compliance'),
)
PERSONAS_NEW = [
    DO_RESEARCH_FIRST,
    KNOW_YOUR_CUSTOMER,
    MEET_YOUR_CUSTOMER,
    MANAGE_LANGUAGE_DIFFERENCES,
    GET_MONEY_TO_EXPORT,
]
PERSONAS_OCCASIONAL = [
    DEFINE_MARKET_POTENTIAL,
    DO_FIELD_RESEARCH,
    ANALYSE_THE_COMPETITION,
    KNOW_YOUR_CUSTOMER,
    MANAGE_LANGUAGE_DIFFERENCES,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    GET_MONEY_TO_EXPORT,
    CHOOSE_THE_RIGHT_FINANCE,
    GET_EXPORT_FINANCE,
    RAISE_MONEY_BY_BORROWING,
    BORROW_AGAINST_ASSETS,
    RAISE_MONEY_WITH_INVESTMENT,
    GET_GOVERNMENT_FINANCE_SUPPORT,
    MAKE_EXPORTING_PLAN,
    FIND_A_ROUTE_TO_MARKET,
    USE_OVERSEAS_AGENT,
    USE_DISTRIBUTOR,
    CHOOSING_AGENT_OR_DISTRIBUTOR,
    LICENCE_YOUR_PRODUCT_OR_SERVICE,
    START_JOINT_VENTURE,
    CONSIDER_HOW_PAID,
    INVOICE_CURRENCY_AND_CONTENTS,
    DECIDE_WHEN_PAID,
    PAYMENT_METHODS,
    INSURE_AGAINST_NON_PAYMENT,
    USE_FREIGHT_FORWARDER,
    USE_INCOTERMS_IN_CONTRACTS,
    GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
    MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
    INTERNATIONALISE_WESBITE,
    WHAT_INTERLECTUAL_PROPERTY_IS,
    TYPES_OF_INTERLECTUAL_PROPERTY,
    KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE,
    INTERLECTUAL_PROPERTY_PROTECTION,
]
PERSONAS_REGULAR = [
    DEFINE_MARKET_POTENTIAL,
    DO_FIELD_RESEARCH,
    ANALYSE_THE_COMPETITION,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    CHOOSE_THE_RIGHT_FINANCE,
    GET_EXPORT_FINANCE,
    RAISE_MONEY_BY_BORROWING,
    BORROW_AGAINST_ASSETS,
    RAISE_MONEY_WITH_INVESTMENT,
    GET_GOVERNMENT_FINANCE_SUPPORT,
    LICENCE_YOUR_PRODUCT_OR_SERVICE,
    FRANCHISE_YOUR_BUSINESS,
    START_JOINT_VENTURE,
    SETUP_OVERSEAS_OPERATION,
    INSURE_AGAINST_NON_PAYMENT,
    KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE,
    INTERLECTUAL_PROPERTY_PROTECTION
]
