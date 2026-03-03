from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from app.models import amenity
from app.models.amenity import Amenity
from app.services import facade

api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """
        Admin only: POST /api/v1/amenities/
        """
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        name = (amenity_data.get('name') or '').strip()

        if not name:
            return {"error": "Name is required"}, 400

            # If duplicates are handled in facade, this may raise ValueError
        try:
            new_amenity = facade.create_amenity({"name": name})
            return {'id': new_amenity.id, 'name': new_amenity.name}, 201
        except ValueError as e:
            return {'error': str(e)}, 400


    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        amenities_list = [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200
        return amenities_list

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if amenity:
            return {'id': amenity.id, 'name': amenity.name}
        return {'error': 'Amenity not found'}, 404

    @jwt_required()
    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        """
        Admin only: PUT /api/v1/amenities/<amenity_id>
        """
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload
        name = (amenity_data.get('name') or '').strip()
        if not name:
            return {"error": "Name is required"}, 400

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, 404
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


