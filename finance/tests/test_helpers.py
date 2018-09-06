from finance import helpers


def test_flatten_form_data():
    actual = helpers.flatten_form_data({
        '1': ['1', '2', '3'],
        '2': '4',
    })
    assert sorted(actual) == [
        ('1', '1'),
        ('1', '2'),
        ('1', '3'),
        ('2', '4'),
    ]
