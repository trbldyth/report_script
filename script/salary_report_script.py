import argparse
import pathlib
import json


def data_formation(path):
    data: dict[str, list] = {'id': [], 'email': [], 'name': [],
                             'department': [], 'hours_worked': [], 'rate': []}
    for file in path:
        with open(file, 'r') as check:
            if check.read() == '':
                print(f'{check.name} is empty!')
                if len(path) == 1:
                    break
                else:
                    continue
        f = open(file, 'r')
        first_string: str = next(f)[:-1]
        keys: list[str] = first_string.split(',')
        for line in f:
            values: list[str] = line[:-1].split(',')
            for i, key in enumerate(keys):
                try:
                    data[key].append(values[i])
                except Exception:
                    data['rate'].append(values[i])
        f.close()
    return data


def table_creation(data: dict[str, list], args) -> str:
    if args.result_path:
        open(args.result_path, 'w')
    if args.report == 'payout':
        headers: list[str] = ['Department', 'Name', 'Hours', 'Rate', 'Payout']
        separator: str = (f"+{'-' * 20}+{'-' * 25}+{'-' * 15}"
                          f"+{'-' * 7}+{'-' * 10}+")
    table: list[str] = []
    table.append(separator)
    table.append(f'| {headers[0].ljust(18)} |'
                 f' {headers[1].ljust(23)} |'
                 f' {headers[2].ljust(13)} |'
                 f' {headers[3].ljust(5)} |'
                 f' {headers[4].ljust(8)} |')
    table.append(separator)
    used: list[int] = []
    i: int = 0
    while i <= (len(data['id'])-1):
        if i not in used:
            dep_values: list[str] = data.get('department')
            total_hw: int = 0
            total_payout: int = 0
            dictionary: dict[str, dict] = {}
            for n, m in enumerate(dep_values):
                if m == data['department'][i]:
                    if data['department'][n] not in dictionary.keys():
                        dictionary: dict = {
                            data['department'][n]: []}
                    if args.report == 'payout':
                        payout: int = (int(data["rate"][n])
                                       * int(data["hours_worked"][n]))
                        table.append(f'| {str(data["department"][n]).ljust(18)} |'
                                     f' {str(data["name"][n]).ljust(23)} |'
                                     f' {str(data["hours_worked"][n]).ljust(13)} |'
                                     f' ${str(data["rate"][n]).ljust(4)} |'
                                     f' ${str(payout).ljust(8)}|')
                        total_hw += int(data["hours_worked"][n])
                        total_payout += payout
                        table.append(separator)
                        used.append(n)
                    if args.result_path:
                        dictionary[data['department'][n]].append({
                                str(headers[1]): str(data['name'][n]),
                                str(headers[2]):
                                str(data['hours_worked'][n]),
                                str(headers[3]): '$'+str(data['rate'][n]),
                                str(headers[4]): f'${str(payout)}'}
                        )
                    a: str = data['department'][n]
            if args.result_path:
                dictionary[a].append({'Total hours': str(total_hw),
                                      'Total payout': '$'+str(total_payout)})
                report_convert(dictionary, args)
            table.append(f'| {"Total".ljust(18)} |'
                         f' {"".ljust(23)} |'
                         f' {str(total_hw).ljust(13)}'
                         f' | {"".ljust(5)} | ${str(total_payout).ljust(8)}|')
            table.append(separator)
            if i != len(data['id'])-3:
                table.append(separator)
        i += 1
    return '\n'.join(table)


def report_convert(sample, args):
    result_file = open(args.result_path, 'a')
    file_format: str = str(args.result_path).split('.')[1]
    if file_format == 'json':
        json.dump(sample, result_file)
    else:
        print('This type of file not supported yet!')
    result_file.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path', nargs='*', type=pathlib.Path)
    parser.add_argument('--report', action='store')
    parser.add_argument('-rp', '--result_path', type=pathlib.Path)
    args = parser.parse_args()
    data = data_formation(args.path)
    print(table_creation(data, args))
