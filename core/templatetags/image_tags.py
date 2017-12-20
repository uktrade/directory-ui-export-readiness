from django import template
from django.template.loader import render_to_string
from django.templatetags import static

register = template.Library()


@register.simple_tag
def progressive_image(webp, src, img_id='', alt_text=''):
    context = {
        'src': src,
        'webp': webp,
        'alt_text': alt_text,
        'img_id': img_id
        }
    return render_to_string('core/widgets/progressive_image.html', context)


class FullStaticNode(static.StaticNode):
    def url(self, context):
        request = context['request']
        return request.build_absolute_uri(super().url(context))


@register.tag
def get_image_absolute_uri(parser, token):
    return FullStaticNode.handle_token(parser, token)
