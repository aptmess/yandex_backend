class TestDeleteRoute:
    def test_validation_error(self, client):
        for uuid in [1, 'abcd', '2345554', 'no-exists']:
            response = client.delete(f'/delete/{uuid}')
            assert response.status_code == 400
            assert response.json()['detail'] == 'Validation Failed'

    def test_unknown_id(self, client, offer, root_category, sub_root_category):
        for uuid in [offer, root_category, sub_root_category]:
            uuid = uuid[:-3] + '000'
            response = client.delete(f'/delete/{uuid}')
        assert response.status_code == 404
        assert response.json()['detail'] == 'Item not found'
