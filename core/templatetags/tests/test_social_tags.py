from core.templatetags import social_tags


def test_build_social_links():
    actual = social_tags.build_twitter_link(
        'Welcome to the UK',
        'http://exred.trade.great')
    expected = (
        'https://twitter.com/intent/tweet?text=Welcome%20to%20the%20UK%20'
        'http://exred.trade.great')
    assert actual == expected


def test_build_facebook_link():
    actual = social_tags.build_facebook_link(
        'http://exred.trade.great')
    expected = 'https://www.facebook.com/share.php?u=http://exred.trade.great'
    assert actual == expected


def test_build_email_link():
    actual = social_tags.build_email_link(
        'Welcome to the UK',
        'http://exred.trade.great')
    expected = (
        'mailto:?body=http://exred.trade.great'
        '&subject=Welcome%20to%20the%20UK')
    assert actual == expected


def test_build_linkedin_link():
    actual = social_tags.build_linkedin_link(
        'Welcome to the UK',
        'http://exred.trade.great')
    expected = (
        'https://www.linkedin.com/shareArticle?mini=true&url='
        'http://exred.trade.great'
        '&title=Welcome%20to%20the%20UK&source=LinkedIn')
    assert actual == expected
