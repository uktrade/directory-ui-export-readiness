from euexit import forms


def test_international_contact_form_set_field_attributes():
    form_one = forms.InternationalContactForm(
        field_attributes={},
    )
    form_two = forms.InternationalContactForm(
        field_attributes={
            'first_name': {
                'label': 'Your given name',
            },
            'last_name': {
                'label': 'Your family name'
            }
        },
    )

    assert form_one.fields['first_name'].label is None
    assert form_one.fields['last_name'].label is None
    assert form_two.fields['first_name'].label == 'Your given name'
    assert form_two.fields['last_name'].label == 'Your family name'
