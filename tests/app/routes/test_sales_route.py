from tests.test_assets.expected_sales import (
    EXPECTED_SALE_BY_DATE
)


class TestSale:
    def test_sales(self, client):
        response = client.get(
            '/sales?date=2022-02-06T21:12:01.000Z',
        )
        assert response.status_code == 200
        data = response.json()
        assert EXPECTED_SALE_BY_DATE == data

    def test_date_validation_error(self, client):
        for date in ['02-02-2012', '2012-02-02', 'a']:
            response = client.get(
                f'/sales?date={date}'
            )
            assert response.status_code == 400
            assert response.json()['detail'] == 'Validation Failed'

    def test_null_result(self, client):
        response = client.get(
            '/sales?date=2022-02-10T21:12:01.000Z',
        )
        assert response.status_code == 200
        data = response.json()
        assert data is None
