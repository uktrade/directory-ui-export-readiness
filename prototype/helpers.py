

def unprefix_prototype_url(path):
    return path.replace('/prototype', '', 1)


def prefix_international_news_url(path):
    return path.replace(
        '/international/news/',
        '/international/international-news/', 1)
