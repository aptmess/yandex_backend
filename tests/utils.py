# encoding=utf8

import json
import re
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from tests.assets import API_BASEURL, IMPORT_BATCHES, ROOT_ID
from tests.test_assets.expected_tree_assets import EXPECTED_TREE_ROOT


def request(path, method='GET', data=None, json_response=False):
    try:
        params = {
            'url': f'{API_BASEURL}{path}',
            'method': method,
            'headers': {},
        }

        if data:
            params['data'] = json.dumps(data, ensure_ascii=False).encode(
                'utf-8'
            )
            params['headers']['Content-Length'] = len(params['data'])
            params['headers']['Content-Type'] = 'application/json'

        req = urllib.request.Request(**params)

        with urllib.request.urlopen(req) as res:
            res_data = res.read().decode('utf-8')
            if json_response:
                res_data = json.loads(res_data)
            return res.getcode(), res_data
    except urllib.error.HTTPError as e:
        return e.getcode(), None


def deep_sort_children(node):
    if node.get('children'):
        node['children'].sort(key=lambda x: x['id'])

        for child in node['children']:
            deep_sort_children(child)


def print_diff(expected, response):
    with open('expected.json', 'w') as f:
        json.dump(expected, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write('\n')

    with open('response.json', 'w') as f:
        json.dump(response, f, indent=2, ensure_ascii=False, sort_keys=True)
        f.write('\n')

    subprocess.run(
        [
            'git',
            '--no-pager',
            'diff',
            '--no-index',
            'expected.json',
            'response.json',
        ]
    )


def test_import():
    for index, batch in enumerate(IMPORT_BATCHES):
        print(f'Importing batch {index}')
        status, _ = request('/imports', method='POST', data=batch)

        assert status == 200, f'Expected HTTP status code 200, got {status}'

    print('Test import passed.')


def test_nodes():
    status, response = request(f'/nodes/{ROOT_ID}', json_response=True)
    # print(json.dumps(response, indent=2, ensure_ascii=False))

    assert status == 200, f'Expected HTTP status code 200, got {status}'

    deep_sort_children(response)
    deep_sort_children(EXPECTED_TREE_ROOT)
    if response != EXPECTED_TREE_ROOT:
        print_diff(EXPECTED_TREE_ROOT, response)
        print("Response tree doesn't match expected tree.")
        sys.exit(1)

    print('Test nodes passed.')


def test_sales():
    params = urllib.parse.urlencode({'date': '2022-02-04T00:00:00.000Z'})
    status, response = request(f'/sales?{params}', json_response=True)
    assert status == 200, f'Expected HTTP status code 200, got {status}'
    print('Test sales passed.')


def test_stats():
    params = urllib.parse.urlencode(
        {
            'dateStart': '2022-02-01T00:00:00.000Z',
            'dateEnd': '2022-02-03T00:00:00.000Z',
        }
    )
    status, response = request(
        f'/node/{ROOT_ID}/statistic?{params}', json_response=True
    )

    assert status == 200, f'Expected HTTP status code 200, got {status}'
    print('Test stats passed.')


def test_delete():
    status, _ = request(f'/delete/{ROOT_ID}', method='DELETE')
    assert status == 200, f'Expected HTTP status code 200, got {status}'

    status, _ = request(f'/nodes/{ROOT_ID}', json_response=True)
    assert status == 404, f'Expected HTTP status code 404, got {status}'

    print('Test delete passed.')


def test_all():
    test_import()
    test_nodes()
    test_sales()
    test_stats()
    test_delete()


def main():
    global API_BASEURL
    test_name = None

    for arg in sys.argv[1:]:
        if re.match(r'^https?://', arg):
            API_BASEURL = arg
        elif test_name is None:
            test_name = arg

    if API_BASEURL.endswith('/'):
        API_BASEURL = API_BASEURL[:-1]

    if test_name is None:
        test_all()
    else:
        test_func = globals().get(f'test_{test_name}')
        if not test_func:
            print(f'Unknown test: {test_name}')
            sys.exit(1)
        test_func()


if __name__ == '__main__':
    main()
