import os

import pytest
from fastapi.testclient import TestClient

from tests.assets import IMPORT_BATCHES, ROOT_ID
from tests.utils import request


@pytest.fixture(scope='session')
def test_client():
    os.environ[
        'DATABASE_URL'
    ] = 'postgresql://postgres:postgres@localhost:5432/'
    from app.main import app

    with TestClient(app) as client:
        yield client


@pytest.fixture(scope='session')
def client(test_client):
    client = test_client
    for index, batch in enumerate(IMPORT_BATCHES):
        print(f'Importing batch {index}')
        status, _ = request('/imports', method='POST', data=batch)

        assert status == 200, f'Expected HTTP status code 200, got {status}'

    yield client

    status, _ = request(f'/delete/{ROOT_ID}', method='DELETE')
    assert status == 200, f'Expected HTTP status code 200, got {status}'

    status, _ = request(f'/nodes/{ROOT_ID}', json_response=True)
    assert status == 404, f'Expected HTTP status code 404, got {status}'


@pytest.fixture(scope='session')
def root_category():
    return '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1'


@pytest.fixture(scope='session')
def sub_root_category():
    return '1cc0129a-2bfe-474c-9ee6-d435bf5fc8f2'


@pytest.fixture(scope='session')
def offer():
    return '73bc3b36-02d1-4245-ab35-3106c9ee1c65'
