from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace("places", description="Place operations")

# ---------- Swagger models ----------
amenity_model = api.model("PlaceAmenity", {
    "id": fields.String(description="Amenity ID"),
    "name": fields.String(description="Name of the amenity"),
})

user_model = api.model("PlaceUser", {
    "id": fields.String(description="User ID"),
    "first_name": fields.String(description="First name of the owner"),
    "last_name": fields.String(description="Last name of the owner"),
    "email": fields.String(description="Email of the owner"),
})

review_model = api.model("PlaceReview", {
    "id": fields.String(description="Review ID"),
    "text": fields.String(description="Text of the review"),
    "rating": fields.Integer(description="Rating of the place (1-5)"),
    "user_id": fields.String(description="ID of the user"),
})

place_model = api.model("Place", {
    "title": fields.String(required=True, description="Title of the place"),
    "description": fields.String(description="Description of the place"),
    "price": fields.Float(required=True, description="Price per night"),
    "latitude": fields.Float(required=True, description="Latitude of the place"),
    "longitude": fields.Float(required=True, description="Longitude of the place"),

    # Your DB/model uses user_id
    "user_id": fields.String(required=False, description="Owner user ID"),

    "owner": fields.Nested(user_model, description="Owner of the place"),
    'amenities': fields.List(
        fields.Integer,
        description="List of amenity IDs"
    ),
    "reviews": fields.List(fields.Nested(review_model), description="List of reviews"),
})


@api.route("/")
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    def post(self):
        """Register a new place (auth required)"""
        current_user_id = get_jwt_identity()
        place_data = api.payload or {}

        # ✅ model expects user_id, so set it
        place_data["user_id"] = current_user_id

        # (optional) prevent client from overriding user_id
        # place_data.pop("user_id", None)  # <- don't do this, we need it
        try:
            new_place = facade.create_place(place_data)
            return new_place.to_dict(include_owner=True), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, "List of places retrieved successfully")
    def get(self):
        """Retrieve a list of all places"""
        places = facade.get_all_places() or []
        places_list = [p.to_dict() for p in places]
        return places_list, 200


@api.route("/<place_id>")
class PlaceResource(Resource):
    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """Get place details by ID"""
        p = facade.get_place(place_id)
        if not p:
            return {"error": "Place not found"}, 404

        return p.to_dict(include_owner=True, include_amenities=True, include_reviews=True), 200


    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(200, "Place updated successfully")
    @api.response(404, "Place not found")
    @api.response(400, "Invalid input data")
    @api.response(403, "Unauthorized action")
    def put(self, place_id):
        """
        Update a place:
        - owner can update own place
        - admin can update any place
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = bool(claims.get("is_admin", False))

        p = facade.get_place(place_id)
        if not p:
            return {"error": "Place not found"}, 404

        # ✅ ownership check uses user_id
        if not is_admin and str(p.user_id) != str(current_user_id):
            return {"error": "Unauthorized action"}, 403

        place_data = api.payload or {}

        # prevent changing ownership
        place_data.pop("user_id", None)
        place_data.pop("owner_id", None)

        try:
            updated_place = facade.update_place(place_id, place_data)
            if not updated_place:
                return {"error": "Place not found"}, 404
            return updated_place.to_dict(include_owner=True), 200
        except ValueError as e:
            return {"error": str(e)}, 400