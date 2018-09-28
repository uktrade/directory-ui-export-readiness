from finance import forms


def test_company_detail_form_no_company_number():
    form = forms.CompanyDetailsForm(data={})
    assert form.is_valid() is False
    assert form.errors['company_number'] == ['This field is required.']


def test_company_detail_form_no_company_number_not_companies_house():
    form = forms.CompanyDetailsForm(data={'not_companies_house': True})
    assert form.is_valid() is False
    assert 'company_number' not in form.errors


def test_compamy_detail_form_industry_options():
    form = forms.CompanyDetailsForm()

    assert form.fields['industry'].choices == [
        ('', ''),
        ('Aerospace', 'Aerospace'),
        ('Advanced Manufacturing', 'Advanced manufacturing'),
        ('Airports', 'Airports'),
        (
            'Agriculture Horticulture And Fisheries',
            'Agriculture, horticulture and fisheries'
        ),
        ('Automotive', 'Automotive'),
        (
            'Biotechnology And Pharmaceuticals',
            'Biotechnology and pharmaceuticals'
        ),
        ('Business And Consumer Services', 'Business and consumer services'),
        ('Chemicals', 'Chemicals'),
        ('Clothing Footwear And Fashion', 'Clothing, footwear and fashion'),
        ('Communications', 'Communications'),
        ('Construction', 'Construction'),
        ('Creative And Media', 'Creative and media'),
        ('Education And Training', 'Education and training'),
        ('Electronics And It Hardware', 'Electronics and IT hardware'),
        ('Environment', 'Environment'),
        (
            'Financial And Professional Services',
            'Financial and professional services'
        ),
        ('Food And Drink', 'Food and drink'),
        (
            'Giftware Jewellery And Tableware',
            'Giftware, jewellery and tableware'
        ),
        ('Global Sports Infrastructure', 'Global sports infrastructure'),
        ('Healthcare And Medical', 'Healthcare and medical'),
        (
            'Household Goods Furniture And Furnishings',
            'Household goods, furniture and furnishings'
        ),
        ('Life Sciences', 'Life sciences'),
        ('Leisure And Tourism', 'Leisure and tourism'),
        ('Legal Services', 'Legal services'),
        ('Marine', 'Marine'),
        (
            'Mechanical Electrical And Process Engineering',
            'Mechanical electrical and process engineering'
        ),
        ('Metallurgical Process Plant', 'Metallurgical process plant'),
        ('Metals Minerals And Materials', 'Metals, minerals and materials'),
        ('Mining', 'Mining'),
        ('Oil And Gas', 'Oil and gas'),
        ('Ports And Logistics', 'Ports and logistics'),
        ('Power', 'Power'), ('Railways', 'Railways'),
        ('Renewable Energy', 'Renewable energy'),
        ('Retail And Luxury', 'Retail and luxury'),
        ('Security', 'Security'),
        ('Software And Computer Services', 'Software and computer services'),
        (
            'Textiles Interior Textiles And Carpets',
            'Textiles, interior textiles and carpets'
        ),
        ('Water', 'Water'),
        ('Other', 'Other')
    ]
