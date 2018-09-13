from invest import forms


def test_high_potential_opportunity_form_set_field_attributes():
    form_one = forms.HighPotentialOpportunityForm(
        field_attributes={},
        opportunity_choices=[]
    )
    form_two = forms.HighPotentialOpportunityForm(
        field_attributes={
            'full_name': {
                'label': 'Your name',
            },
            'role_in_company': {
                'label': 'Position in company'
            }
        },
        opportunity_choices=[
            ('http://www.example.com/a', 'some great opportunity'),
        ]
    )

    assert form_one.fields['full_name'].label is None
    assert form_one.fields['role_in_company'].label is None
    assert form_two.fields['full_name'].label == 'Your name'
    assert form_two.fields['role_in_company'].label == 'Position in company'
    assert form_two.fields['opportunities'].choices == [
        ('http://www.example.com/a', 'some great opportunity'),
    ]


def test_high_potential_opportunity_form_serialize_data():
    form = forms.HighPotentialOpportunityForm(
        data={
            'full_name': 'Jim Example',
            'role_in_company': 'Chief chief',
            'email_address': 'test@example.com',
            'phone_number': '555',
            'company_name': 'Example corp',
            'website_url': 'example.com',
            'country': 'UK',
            'company_size': '1 - 10',
            'opportunities': [
                'http://www.e.com/a',
                'http://www.e.com/b',
            ],
            'comment': 'hello',
            'terms_agreed': True,
        },
        field_attributes={},
        opportunity_choices=[
            ('http://www.e.com/a', 'some great opportunity'),
            ('http://www.e.com/b', 'some other great opportunity'),
        ]
    )

    assert form.is_valid()
    assert form.serialized_data == {
        'full_name': 'Jim Example',
        'role_in_company': 'Chief chief',
        'email_address': 'test@example.com',
        'phone_number': '555',
        'company_name': 'Example corp',
        'website_url': 'example.com',
        'country': 'UK',
        'company_size': '1 - 10',
        'opportunities': [
            'http://www.e.com/a',
            'http://www.e.com/b',
        ],
        'opportunity_urls': 'http://www.e.com/a\nhttp://www.e.com/b',
        'comment': 'hello',
        'terms_agreed': True,
    }
