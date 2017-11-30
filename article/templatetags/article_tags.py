from django import template
from django.utils.html import mark_safe
from django.urls import resolve, reverse

from article import helpers, structure


register = template.Library()


@register.simple_tag(takes_context=True)
def include_markdown(context, markdown_file_path):
    html = helpers.markdown_to_html(
        markdown_file_path=markdown_file_path,
        context=context.flatten(),
    )
    return mark_safe(html)


@register.filter
def time_to_read(value):
    if value <= 59:
        return 'Less than 1 minute'
    minutes = int(round(value / 60))
    unit = 'min' if minutes == 1 else 'mins'
    return '{minutes} {unit}'.format(minutes=minutes, unit=unit)


@register.simple_tag(takes_context=True)
def url_with_source(context, url_name):
    """Add "?source=..." to the end of a url

    Use the current active article list if the article in the requested url
    is in the current article list, otherwise look though all other article
    lists and pick the first valid.

    Arguments:
        context {dict}
        url_name {str}

    Returns:
        str -- A relative url with "?source=..."

    """

    source = 'all'
    url = reverse(url_name)
    if 'request' in context:
        article = resolve(url).func.view_class.article
        group_names = [
            context['request'].GET.get('source'),
            structure.GUIDANCE_MARKET_RESEARCH_ARTICLES.name,
            structure.GUIDANCE_CUSTOMER_INSIGHT_ARTICLES.name,
            structure.GUIDANCE_FINANCE_ARTICLES.name,
            structure.GUIDANCE_BUSINESS_PLANNING_ARTICLES.name,
            structure.GUIDANCE_GETTING_PAID_ARTICLES.name,
            structure.GUIDANCE_OPERATIONS_AND_COMPLIANCE_ARTICLES.name,
        ]
        for group_name in group_names:
            if structure.is_article_in_group(group_name, article):
                source = group_name
                break
    return url + '?source=' + source
