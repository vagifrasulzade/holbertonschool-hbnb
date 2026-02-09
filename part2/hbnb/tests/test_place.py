import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # 1. Create a valid owner for all tests
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Owner",
            "last_name": "User",
            "email": "owner@hbnb.com",
        })
        self.owner_id = user_resp.get_json()['id']

    def tearDown(self):
        self.app_context.pop()

    def test_create_place(self):
        """Test successful place creation"""
        place_data = {
            "title": "Beautiful Villa",
            "description": "Luxurious stay",
            "price": 150.0,
            "latitude": 45.0,
            "longitude": 90.0,
            "owner_id": self.owner_id
        }
        response = self.client.post('/api/v1/places/', json=place_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_get_place_by_id(self):
        """Test retrieving a single place"""
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Apartment",
            "price": 50.0,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": self.owner_id
        })
        place_id = create_response.get_json()['id']

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], "Apartment")

    def test_update_place(self):
        """Test updating a place"""
        create_response = self.client.post('/api/v1/places/', json={
            "title": "Old Title",
            "price": 100.0,
            "latitude": 0.0,
            "longitude": 0.0,
            "owner_id": self.owner_id
        })
        place_id = create_response.get_json()['id']

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            "title": "New Title",
            "price": 120.0
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], "New Title")

    def test_place_not_found(self):
        """Test retrieving a place that does not exist"""
        response = self.client.get('/api/v1/places/invalid-id')
        self.assertEqual(response.status_code, 404)