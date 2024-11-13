#!/usr/bin/python3
"""
Places' API.
"""

from flask_restx import fields, Namespace, Resource
from flask_jwt_extended import get_jwt_identity, jwt_required
from app import facade

api = Namespace("places", description="Place operations")

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.String(required=True, description='ID of the owner')
})


@api.route("/")
class PlaceList(Resource):

    """
    Handle the place database
    """

    @jwt_required()
    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner not found")
    def post(self):
        """
        POST a new place in database
        """

        current_user = get_jwt_identity()
        place_data = api.payload
        owner_id = place_data.get("owner", 0)

        if current_user["id"] != owner_id:
            return {"error": "Unauthorized action."}, 403

        owner = facade.get_user(current_user["id"])
        if not owner:
            return {'error': "Owner not found"}, 404

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": "Invalid input data"}, 400

        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner": current_user["id"]
        }, 201

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
        return [{
            "id": i.id,
            "title": i.title,
            "latitude": i.latitude,
            "longitude": i.longitude,
        } for i in facade.get_all_places()], 200

@api.route("/<place_id>")
class PlaceResource(Resource):

    """
    Display data of place
    """

    @api.response(200, "Place details retrieved successfully")
    @api.response(404, "Place not found")
    def get(self, place_id):
        """
        GET place details from their ID
        """
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner = facade.get_user(place.owner_id)
        if not owner:
            return {'error': "Owner not found"}, 404

        return {
            "id": place.id,
            "title": place.title,
            "description": place.description,
            "price": place.price,
            "latitude": place.latitude,
            "longitude": place.longitude,
            "owner": {
                "id": owner.id,
                "first_name": owner.first_name,
                "last_name": owner.last_name,
                "email": owner.email
            },
            "reviews": [{"id": review.id, "text": review.text, "rating": review.rating, "user_id": review.user_id} for review in place.reviews],
            "amenities": [{ "id": i.id, "name": i.name } for i in place.amenities]
        }, 200

    @jwt_required()
    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    def put(self, place_id):

        """
        PUT place details with their ID
        """

        current_user = get_jwt_identity()

        obj = facade.get_place(place_id)
        if not obj:
            return {"error": "Place not found"}, 404

        if not current_user["is_admin"]:
            if current_user["id"] != obj.owner_id:
                return {"error": "Unauthorized action."}, 403

        try:
            facade.update_place(place_id, api.payload)
        except Exception as e:
            return {"error": "Invalid input data"}, 400
        return {"message": "Place updated successfully"}, 200

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a review"""
        current_user = get_jwt_identity()

        obj = facade.get_place(place_id)
        if not obj:
            return {"error": "Place not found"}, 404

        if not current_user["is_admin"]:
            if current_user["id"] != obj.owner:
                return {"error": "Unauthorized action"}, 403

        for review in obj.reviews:
            facade.delete_review(review.id)

        for amenity in obj.amenities:
            facade.delete_amenity(amenity.id)

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200

@api.route("/<place_id>/add_amenity/<amenity_id>")
class PlaceAmenity(Resource):
    @jwt_required()
    @api.response(200, "Add amenity to place.")
    @api.response(404, "Place not found")
    @api.response(404, "Amenity not found")
    def post(self, place_id, amenity_id):
        """Associate an amenity to a place."""
        current_user = get_jwt_identity()

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Invalid place id"}

        if current_user["id"] != place.owner_id:
            return { "error": "Unauthorized action." }, 403

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Invalid amenity id"}

        place.amenities.append(amenity)
        return {"message": "Add amenity to place"}, 200