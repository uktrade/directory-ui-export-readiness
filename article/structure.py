from django.urls import reverse_lazy
from django.utils.functional import cached_property

from article import articles


class ArticleGroup:

    def __init__(self, articles, name, title, url):
        self.articles = articles
        self.name = name
        self.title = title
        self.url = url
        self.articles_set = frozenset(
            [article.uuid for article in self.articles]
        )

    @cached_property
    def total_reading_time(self):
        return round(
            sum((article.time_to_read for article in self.articles))
        )


PERSONA_NEW_ARTICLES = ArticleGroup(
    name='persona_new',
    title='New to exporting',
    articles=[
        articles.DO_RESEARCH_FIRST,
        articles.KNOW_YOUR_CUSTOMER,
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.SELL_OVERSEAS_DIRECTLY,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        articles.MEET_YOUR_CUSTOMER,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.GET_MONEY_TO_EXPORT,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.CONSIDER_HOW_PAID,
        articles.PLAN_THE_LOGISTICS,
        articles.INTERNATIONALISE_WESBITE,
        articles.WHAT_INTELLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTELLECTUAL_PROPERTY,
        articles.NEXT_STEPS_NEW_EXPORTER,
    ],
    url=reverse_lazy('article-list-persona-new'),
)

PERSONA_OCCASIONAL_ARTICLES = ArticleGroup(
    name='persona_occasional',
    title='Occasional exporter',
    articles=[
        articles.DO_RESEARCH_FIRST,
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.VISIT_TRADE_SHOW,
        articles.ANALYSE_THE_COMPETITION,
        articles.KNOW_YOUR_CUSTOMER,
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.SELL_OVERSEAS_DIRECTLY,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.START_JOINT_VENTURE,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
        articles.GET_MONEY_TO_EXPORT,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
        articles.CONSIDER_HOW_PAID,
        articles.INVOICE_CURRENCY_AND_CONTENTS,
        articles.DECIDE_WHEN_PAID,
        articles.PAYMENT_METHODS,
        articles.INSURE_AGAINST_NON_PAYMENT,
        articles.USE_FREIGHT_FORWARDER,
        articles.USE_INCOTERMS_IN_CONTRACTS,
        articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        articles.INTERNATIONALISE_WESBITE,
        articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        articles.WHAT_INTELLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTELLECTUAL_PROPERTY,
        articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTELLECTUAL_PROPERTY_PROTECTION,
        articles.NEXT_STEPS_OCCASIONAL_EXPORTER,
    ],
    url=reverse_lazy('article-list-persona-occasional'),
)

PERSONA_REGULAR_ARTICLES = ArticleGroup(
    name='persona_regular',
    title='Regular exporter',
    articles=[
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.ANALYSE_THE_COMPETITION,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.FRANCHISE_YOUR_BUSINESS,
        articles.START_JOINT_VENTURE,
        articles.SETUP_OVERSEAS_OPERATION,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
        articles.INSURE_AGAINST_NON_PAYMENT,
        articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTELLECTUAL_PROPERTY_PROTECTION,
        articles.NEXT_STEPS_REGULAR_EXPORTER,
    ],
    url=reverse_lazy('article-list-persona-regular'),
)

GUIDANCE_MARKET_RESEARCH_ARTICLES = ArticleGroup(
    name='market_research',
    title=articles.GUIDANCE_MARKET_RESEARCH.title,
    articles=[
        articles.DO_RESEARCH_FIRST,
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.ANALYSE_THE_COMPETITION,
        articles.VISIT_TRADE_SHOW,
    ],
    url=reverse_lazy('article-list-market-research'),
)

GUIDANCE_CUSTOMER_INSIGHT_ARTICLES = ArticleGroup(
    name='customer_insights',
    title=articles.GUIDANCE_CUSTOMER_INSIGHT.title,
    articles=[
        articles.KNOW_YOUR_CUSTOMER,
        articles.MEET_YOUR_CUSTOMER,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
    ],
    url=reverse_lazy('article-list-customer-insight'),
)

GUIDANCE_FINANCE_ARTICLES = ArticleGroup(
    name='finance',
    title=articles.GUIDANCE_FINANCE.title,
    articles=[
        articles.GET_MONEY_TO_EXPORT,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
    ],
    url=reverse_lazy('article-list-finance'),
)

GUIDANCE_BUSINESS_PLANNING_ARTICLES = ArticleGroup(
    name='business_planning',
    title=articles.GUIDANCE_BUSINESS_PLANNING.title,
    articles=[
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.SELL_OVERSEAS_DIRECTLY,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        articles.LICENCE_AND_FRANCHISING,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.FRANCHISE_YOUR_BUSINESS,
        articles.START_JOINT_VENTURE,
        articles.SETUP_OVERSEAS_OPERATION,
    ],
    url=reverse_lazy('article-list-business-planning'),
)

GUIDANCE_GETTING_PAID_ARTICLES = ArticleGroup(
    name='getting_paid',
    title=articles.GUIDANCE_GETTING_PAID.title,
    articles=[
        articles.CONSIDER_HOW_PAID,
        articles.INVOICE_CURRENCY_AND_CONTENTS,
        articles.DECIDE_WHEN_PAID,
        articles.PAYMENT_METHODS,
        articles.INSURE_AGAINST_NON_PAYMENT,
    ],
    url=reverse_lazy('article-list-getting-paid'),
)

GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES = ArticleGroup(
    name='operations_and_compliance',
    title=articles.GUIDANCE_OPERATIONS_AND_COMPLIANCE.title,
    articles=[
        articles.PLAN_THE_LOGISTICS,
        articles.USE_FREIGHT_FORWARDER,
        articles.USE_INCOTERMS_IN_CONTRACTS,
        articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        articles.INTERNATIONALISE_WESBITE,
        articles.WHAT_INTELLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTELLECTUAL_PROPERTY,
        articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTELLECTUAL_PROPERTY_PROTECTION,
    ],
    url=reverse_lazy('article-list-operations-and-compliance'),
)

