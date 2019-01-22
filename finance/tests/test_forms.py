from finance import forms


def test_company_detail_form_has_company_number():
    form = forms.CompanyDetailsForm(data={
        'trading_name': 'test',
        'company_number': 'test',
        'address_line_one': 'test',
        'address_line_two': 'test',
        'address_town_city': 'test',
        'address_county': 'test',
        'address_post_code': 'test',
        'industry': 'Other',
        'industry_other': 'test',
        'export_status': 'I have customers outside the UK',
    })

    assert form.is_valid() is False
    assert form.cleaned_data['not_companies_house'] is False


def test_company_detail_form_no_company_number():
    form = forms.CompanyDetailsForm(data={
        'trading_name': 'test',
        'address_line_one': 'test',
        'address_line_two': 'test',
        'address_town_city': 'test',
        'address_county': 'test',
        'address_post_code': 'test',
        'industry': 'Other',
        'industry_other': 'test',
        'export_status': 'I have customers outside the UK',
    })

    assert form.is_valid() is False
    assert form.cleaned_data['not_companies_house'] is True


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
