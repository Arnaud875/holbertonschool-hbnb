#!/usr/bin/python3

"""
Places' API.
"""


from flask_restx import fields, Namespace, Resource
from app.services.facade import HBnBFacade


api = Namespace("places", description="Place operations")
facade = HBnBFacade.get_instance()

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner': fields.String(required=True, description='ID of the owner'),
    'amenities': fields.List(fields.String, required=False, description="List of amenities ID's")
})


@api.route("/")
class PlaceList(Resource):

    """
    Handle the place database
    """

    @api.expect(place_model, validate=True)
    @api.response(201, "Place successfully created")
    @api.response(400, "Invalid input data")
    @api.response(404, "Owner not found")
    def post(self):
        """
        POST a new place in database
        """

        place_data = api.payload
        owner_id = api.payload.get("owner", 0)

        owner = facade.get_user(owner_id)
        if not owner:
            return {'error': "Owner not found"}, 404

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": "Invalid input data"}

        owner.add_place(new_place)
        return {
            "id": new_place.id,
            "title": new_place.title,
            "description": new_place.description,
            "price": new_place.price,
            "latitude": new_place.latitude,
            "longitude": new_place.longitude,
            "owner": owner_id,
            "amenities": new_place.amenities
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

        owner = facade.get_user(place.owner)
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

    @api.expect(place_model)
    @api.response(200, "Place updated successfully")
    @api.response(400, "Invalid input data")
    def put(self, place_id):

        """
        PUT place details with their ID
        """

        obj = facade.get_place(place_id)
        if not obj:
            return {"error": "Place not found"}, 404

        try:
            facade.update_place(place_id, api.payload)
        except Exception as e:
            return {"error": "Invalid input data"}, 400
        return {"message": "Place updated successfully"}, 200

@api.route("/<place_id>/add_amenity/<amenity_id>")
class PlaceAmenity(Resource):
    @api.response(200, "Add amenity to place.")
    @api.response(404, "Place not found")
    @api.response(404, "Amenity not found")
    def post(self, place_id, amenity_id):
        """Associate an amenity to a place."""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Invalid place id"}

        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Invalid amenity id"}

        place.add_amenity(amenity)
        return {"message": "Add amenity to place"}, 200