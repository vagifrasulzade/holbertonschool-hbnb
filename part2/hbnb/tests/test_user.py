import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_create_user(self):
        """Test successful user creation"""
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.unique@example.com"
        }
        response = self.client.post('/api/v1/users/', json=user_data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

    def test_create_user_invalid_data(self):
        """Test user creation with missing/invalid fields"""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "Doe",
            "email": "not-an-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_get_all_users(self):
        """Test retrieving the list of users"""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        """Test retrieving a single user"""
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        user_id = create_response.get_json()['id']
        response = self.client.get(f'/api/v1/users/{user_id}')

        self.assertEqual(response.status_code, 200)
        # FIXED: Separated by comma
        self.assertEqual(response.json['first_name'], "Jane")

    def test_user_not_found(self):
        """Test retrieving a user that does not exist"""
        response = self.client.get('/api/v1/users/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user(self):
        """Test updating a user"""
        # Create user
        create_response = self.client.post('/api/v1/users/', json={
            "first_name": "Judy",
            "last_name": "Dove",
            "email": "judy.dove@example.com"
        })
        user_id = create_response.get_json()['id']

        # Update user
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "John",
            "last_name": "Dove",
            "email": "judy.dove@example.com"  # Some APIs require the email to remain consistent
        })

        # Added debug msg to see WHY it returns 400 if it fails
        self.assertEqual(response.status_code, 200, msg=f"Update failed: {response.data}")

        # Verify update
        verify_resp = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(verify_resp.json['first_name'], "John")


if __name__ == '__main__':
    unittest.main()