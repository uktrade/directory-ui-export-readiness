import pytest

from triage import forms
from directory_constants.constants import exred_sector_names


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


def test_regular_exporter_optional_fields():
    form = forms.RegularExporterForm(data={})

    assert form.fields['regular_exporter'].required is False


def test_online_marketplace_optional_fields():
    form = forms.OnlineMarketplaceForm(data={})

    assert form.fields['used_online_marketplace'].required is False


def test_company_form_optional_fields():
    form = forms.CompanyForm(data={})

    assert form.fields['company_name'].required is False
    assert form.fields['company_number'].required is False


def test_custom_page_sector_form():
    form = forms.SectorForm(data={
        'sector': 'HS01',
    })

    form.is_valid()

    assert form.cleaned_data['sector'] == 'HS01'


def test_get_sector_label():
    for key, label in exred_sector_names.SECTORS_CHOICES:
        data = {'sector': key}
        assert forms.get_sector_label(data) == label
