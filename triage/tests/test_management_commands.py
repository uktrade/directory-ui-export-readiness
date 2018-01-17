from unittest.mock import ANY, mock_open, patch, call

from django.core.management import call_command


def stream_file_in_chucks(file_object):
    while True:
        data = file_object.read(4096)
        if not data:
            break
        yield data


@patch('triage.management.commands.update_top_importers.open', mock_open())
@patch('triage.management.commands.update_top_importers.csv.DictWriter')
@patch('triage.management.commands.update_top_importers.requests')
def test_update_top_importers_write_csv(
        mocked_requests,
        mocked_dictwriter,
):
    with open('triage/tests/comtrade_test.zip', 'rb') as test_file:
        mocked_requests.get.return_value.iter_content.return_value = \
            stream_file_in_chucks(test_file)
        call_command('update_top_importers', '--toptens')
        assert mocked_dictwriter.call_args == call(
            ANY,
            fieldnames=(
                'Partner',
                'Partner ISO',
                'Commodity Code',
                'Trade Value'
            )
        )
        assert mocked_dictwriter().writeheader.called is True
        data = mocked_dictwriter().writerows.call_args[0][0]
        expected_data = [{
            'Commodity Code': '01',
            'Partner': 'Antigua and Barbuda',
            'Partner ISO': 'ATG',
            'Reporter': 'United Kingdom',
            'Reporter ISO': 'GBR',
            'Trade Value': '2703'
        },
            {
                'Commodity Code': '01',
                'Partner': 'Azerbaijan',
                'Partner ISO': 'AZE',
                'Reporter': 'United Kingdom',
                'Reporter ISO': 'GBR',
                'Trade Value': '148262'
            },
            {
                'Commodity Code': '01',
                'Partner': 'Australia',
                'Partner ISO': 'AUS',
                'Reporter': 'United Kingdom',
                'Reporter ISO': 'GBR',
                'Trade Value': '25152614'
            }]
        assert list(data) == expected_data


@patch('triage.management.commands.update_top_importers.open', mock_open())
@patch('triage.management.commands.update_top_importers.csv.DictWriter')
@patch('triage.management.commands.update_top_importers.requests')
def test_update_totals_write_csv(
        mocked_requests,
        mocked_dictwriter,
):
    with open('triage/tests/comtrade_test.zip', 'rb') as test_file:
        mocked_requests.get.return_value.iter_content.return_value = \
            stream_file_in_chucks(test_file)
        call_command('update_top_importers', '--totals')
        assert mocked_dictwriter.call_args == call(
            ANY,
            fieldnames=(
                'Partner ISO',
                'Commodity Code',
                'Trade Value'
            )
        )
        assert mocked_dictwriter().writeheader.called is True
        data = mocked_dictwriter().writerows.call_args[0][0]
        expected_data = [{
                             'Commodity Code': '01', 'Partner ISO': 'ATG',
                             'Trade Value': 2703
                         },
                         {
                             'Commodity Code': '01', 'Partner ISO': 'AUS',
                             'Trade Value': 25153169
                         },
                         {
                             'Commodity Code': '01', 'Partner ISO': 'AZE',
                             'Trade Value': 148262
                         },
                         {
                             'Commodity Code': '21', 'Partner ISO': 'ITA',
                             'Trade Value': 455
                         }]
        assert list(data) == expected_data


@patch('triage.management.commands.update_top_importers.open', mock_open())
@patch('triage.management.commands.update_top_importers.csv.DictWriter')
@patch('triage.management.commands.update_top_importers.requests')
def test_update_totals_and_top_importers_write_csv(
        mocked_requests,
        mocked_dictwriter,
):
    with open('triage/tests/comtrade_test.zip', 'rb') as test_file:
        mocked_requests.get.return_value.iter_content.return_value = \
            stream_file_in_chucks(test_file)
        call_command('update_top_importers')
        # Because dictwriter is inside a with there's only knowledge of the
        # last file opened.
        # Previous tests are testing the two scenarios
        assert mocked_dictwriter.call_args == call(
            ANY,
            fieldnames=(
                'Partner ISO',
                'Commodity Code',
                'Trade Value'
            )
        )
