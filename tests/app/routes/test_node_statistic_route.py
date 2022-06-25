from tests.test_assets.statistic.expected_statistic_category_assets import (
    EXPECTED_STATISTIC_CATEGORY_DATE_END,
    EXPECTED_STATISTIC_CATEGORY_DATE_START,
    EXPECTED_STATISTIC_CATEGORY_DATE_START_DATE_END,
    EXPECTED_STATISTIC_CATEGORY_FULL_DATES,
)
from tests.test_assets.statistic.expected_statistic_offer_assets import (
    OFFER_STATISTIC_DATE_END,
    OFFER_STATISTIC_DATE_START,
    OFFER_STATISTIC_DATE_START_AND_DATE_END,
    OFFER_STATISTIC_FULL_DATES,
)


class TestStatisticRoute:
    date_start: str = '2022-02-04T15:00:00.000Z'
    date_end: str = '2022-02-06T15:00:00.000Z'

    def test_offer_statistic(self, client, offer):
        response = client.get(f'/node/{offer}/statistic')
        assert response.status_code == 200
        data = response.json()
        assert OFFER_STATISTIC_FULL_DATES == data

    def test_offer_statistic_with_date_start(self, client, offer):
        response = client.get(
            f'/node/{offer}/statistic?dateStart={self.date_start}'
        )
        assert response.status_code == 200
        data = response.json()
        assert OFFER_STATISTIC_DATE_START == data

    def test_offer_statistic_with_date_end(self, client, offer):
        response = client.get(
            f'/node/{offer}/statistic' f'?dateEnd={self.date_end}'
        )
        assert response.status_code == 200
        data = response.json()
        assert OFFER_STATISTIC_DATE_END == data

    def test_offer_statistic_with_date_start_date_end(self, client, offer):
        response = client.get(
            f'/node/{offer}/statistic'
            f'?dateStart={self.date_start}'
            f'&dateEnd={self.date_end}'
        )
        assert response.status_code == 200
        data = response.json()
        assert OFFER_STATISTIC_DATE_START_AND_DATE_END == data

    def test_category_statistic(self, client, root_category):
        response = client.get(f'/node/{root_category}/statistic')
        assert response.status_code == 200
        data = response.json()
        assert EXPECTED_STATISTIC_CATEGORY_FULL_DATES == data

    def test_category_statistic_with_date_start(self, client, root_category):
        response = client.get(
            f'/node/{root_category}/statistic?dateStart={self.date_start}'
        )
        assert response.status_code == 200
        data = response.json()
        assert EXPECTED_STATISTIC_CATEGORY_DATE_START == data

    def test_category_statistic_with_date_end(self, client, root_category):
        response = client.get(
            f'/node/{root_category}/statistic' f'?dateEnd={self.date_end}'
        )
        assert response.status_code == 200
        data = response.json()
        assert EXPECTED_STATISTIC_CATEGORY_DATE_END == data

    def test_category_statistic_with_date_start_date_end(
        self, client, root_category
    ):
        response = client.get(
            f'/node/{root_category}/statistic'
            f'?dateStart={self.date_start}'
            f'&dateEnd={self.date_end}'
        )
        assert response.status_code == 200
        data = response.json()
        assert EXPECTED_STATISTIC_CATEGORY_DATE_START_DATE_END == data

    def test_validation_error(self, client):
        for uuid in [1, 'abcd', '2345554', 'no-exists']:
            response = client.get(f'/node/{uuid}/statistic')
            assert response.status_code == 400
            assert response.json()['detail'] == 'Validation Failed'

    def test_unknown_id(self, client, offer, root_category, sub_root_category):
        for uuid in [offer, root_category, sub_root_category]:
            uuid = uuid[:-3] + '000'
            response = client.get(f'/node/{uuid}/statistic')
        assert response.status_code == 404
        assert response.json()['detail'] == 'Item not found'

    def test_bigger_date(self, client, offer, root_category, sub_root_category):
        for uuid in [offer, root_category, sub_root_category]:
            response = client.get(
                f'/node/{uuid}/statistic' f'?dateStart=2022-02-10T12:00:00.000Z'
            )
        assert response.status_code == 200
        assert response.json() == {'items': []}
