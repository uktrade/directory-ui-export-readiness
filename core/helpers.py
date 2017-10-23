def build_social_link(template, request, title):
    return template.format(
        url=request.build_absolute_uri(),
        text='Export Readiness - ' + title,
    )


def build_twitter_link(request, title):
    template = 'https://twitter.com/intent/tweet?text={text} {url}'
    return build_social_link(template, request, title)


def build_facebook_link(request, title):
    template = 'http://www.facebook.com/share.php?u={url}'
    return build_social_link(template, request, title)


def build_linkedin_link(request, title):
    template = (
        'https://www.linkedin.com/shareArticle'
        '?mini=true&url={url}&title={text}&source=LinkedIn'
    )
    return build_social_link(template, request, title)


def build_email_link(request, title):
    template = 'mailto:?body={text}&subject={url}'
    return build_social_link(template, request, title)


def build_social_links(request, title):
    kwargs = {'request': request, 'title': title}
    return {
        'facebook': build_facebook_link(**kwargs),
        'twitter': build_twitter_link(**kwargs),
        'linkedin': build_linkedin_link(**kwargs),
        'email': build_email_link(**kwargs),
    }
