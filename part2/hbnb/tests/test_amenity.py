import unittest

from flask import request

from app import create_app


class TestAmenityEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_create_amenity(self):
        """Test successful amenity creation"""
        amenity_data = {
            "name": "WiFi"
        }
        # Just send the request to the client
        response = self.client.post('/api/v1/amenities/', json=amenity_data)

        # Check if the server did its job
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.get_json()['name'], "WiFi")

    def test_create_amenity_invalid_data(self):
        """Test amenity creation with missing/invalid fields"""
        response = self.client.post('/api/v1/amenities/', json={
            "name": "",
        })
        self.assertEqual(response.status_code, 400,
                         msg=f"Expected 400 but got {response.status_code}. Response: {response.data}")

    def test_get_all_amenities(self):
        """Test retrieving the list of amenities"""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_amenity_by_id(self):
        """Test retrieving a single amenity"""
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Pool",
        })
        amenity_id = create_response.get_json()['id']

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], amenity_id)  # Use two arguments

    def test_amenity_not_found(self):
        """Test retrieving an amenity that does not exist"""
        response = self.client.get('/api/v1/amenities/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_update_amenity(self):
        """Test updating an amenity"""
        create_response = self.client.post('/api/v1/amenities/', json={
            "name": "Gym",
        })
        amenity_id = create_response.get_json()['id']

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            "name": "New Gym Name",
        })

        self.assertEqual(response.status_code, 200)
        # FIX: Check the updated field, not the ID (IDs shouldn't change)
        self.assertEqual(response.json['name'], "New Gym Name")


if __name__ == '__main__':
    unittest.main()