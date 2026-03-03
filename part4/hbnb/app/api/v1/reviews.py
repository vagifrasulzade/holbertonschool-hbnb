from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# ✅ Client sends ONLY text, rating, place_id
# user_id comes from JWT token (so no spoofing)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Place not found')
    @jwt_required()
    def post(self):
        """Register a new review"""
        current_user_id = str(get_jwt_identity())
        review_data = api.payload or {}

        # must exist
        place = facade.get_place(review_data.get('place_id'))
        if not place:
            return {'error': 'Place not found'}, 404

        if str(place.user_id) == current_user_id:
            return {'message': 'You cannot review your own place'}, 400

        all_reviews = facade.get_all_reviews()
        for r in all_reviews:
            if str(r.place_id) == str(review_data.get('place_id')) and str(r.user_id) == current_user_id:
                return {'error': 'You have already reviewed this place'}, 400

        # force user_id from token
        review_data['user_id'] = current_user_id

        try:
            new_review = facade.create_review(review_data)
            if not new_review:
                return {'error': 'Invalid User or Place ID'}, 400

            # return using ids directly (no need for relationship loading)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user_id,
                'place_id': new_review.place_id
            }, 201

        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': r.id,
                'text': r.text,
                'rating': r.rating,
                'user_id': r.user_id,
                'place_id': r.place_id
            }
            for r in reviews
        ], 200


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        r = facade.get_review(review_id)
        if not r:
            return {'message': 'Review not found'}, 404
        return {
            'id': r.id,
            'text': r.text,
            'rating': r.rating,
            'user_id': r.user_id,
            'place_id': r.place_id
        }, 200

    @api.expect(review_model)  # still only text/rating/place_id allowed from client
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """Update a review's information"""
        current_user_id = str(get_jwt_identity())
        r = facade.get_review(review_id)
        if not r:
            return {'message': 'Review not found'}, 404

        # only the author can edit
        if str(r.user_id) != current_user_id:
            return {'message': 'Unauthorized action'}, 400

        review_data = api.payload or {}

        # never allow changing ownership through payload
        review_data.pop('user_id', None)

        try:
            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404
            return {'message': 'Review updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete a review"""
        current_user_id = str(get_jwt_identity())
        r = facade.get_review(review_id)
        if not r:
            return {'message': 'Review not found'}, 404

        # only the author can delete
        if str(r.user_id) != current_user_id:
            return {'message': 'Unauthorized action'}, 400

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200