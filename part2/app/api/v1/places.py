#!/usr/bin/python3

"""
Places' API.
"""


from flask_restx import fields, Namespace, Resource
from app.services.facade import HBnBFacade


api = Namespace("places", description="Place operations")
facade = HBnBFacade.get_instance()
place_model = api.model("Place", {
    "title": fields.String(required=True, description="Place title"),
    "description": fields.String(required=True, description="Place desc."),
    "price": fields.Float(required=True, description="Place's rent price"),
    "latitude": fields.Float(required=True, description="Place latitude"),
    "longitude": fields.Float(required=True, description="Place longitude"),
    "owner": fields.Integer(required=True, description="Place owner"),
    "reviews": fields.List(required=False, description="Place's reviews"),
    "amenities": fields.List(required=False, description="Place's amenity")
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

        try:
            new_place = facade.create_place(place_data)
        except ValueError as e:
            return {"error": str(e)}

        owner = facade.get_user(new_place.owner)
        if not owner:
            return {'error': "Owner not found"}, 404

        return {
            "id": new_place.id,
            "title": new_place.title(),
            "description": new_place.description,
            "price": new_place.price(),
            "latitude": new_place.latitude(),
            "longitude": new_place.longitude(),
            "owner": owner,
            "reviews": new_place.reviews,
            "amenities": new_place.amenities
            }, 201


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
            "latitude": place.latitude(),
            "longitude": place.longitude(),
            "owner": owner,
            "reviews": place.reviews,
            "amenities": place.amenities
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
