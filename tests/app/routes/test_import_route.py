class TestImportRoute:
    def test_validation_error(self, client):
        for data in [
            {
                'items': [
                    {
                        'type': 'OFFER',
                        'name': 'Товары',
                        'id': '069cb8d7-bbdd-47d3-ad8f-82ef4c269df1',
                        'parentId': None,
                    }
                ],
                'updateDate': '2022-02-10T12:00:00.000Z',
            },
            {
                'items': [
                    {
                        'type': 'OFFERS',
                        'name': 'jPhone 13',
                        'id': '863e1a7a-1304-42ae-943b-179184c077e3',
                        'parentId': 'd515e43f-f3f6-4471-bb77-6b455017a2d2',
                        'price': 79999,
                    },
                ],
                'updateDate': '2022-02-10T12:00:00.000Z',
            },
        ]:
            response = client.post('/imports', data=data)
            assert response.status_code == 400
            assert response.json()['detail'] == 'Validation Failed'
