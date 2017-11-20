from django.utils import translation


class TranslationsMixin:
    template_name_bidi = None

    def dispatch(self, request, *args, **kwargs):
        translation.activate(request.LANGUAGE_CODE)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['LANGUAGE_BIDI'] = translation.get_language_bidi()
        return context

    def get_template_names(self):
        if translation.get_language_bidi():
            return [self.template_name_bidi]
        return super().get_template_names()
