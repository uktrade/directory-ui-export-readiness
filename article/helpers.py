import markdown2

from django.template.loader import render_to_string


def markdown_to_html(markdown_file_path):
    html = render_to_string(markdown_file_path)
    return markdown2.markdown(html)


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
