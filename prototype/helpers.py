
def prefix_international_news_url(path):
    return path.replace(
        '/international/eu-exit-news/',
        '/international/international-eu-exit-news/', 1)


def unslugify(slug):
    return (slug.replace('-', ' ')).capitalize()
