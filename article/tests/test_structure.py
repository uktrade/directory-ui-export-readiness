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


def test_article_group_total_reading_time():
    group = structure.PERSONA_NEW_ARTICLES
    assert group.total_reading_time == 808.0
