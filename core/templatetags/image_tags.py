from django import template
from django.template.loader import render_to_string

register = template.Library()


@register.simple_tag
def progressive_image(webp, src, img_id='', alt_text=''):
    context = {'src': src, 'webp': webp, 'alt_text': alt_text, 'img_id': img_id}
    return render_to_string('core/widgets/progressive_image.html', context)
