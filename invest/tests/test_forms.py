from invest import forms


def test_high_potential_opportunity_form_set_field_attributes():
    form_one = forms.HighPotentialOpportunityForm()
    form_two = forms.HighPotentialOpportunityForm(
        field_attributes={
            'full_name': {
                'label': 'Your name',
            },
            'role_in_company': {
                'label': 'Position in company'
            }
        }
    )

    assert form_one.fields['full_name'].label is None
    assert form_one.fields['role_in_company'].label is None
    assert form_two.fields['full_name'].label == 'Your name'
    assert form_two.fields['role_in_company'].label == 'Position in company'
