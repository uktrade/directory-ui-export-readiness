from collections import namedtuple

Article = namedtuple(
    'article',
    ['uuid', 'title', 'keywords', 'tasks', 'markdown_file_path']
)

DO_RESEARCH_FIRST = Article(
    uuid='DO_RESEARCH_FIRST',
    title='Do research first',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/01_do-research-first.md',
)
DEFINE_MARKET_POTENTIAL = Article(
    uuid='DEFINE_MARKET_POTENTIAL',
    title='Define market potential',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/02_define-market-potential.md',
)
DO_FIELD_RESEARCH = Article(
    uuid='DO_FIELD_RESEARCH',
    title='Do field research',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/02_define-market-potential.md',
)
ANALYSE_THE_COMPETITION = Article(
    uuid='ANALYSE_THE_COMPETITION',
    title='Analyse the competition',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/04_analyse-the-competition.md',
)
VISIT_TRADE_SHOW = Article(
    uuid='VISIT_TRADE_SHOW',
    title='Visit a trade show',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/05_visit-a-trade-show.md',
)
KNOW_YOUR_CUSTOMER = Article(
    uuid='KNOW_YOUR_CUSTOMER',
    title='Know your customers',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/05_know-your-customers.md',

)
MAKE_EXPORTING_PLAN = Article(
    uuid='MAKE_EXPORTING_PLAN',
    title='Make an export plan',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/06_make-an-export-plan.md',
)
FIND_A_ROUTE_TO_MARKET = Article(
    uuid='FIND_A_ROUTE_TO_MARKET',
    title='Find a route to market',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/07_find-a-route-to-market.md',
)
USE_OVERSEAS_AGENT = Article(
    uuid='USE_OVERSEAS_AGENT',
    title='Use an overseas agent',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/10_use-an-overseas-agent.md',
)
USE_DISTRIBUTOR = Article(
    uuid='USE_DISTRIBUTOR',
    title='Use a distributor',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/11_use-a-distributor.md',
)
CHOOSING_AGENT_OR_DISTRIBUTOR = Article(
    uuid='CHOOSING_AGENT_OR_DISTRIBUTOR',
    title='Choosing an agent or distributor',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/12_choosing-an-agent-or-distributor.md'
    )
)
LICENCE_AND_FRANCHISING = Article(
    uuid='LICENCE_AND_FRANCHISING',
    title='Licensing and franchising',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/13_licensing-and-franchising.md',
)
LICENCE_YOUR_PRODUCT_OR_SERVICE = Article(
    uuid='LICENCE_YOUR_PRODUCT_OR_SERVICE',
    title='License your product or service',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/14_license-your-product-or-service.md'
    ),
)
FRANCHISE_YOUR_BUSINESS = Article(
    uuid='FRANCHISE_YOUR_BUSINESS',
    title='Franchise your business',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/15_franchise-your-business.md',
)
START_JOINT_VENTURE = Article(
    uuid='START_JOINT_VENTURE',
    title='Start a joint venture',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/16_start-a-joint-venture.md',
)
SETUP_OVERSEAS_OPERATION = Article(
    uuid='SETUP_OVERSEAS_OPERATION',
    title='Set up an overseas operation',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/17_set-up-an-overseas-operation.md',
)
GET_MONEY_TO_EXPORT = Article(
    uuid='GET_MONEY_TO_EXPORT',
    title='Get money to export',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/18_get-money-to-export.md',
)
CHOOSE_THE_RIGHT_FINANCE = Article(
    uuid='CHOOSE_THE_RIGHT_FINANCE',
    title='Choose the right finance',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/19_choose-the-right-finance.md',
)
GET_EXPORT_FINANCE = Article(
    uuid='GET_EXPORT_FINANCE',
    title='Get export finance',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/20_get-export-finance.md',
)
RAISE_MONEY_BY_BORROWING = Article(
    uuid='RAISE_MONEY_BY_BORROWING',
    title='Raise money by borrowing',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/21_raise-money-by-borrowing.md',
)
BORROW_AGAINST_ASSETS = Article(
    uuid='BORROW_AGAINST_ASSETS',
    title='Borrow against assets',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/22_borrow-against-assets.md',
)
RAISE_MONEY_WITH_INVESTMENT = Article(
    uuid='RAISE_MONEY_WITH_INVESTMENT',
    title='Raise money with investment',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/23_raise-money-with-investment.md',
)
GET_GOVERNMENT_FINANCE_SUPPORT = Article(
    uuid='GET_GOVERNMENT_FINANCE_SUPPORT',
    title='Get government finance support',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/24_get-government-finance-support.md'
    ),
)
CONSIDER_HOW_PAID = Article(
    uuid='CONSIDER_HOW_PAID',
    title="Consider how you'll get paid",
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/25_consider-how-youll-get-paid.md',
)
INVOICE_CURRENCY_AND_CONTENTS = Article(
    uuid='INVOICE_CURRENCY_AND_CONTENTS',
    title='Invoice currency and contents',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/26_invoice-currency-and-contents.md'
)
DECIDE_WHEN_PAID = Article(
    uuid='DECIDE_WHEN_PAID',
    title="Decide when you'll get paid",
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/27_decide-when-youll-get-paid.md',
)
PAYMENT_METHODS = Article(
    uuid='PAYMENT_METHODS',
    title='Payment methods',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/28_payment-methods.md'
)
INSURE_AGAINST_NON_PAYMENT = Article(
    uuid='INSURE_AGAINST_NON_PAYMENT',
    title='Insure against non-payment',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/29_insure-against-non-payment.md'
)
PLAN_THE_LOGISTICS = Article(
    uuid='PLAN_THE_LOGISTICS',
    title='Plan the logistics',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/30_plan-the-logistics.md',
)
USE_FREIGHT_FORWARDER = Article(
    uuid='USE_FREIGHT_FORWARDER',
    title='Use a freight forwarder',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/31_use-a-freight-forwarder.md',
)
USE_INCOTERMS_IN_CONTRACTS = Article(
    uuid='USE_INCOTERMS_IN_CONTRACTS',
    title='User incoterms in contracts',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/32_use-incoterms-in-contracts.md'
)
GET_YOUR_EXPORT_DOCUMENTS_RIGHT = Article(
    uuid='GET_YOUR_EXPORT_DOCUMENTS_RIGHT',
    title='Get your export documents right',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/33_get-your-export-documents-right.md'
    ),
)
INTERNATIONALISE_WESBITE = Article(
    uuid='INTERNATIONALISE_WESBITE',
    title='Internationalise your website',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/34_internationalise-your-website.md'
)
MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE = Article(
    uuid='MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE',
    title='Match your website to your audience',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/35_match-your-website-to-your-audience.md'
    )
)
WHAT_INTERLECTUAL_PROPERTY_IS = Article(
    uuid='WHAT_INTERLECTUAL_PROPERTY_IS',
    title='What intellectual property is',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/37_what-intellectual-property-is.md'
    ),
)
TYPES_OF_INTERLECTUAL_PROPERTY = Article(
    uuid='TYPES_OF_INTERLECTUAL_PROPERTY',
    title='Types of intellectual property',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/38_types-of-intellectual-property.md'
    ),
)
KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE = Article(
    uuid='KNOW_WHAT_INTERLECTUAL_PROPERTY_YOU_HAVE',
    title='Know what IP you have',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/39_know-what-IP-you-have.md',
)
INTERLECTUAL_PROPERTY_PROTECTION = Article(
    uuid='INTERLECTUAL_PROPERTY_PROTECTION',
    title='IP protection in multiple countries',
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/40_ip-protection-in-multiple-countries.md'
    ),
)
MEET_YOUR_CUSTOMER = Article(
    uuid='MEET_YOUR_CUSTOMER',
    title='Meet your customers',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/43_meet-your-customers.md',
)
MANAGE_LANGUAGE_DIFFERENCES = Article(
    uuid='MANAGE_LANGUAGE_DIFFERENCES',
    title='Manage language differences',
    keywords=[],
    tasks=[],
    markdown_file_path='article/markdown/44_manage-language-differences.md',
)
UNDERSTAND_YOUR_CUSTOMERS_CULTURE = Article(
    uuid='UNDERSTAND_YOUR_CUSTOMERS_CULTURE',
    title="Understand your customer's culture",
    keywords=[],
    tasks=[],
    markdown_file_path=(
        'article/markdown/45_understand-your-customers-culture.md'
    )
)


