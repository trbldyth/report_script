import pathlib
import argparse
from ..script.salary_report_script import (data_formation, table_creation,
                                           report_convert)


def test_salary_report():
    test_file = pathlib.Path('test_data.csv')
    args = argparse.Namespace(
        path=test_file, report='payout', result_path=None)
    with open(test_file.name, 'w') as f:
        f.write(
                'id,name,email,department,hours_worked,ratedata\n'
                '1,Alice Smith,aalice@example.com,HR,40,20\n'
                '2,Bob Johnson,bjohnson@example.com,Sales,35,25\n'
                '3,Eve Williams,ewilliams@example.com,Design,45,30\n'
                '4,Carol Harris,charris@example.com,HR,40,30\n'
                '5,John Hexlet,jhexlet@example.com,Design,30,60 ')
    result = data_formation([test_file])
    assert result == {
        'id': ['1', '2', '3', '4', '5'],
        'email': ['aalice@example.com', 'bjohnson@example.com',
                  'ewilliams@example.com', 'charris@example.com',
                  'jhexlet@example.com'],
        'name': ['Alice Smith', 'Bob Johnson',
                 'Eve Williams', 'Carol Harris', 'John Hexlet'],
        'department': ['HR', 'Sales', 'Design', 'HR', 'Design'],
        'hours_worked': ['40', '35', '45', '40', '30'],
        'rate': ['20', '25', '30', '30', '60']
    }
    output = table_creation(result, args)
    expected_output = ('+--------------------+-------------------------+------'
                       '---------+-------+----------+\n| Department         | '
                       'Name                    | Hours         | Rate  | Payo'
                       'ut   |\n+--------------------+------------------------'
                       '-+---------------+-------+----------+\n| HR           '
                       '      | Alice Smith             | 40            | $20 '
                       '  | $800     |\n+--------------------+----------------'
                       '---------+---------------+-------+----------+\n| HR   '
                       '              | Carol Harris            | 40          '
                       '  | $30   | $1200    |\n+--------------------+--------'
                       '-----------------+---------------+-------+----------+'
                       '\n| Total              |                         | 80 '
                       '           |       | $2000    |\n+--------------------'
                       '+-------------------------+---------------+-------+---'
                       '-------+\n+--------------------+----------------------'
                       '---+---------------+-------+----------+\n| Sales      '
                       '        | Bob Johnson             | 35            | $2'
                       '5   | $875     |\n+--------------------+--------------'
                       '-----------+---------------+-------+----------+\n| Tot'
                       'al              |                         | 35        '
                       '    |       | $875     |\n+--------------------+------'
                       '-------------------+---------------+-------+----------'
                       '+\n+--------------------+-------------------------+---'
                       '------------+-------+----------+\n| Design            '
                       ' | Eve Williams            | 45            | $30   | $'
                       '1350    |\n+--------------------+---------------------'
                       '----+---------------+-------+----------+\n| Design    '
                       '         | John Hexlet             | 30            | $'
                       '60   | $1800    |\n+--------------------+-------------'
                       '------------+---------------+-------+----------+\n| To'
                       'tal              |                         | 75       '
                       '     |       | $3150    |\n+--------------------+-----'
                       '--------------------+---------------+-------+---------'
                       '-+')

    assert output == expected_output
    test_file.unlink()


def test_empty_file():
    empty_file = pathlib.Path('test_empty.csv')
    empty_file.touch()
    result = data_formation([empty_file])
    assert result == {'id': [], 'email': [], 'name': [],
                      'department': [], 'hours_worked': [], 'rate': []}
    empty_file.unlink()


def test_report_convert():
    test_file = pathlib.Path('test_file.csv')
    args = argparse.Namespace(
        path=test_file, report='payout', result_path='test_file.json')
    sample = {"HR": [{"Name": "Alice Smith", "Hours": "40", "Rate":
                      "$20", "Payout": "$800"}, {"Name": "Carol Harris",
                                                 "Hours": "40", "Rate":
                                                 "$30", "Payout": "$1400"},
                     {"Total hours":
                      "80", "Total payout": "$2000"}]}
    sample_2nd = {"Design": [{"Name": "Eve Williams", "Hours": "45",
                              "Rate": "$30", "Payout": "$1350"},
                             {"Name": "John Hexlet", "Hours":
                              "30", "Rate": "60", "Payout": "1800"},
                             {"Total hours": "75",
                              "Total payout": "$3150"}]}
    open('test_file.json', 'w')
    report_convert(sample, args)
    report_convert(sample_2nd, args)
    with open('test_file.json', 'r') as f:
        assert f.read() == ('{"HR": [{"Name": "Alice Smith", "Hours": "40", '
                            '"Rate": "$20", "Payout": "$800"}, {"Name": "Car'
                            'ol Harris", "Hours": "40", "Rate": "$30", "Payo'
                            'ut": "$1400"}, {"Total hours": "80", "Total pay'
                            'out": "$2000"}]}{"Design": [{"Name": "Eve Willi'
                            'ams", "Hours": "45", "Rate": "$30", "Payout": "'
                            '$1350"}, {"Name": "John Hexlet", "Hours": "30",'
                            ' "Rate": "60", "Payout": "1800"}, {"Total hours'
                            '": "75", "Total payout": "$3150"}]}')
