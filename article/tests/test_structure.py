import pytest

from article import articles, structure


def test_get_article_group():
    group = structure.GUIDANCE_MARKET_RESEARCH_ARTICLES
    assert structure.get_article_group(group.name) == group


def test_get_article_group_missing_key():
    assert structure.get_article_group('foo') == structure.ALL_ARTICLES


def test_get_article_from_uuid():
    article = articles.DO_RESEARCH_FIRST
    assert structure.get_article_from_uuid(article.uuid) == article


def test_get_articles_from_uuids():
    articles_list = [
        articles.DO_RESEARCH_FIRST,
        articles.CONSIDER_HOW_PAID
    ]
    articles_returned = structure.get_articles_from_uuids(
        [article.uuid for article in articles_list]
    )
    assert list(articles_returned) == articles_list


def test_article_group_read_time():
    group = structure.PERSONA_NEW_ARTICLES
    assert group.read_time == 2620


@pytest.mark.parametrize(
    'current_group, expected_next_group',
    (
        (
            structure.GUIDANCE_MARKET_RESEARCH_ARTICLES,
            structure.GUIDANCE_CUSTOMER_INSIGHT_ARTICLES
        ),
        (
            structure.GUIDANCE_CUSTOMER_INSIGHT_ARTICLES,
            structure.GUIDANCE_FINANCE_ARTICLES
        ),
        (
            structure.GUIDANCE_FINANCE_ARTICLES,
            structure.GUIDANCE_BUSINESS_PLANNING_ARTICLES
        ),
        (
            structure.GUIDANCE_BUSINESS_PLANNING_ARTICLES,
            structure.GUIDANCE_GETTING_PAID_ARTICLES
        ),
        (
            structure.GUIDANCE_GETTING_PAID_ARTICLES,
            structure.GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES
        ),
        (
            structure.GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES,
            None
        ),
        (
            structure.ALL_ARTICLES,
            None
        ),
        (
            structure.PERSONA_NEW_ARTICLES,
            None
        ),
        (
            structure.PERSONA_OCCASIONAL_ARTICLES,
            None
        ),
        (
            structure.PERSONA_REGULAR_ARTICLES,
            None
        )
    ),
    ids=(
        'Market research',
        'Customer insight',
        'Finance',
        'Business planning',
        'Getting paid',
        'Operations and compliance',
        'All articles',
        'Persona new article',
        'Persona occasional articles',
        'Persona regular articles'
    )
)
def test_next_guidance_category(current_group, expected_next_group):
    assert current_group.next_guidance_group == expected_next_group