ALL_ARTICLES = ArticleGroup(
    name='all',
    title='',
    articles=[
        # market research
        articles.DO_RESEARCH_FIRST,
        articles.DEFINE_MARKET_POTENTIAL,
        articles.DO_FIELD_RESEARCH,
        articles.ANALYSE_THE_COMPETITION,
        articles.VISIT_TRADE_SHOW,
        # customer insight
        articles.KNOW_YOUR_CUSTOMER,
        articles.MEET_YOUR_CUSTOMER,
        articles.MANAGE_LANGUAGE_DIFFERENCES,
        articles.UNDERSTAND_YOUR_CUSTOMERS_CULTURE,
        # finance
        articles.GET_MONEY_TO_EXPORT,
        articles.CHOOSE_THE_RIGHT_FINANCE,
        articles.GET_EXPORT_FINANCE,
        articles.RAISE_MONEY_BY_BORROWING,
        articles.BORROW_AGAINST_ASSETS,
        articles.RAISE_MONEY_WITH_INVESTMENT,
        articles.GET_GOVERNMENT_FINANCE_SUPPORT,
        # business planning
        articles.MAKE_EXPORTING_PLAN,
        articles.FIND_A_ROUTE_TO_MARKET,
        articles.SELL_OVERSEAS_DIRECTLY,
        articles.USE_OVERSEAS_AGENT,
        articles.USE_DISTRIBUTOR,
        articles.CHOOSING_AGENT_OR_DISTRIBUTOR,
        articles.LICENCE_AND_FRANCHISING,
        articles.LICENCE_YOUR_PRODUCT_OR_SERVICE,
        articles.FRANCHISE_YOUR_BUSINESS,
        articles.START_JOINT_VENTURE,
        articles.SETUP_OVERSEAS_OPERATION,
        # getting paid
        articles.CONSIDER_HOW_PAID,
        articles.INVOICE_CURRENCY_AND_CONTENTS,
        articles.DECIDE_WHEN_PAID,
        articles.PAYMENT_METHODS,
        articles.INSURE_AGAINST_NON_PAYMENT,
        # operations and compliance
        articles.PLAN_THE_LOGISTICS,
        articles.USE_FREIGHT_FORWARDER,
        articles.USE_INCOTERMS_IN_CONTRACTS,
        articles.GET_YOUR_EXPORT_DOCUMENTS_RIGHT,
        articles.MATCH_YOUR_WEBSITE_TO_YOUR_AUDIENCE,
        articles.INTERNATIONALISE_WESBITE,
        articles.WHAT_INTELLECTUAL_PROPERTY_IS,
        articles.TYPES_OF_INTELLECTUAL_PROPERTY,
        articles.KNOW_WHAT_INTELLECTUAL_PROPERTY_YOU_HAVE,
        articles.INTELLECTUAL_PROPERTY_PROTECTION,
        # next steps
        articles.NEXT_STEPS_NEW_EXPORTER,
        articles.NEXT_STEPS_OCCASIONAL_EXPORTER,
        articles.NEXT_STEPS_REGULAR_EXPORTER,
    ],
    url='',
)

ALL_GROUPS = [
    GUIDANCE_MARKET_RESEARCH_ARTICLES,
    GUIDANCE_CUSTOMER_INSIGHT_ARTICLES,
    GUIDANCE_FINANCE_ARTICLES,
    GUIDANCE_BUSINESS_PLANNING_ARTICLES,
    GUIDANCE_GETTING_PAID_ARTICLES,
    GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES,
    PERSONA_NEW_ARTICLES,
    PERSONA_OCCASIONAL_ARTICLES,
    PERSONA_REGULAR_ARTICLES,
    ALL_ARTICLES,
]
ALL_GROUPS_DICT = {group.name: group for group in ALL_GROUPS}
ALL_ARTICLES_PER_UUID = {article.uuid: article for
                         article in ALL_ARTICLES.articles}


def get_article_group(group_name):
    return ALL_GROUPS_DICT.get(group_name) or ALL_ARTICLES


def get_next_article(article_group, current_article):
    index_in_all = ALL_ARTICLES.articles.index(current_article)
    try:
        current_index = article_group.articles.index(current_article)
        i_group = ALL_GROUPS.index(article_group)
    except ValueError:
        # current article is not in the specified group
        return None
    if current_index + 1 == len(article_group.articles):
        # current item is the last item
        if ALL_GROUPS[i_group] == GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES:
            # don't go to new group
            return None
        if index_in_all + 1 == len(ALL_ARTICLES.articles):
            return None
        return ALL_ARTICLES.articles[index_in_all + 1]
    return article_group.articles[current_index + 1]


def get_next_group(article_group, current_article):
    try:
        current_index = article_group.articles.index(current_article)
        i_group = ALL_GROUPS.index(article_group)
    except ValueError:
        # group does not exist
        return None
    if current_index + 1 == len(article_group.articles):
        # current item is the last item
        if ALL_GROUPS[i_group] == GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES:
            # don't go to new persona group
            return None
        if i_group + 1 == len(ALL_GROUPS):
            return None
        return ALL_GROUPS[i_group + 1]


def get_article_from_uuid(article_uuid):
    return ALL_ARTICLES_PER_UUID[article_uuid]


def get_articles_from_uuids(articles_uuids):
    return (get_article_from_uuid(uuid) for uuid in articles_uuids)


def is_article_in_group(group_name, article):
    group = ALL_GROUPS_DICT.get(group_name)
    return group is not None and article in group.articles
