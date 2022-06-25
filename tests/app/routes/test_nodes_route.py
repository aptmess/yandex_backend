from tests.test_assets.expected_tree_assets import (
    EXPECTED_OFFER,
    EXPECTED_SUB_ROOT_TREE,
    EXPECTED_TREE_ROOT,
)
from tests.utils import deep_sort_children


class TestNodesRoute:
    def test_category_tree(self, client, root_category):
        response = client.get(
            f'/nodes/{root_category}',
        )
        assert response.status_code == 200
        data = response.json()
        deep_sort_children(data)
        deep_sort_children(EXPECTED_TREE_ROOT)
        assert EXPECTED_TREE_ROOT == data

    def test_subcategory_root(self, client, sub_root_category):
        response = client.get(
            f'/nodes/{sub_root_category}',
        )
        assert response.status_code == 200
        data = response.json()
        deep_sort_children(data)
        deep_sort_children(EXPECTED_SUB_ROOT_TREE)
        assert EXPECTED_SUB_ROOT_TREE == data

    def test_offer(self, client, offer):
        response = client.get(
            f'/nodes/{offer}',
        )
        assert response.status_code == 200
        data = response.json()
        assert EXPECTED_OFFER == data

    def test_validation_error(self, client):
        for uuid in [1, 'abcd', '2345554', 'no-exists']:
            response = client.get(
                f'/nodes/{uuid}',
            )
            assert response.status_code == 400
            assert response.json()['detail'] == 'Validation Failed'

    def test_unknown_id(self, client, offer, root_category, sub_root_category):
        for uuid in [offer, root_category, sub_root_category]:
            uuid = uuid[:-3] + '000'
            response = client.get(
                f'/nodes/{uuid}',
            )
        assert response.status_code == 404
        assert response.json()['detail'] == 'Item not found'
