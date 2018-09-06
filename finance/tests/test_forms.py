from finance import forms


def test_company_detail_form_no_company_number():
    form = forms.CompanyDetailsForm(data={})
    assert form.is_valid() is False
    assert form.errors['company_number'] == ['This field is required.']


def test_company_detail_form_no_company_number_not_companies_house():
    form = forms.CompanyDetailsForm(data={'not_companies_house': True})
    assert form.is_valid() is False
    assert 'company_number' not in form.errors
