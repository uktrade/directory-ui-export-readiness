import pytest

from marketaccess import forms
from directory_constants.constants import choices


@pytest.fixture
def about_form_data():
    return {
        'firstname': 'Craig',
        'lastname': 'Smith',
        'jobtitle': 'Musician',
        'categories': "I'm an exporter / seeking to export",
        'company_name': 'Craig Music',
        'email': 'craig@craigmusic.com',
        'phone': '0123456789'
    }


def test_about_form_initial():
    form = forms.AboutForm()
    assert form.fields['firstname'].initial is None
    assert form.fields['lastname'].initial is None
    assert form.fields['jobtitle'].initial is None
    assert form.fields['categories'].initial is None
    assert form.fields['company_name'].initial is None
    assert form.fields['email'].initial is None
    assert form.fields['phone'].initial is None


def test_about_form_mandatory_fields():
    form = forms.AboutForm(data={})

    assert form.fields['firstname'].required is True
    assert form.fields['lastname'].required is True
    assert form.fields['jobtitle'].required is True
    assert form.fields['categories'].required is True
    assert form.fields['company_name'].required is True
    assert form.fields['email'].required is True
    assert form.fields['phone'].required is True


def test_about_form_serialize():
    form = forms.AboutForm(
        data=about_form_data()
    )
    assert form.is_valid()
    assert form.cleaned_data == about_form_data()


@pytest.fixture
def problem_details_form_data():
    return {
        'product_service': 'something',
        'country': 'AO',
        'problem_summary': 'problem summary',
        'impact': 'problem impact',
        'resolve_summary': 'steps in resolving',
        'eu_exit_related': 'False',
    }


def test_about_form_initial():
    form = forms.ProblemDetailsForm()
    assert form.fields['product_service'].initial is None
    assert form.fields['country'].initial is None
    assert form.fields['problem_summary'].initial is None
    assert form.fields['impact'].initial is None
    assert form.fields['resolve_summary'].initial is None
    assert form.fields['eu_exit_related'].initial is None


def test_about_form_mandatory_fields():
    form = forms.ProblemDetailsForm(data={})

    assert form.fields['product_service'].required is True
    assert form.fields['country'].required is True
    assert form.fields['problem_summary'].required is True
    assert form.fields['impact'].required is True
    assert form.fields['resolve_summary'].required is True
    assert form.fields['eu_exit_related'].required is True


def test_problem_details_form_serialize():
    form = forms.ProblemDetailsForm(
        data=problem_details_form_data()
    )
    assert form.is_valid()
    assert form.cleaned_data == problem_details_form_data()


@pytest.fixture
def other_details_form_data():
    return {
        'other_details': 'additional details'
    }


def test_about_form_initial():
    form = forms.OtherDetailsForm()
    assert form.fields['other_details'].initial is None


def test_about_form_mandatory_fields():
    form = forms.OtherDetailsForm(data={})

    assert form.fields['other_details'].required is True


def test_other_details_form_serialize():
    form = forms.OtherDetailsForm(
        data=other_details_form_data()
    )
    assert form.is_valid()
    assert form.cleaned_data == other_details_form_data()
