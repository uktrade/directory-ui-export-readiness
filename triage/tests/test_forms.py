import pytest

from triage import forms


@pytest.mark.parametrize('data', (
    {'company_number': '123124', 'sole_trader': False},
    {'company_number': '', 'sole_trader': False},
    {'company_name': 'example corp', 'sole_trader': False},
))
def test_company_form_company_number_without_sole_trader_acceted(data):
    form = forms.CompanyForm(data=data)

    assert form.is_valid() is True


def test_company_form_pad_company_number():
    form = forms.CompanyForm(data={
        'company_number': '1231245',
    })

    form.is_valid()

    assert form.cleaned_data['company_number'] == '01231245'


def test_company_form_empty_string_company_number():
    form = forms.CompanyForm(data={
        'company_number': '',
    })
    form.is_valid()

    assert form.cleaned_data['company_number'] is None


def test_company_form_null_company_number():
    form = forms.CompanyForm(data={
        'company_number': None,
    })
    form.is_valid()

    assert form.cleaned_data['company_number'] is None


@pytest.mark.parametrize('value,expected', (
    (True, True),
    (False, False),
    (None, False),
))
def test_get_used_marketplace(value, expected):
    answers = {
        'used_online_marketplace': value
    }

    assert forms.get_used_marketplace(answers) is expected


def test_companies_house_form_initial():
    form = forms.CompaniesHouseForm(data={})

    assert form.fields['is_in_companies_house'].initial is None