ARTICLE_LIST_MARKET_RESEARCH = [
    DO_RESEARCH_FIRST,
    DEFINE_MARKET_POTENTIAL,
    DO_FIELD_RESEARCH,
    ANALYSE_THE_COMPETITION,
    VISIT_TRADE_SHOW,
]

ARTICLE_LIST_CUSTOMER_INSIGHT = [
    KNOW_YOUR_CUSTOMER,
    MEET_YOUR_CUSTOMER,
    MANAGE_LANGUAGE_DIFFERENCES,
    UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
]
ARTICLE_LIST_FINANCE = [
    GET_MONEY_TO_EXPORT,
    CHOOSE_THE_RIGHT_FINANCE,
    GET_EXPORT_FINANCE,
    RAISE_MONEY_BY_BORROWING,
    BORROW_AGAINST_ASSETS,
    RAISE_MONEY_WITH_INVESTMENT,
    GET_GOVERNMENT_FINANCE_SUPPORT,
]
ARTICLE_LIST_BUSINESS_PLANNING = [
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
]
ARTICLE_LIST_GETTING_PAID = [
    CONSIDER_HOW_PAID,
    INVOICE_CURRENCY_AND_CONTENTS,
    DECIDE_WHEN_PAID,
    PAYMENT_METHODS,
    INSURE_AGAINST_NON_PAYMENT,
]
ARTICLE_LIST_OPERATIONS_AND_COMPLIANCE = [
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
]
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
