import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Create a real User and Place once for use in all tests
        user_resp = self.client.post('/api/v1/users/', json={
            "first_name": "Alice", "last_name": "Reviewer", "email": "alice@test.com"
        })
        self.user_id = user_resp.get_json()['id']

        place_resp = self.client.post('/api/v1/places/', json={
            "title": "Test House", "description": "Nice", "price": 50.0,
            "latitude": 10.0, "longitude": 10.0, "owner_id": self.user_id
        })
        self.place_id = place_resp.get_json()['id']

    def tearDown(self):
        self.app_context.pop()

    def test_create_review(self):
        """Test successful review creation"""
        review_data = {
            "text": "Amazing stay!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        response = self.client.post('/api/v1/reviews/', json=review_data)
        self.assertEqual(response.status_code, 201)

    def test_get_review_by_id(self):
        """Test retrieving a single review"""
        # Use valid IDs from setUp
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Great!",
            "rating": 4,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # FIX: Correct URL formatting (no comma)
        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], review_id)

    def test_update_review(self):
        """Test updating a review"""
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Original text",
            "rating": 3,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Updated text",
            "rating": 5
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], "Review updated successfully")

    def test_review_not_found(self):
        """Test retrieving a review that does not exist"""
        response = self.client.get('/api/v1/reviews/invalid-id')
        self.assertEqual(response.status_code, 404)

    def test_delete_review(self):
        """Test successful deletion of a review"""
        # 1. Create a review to delete
        create_response = self.client.post('/api/v1/reviews/', json={
            "text": "Delete me",
            "rating": 1,
            "user_id": self.user_id,
            "place_id": self.place_id
        })
        review_id = create_response.get_json()['id']

        # 2. Delete the review
        delete_response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(delete_response.status_code, 200)

        # Optional: Check if your backend sends a success message
        self.assertIn('successfully', delete_response.get_json().get('message', ''))

        # 3. VERIFY: Try to GET the deleted review
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)




if __name__ == '__main__':
    unittest.main()