from contact import constants, forms, views


routing_steps = [step for step, _ in views.RoutingFormView.form_list]


def test_location_form_routing():
    field = forms.LocationRoutingForm.base_fields['choice']
    # for each of the choices the form supports
    for choice, _ in field.choices:
        # the view supports routing the user to that step
        assert choice in routing_steps


def test_domestic_form_routing():
    field = forms.DomesticRoutingForm.base_fields['choice']
    choices = set(item for item, _ in field.choices)

    # expect these choices to result in a redirect to a new form
    choices_expect_redirect = {
        constants.TRADE_OFFICE,
        constants.EXPORT_ADVICE,
        constants.FINANCE,
        constants.EUEXIT,
        constants.EVENTS,
        constants.DSO,
        constants.OTHER,
    }
    mapping = views.RoutingFormView.redirect_mapping[constants.DOMESTIC]

    for choice in choices_expect_redirect:
        assert choice in choices
        assert choice in mapping
        assert choice not in routing_steps

    choices_expect_next_step = (constants.GREAT_SERVICES,)
    for choice in choices_expect_next_step:
        assert choice in choices
        assert choice not in mapping
        assert choice in routing_steps

    expected_choice_count = (
        len(choices_expect_next_step) + len(choices_expect_redirect)
    )

    assert expected_choice_count == len(choices)


def test_great_services_form_routing():
    field = forms.GreatServicesRoutingForm.base_fields['choice']
    # for each of the choices the form supports
    for choice, _ in field.choices:
        # the view supports routing the user to that step
        assert choice in routing_steps


def test_export_oppotunities_form_routing():
    field = forms.ExportOpportunitiesRoutingForm.base_fields['choice']

    mapping = (
        views.RoutingFormView.redirect_mapping[constants.EXPORT_OPPORTUNITIES]
    )

    for choice, _ in field.choices:
        assert choice in mapping
        assert choice not in routing_steps


def test_great_account_form_routing():
    # expect these to route to a FAQ page
    pass


def test_international_form_routing():
    field = forms.InternationalRoutingForm.base_fields['choice']
    mapping = views.RoutingFormView.redirect_mapping[constants.INTERNATIONAL]
    for choice, _ in field.choices:
        assert choice in mapping
        assert choice not in routing_steps
