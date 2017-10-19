import pytest

from triage import forms


def test_company_form_company_number_and_sole_trader_throws_error():
    form = forms.CompanyForm(data={
        'company_number': '123124',
        'sole_trader': True,
    })

    assert form.is_valid() is False
    assert form.errors['sole_trader'] == [form.MESSAGE_MUTUALLY_EXCLUSIVE]


@pytest.mark.parametrize('data', (
    {'company_number': '123124', 'sole_trader': False},
    {'company_number': '', 'sole_trader': False},
    {'company_name': 'example corp', 'sole_trader': False},
))
def test_company_form_company_number_without_sole_trader_acceted(data):
    form = forms.CompanyForm(data=data)

    assert form.is_valid() is True
