from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from app import facade

api = Namespace('admin', description='Admin operations')

@api.route('/users/')
class AdminUserCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin', None):
            return {'error': 'Admin privileges required'}, 403

        user_data = request.json
        email = user_data.get('email')

        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, 400

        try:
            user_data["is_admin"] = True
            new_admin_user = facade.create_user(user_data)
        except ValueError as e:
            return {"error": "Invalid input data"}, 400

        return { "id": new_admin_user.id, "first_name": new_admin_user.first_name, "last_name": new_admin_user.last_name, "email": new_admin_user.email }, 201

@api.route('/users/<user_id>')
class AdminUserResource(Resource):
    @jwt_required()
    def put(self, user_id):
        current_user = get_jwt_identity()

        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.json
        email = data.get('email', None)

        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email is already in use'}, 400

        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404

        try:
            facade.update_user(user_id, api.payload)
        except Exception as e:
            return {"error": "Invalid input data"}, 400

        return { "id": user.id, "first_name": user.first_name, "last_name": user.last_name, "email": user.email }

@api.route('/amenities/')
class AdminAmenityCreate(Resource):
    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        amenity_data = api.payload

        try:
            new_amenity = facade.create_amenity(amenity_data)
        except Exception as e:
            return {"error": "Invalid input data"}, 400

        return { "id": new_amenity.id, "name": new_amenity.name }, 201

@api.route('/amenities/<amenity_id>')
class AdminAmenityModify(Resource):
    @jwt_required()
    def put(self, amenity_id):
        current_user = get_jwt_identity()
        if not current_user.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        obj = facade.get_amenity(amenity_id)
        if not obj:
            return {"error": "Amenity not found"}, 404

        try:
            facade.update_amenity(amenity_id, api.payload)
        except Exception as e:
            return {"error": "Invalid input data"}, 400

        return {"message": "Amenity updated successfully"}, 200