from django.template import Context, Template


def test_add_anchors():
    template = Template(
        '{% load add_anchors from cms_tags %}'
        '{{ html|add_anchors|safe }}'
    )

    context = Context({
        'html': '<br/><h2>Title one</h2><h2>Title two</h2><br/>'
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h2 id="title-one-section">Title one</h2>'
        '<h2 id="title-two-section">Title two</h2>'
        '<br/>'
    )


def test_add_export_elements_classes():
    template = Template(
        '{% load add_export_elements_classes from cms_tags %}'
        '{{ html|add_export_elements_classes|safe }}'

    )
    context = Context({
        'html': (
            '<br/>'
            '<h1>Title zero</h1>'
            '<h2>Title one</h2>'
            '<h3>Title two</h3>'
            '<ul>List one</ul>'
            '<ol>List two</ol>'
        )
    })
    html = template.render(context)

    assert html == (
        '<br/>'
        '<h1 class="heading-xlarge">Title zero</h1>'
        '<h2 class="heading-large">Title one</h2>'
        '<h3 class="heading-medium">Title two</h3>'
        '<ul class="list list-bullet">List one</ul>'
        '<ol class="list list-number">List two</ol>'
    )
