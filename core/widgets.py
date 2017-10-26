from django.forms import widgets


class RadioSelect(widgets.RadioSelect):
    template_name = 'core/widgets/radio.html'
    option_template_name = 'core/widgets/radio_option.html'
