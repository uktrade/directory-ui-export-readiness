from django import template


register = template.Library()


@register.filter
def humanize_millions(value, word=' million'):
    value = int(value)
    return '{value}{word}'.format(value=int(value / 1000000), word=word)


@register.filter
def humanize_billions(value):
    value = int(value.replace(",", ""))
    return '{value}bn'.format(value=int(value / 1000))
