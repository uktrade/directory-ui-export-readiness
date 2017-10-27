from article import articles


def test_article_time_to_read():
    article = articles.CONSIDER_HOW_PAID
    assert article.time_to_read == 0.27
