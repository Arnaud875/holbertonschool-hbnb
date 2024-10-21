from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('reviews', description='Reviews operations')

# Define the reviews model for input validation and documentation
reviews_model = api.model('Reviews', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.String(required=True, description='Rating of the review'), # fields : int ?
    'place': fields.String(required=True, description='Place rated')
    'user': fields.String(required=True, description='User that write the review')
})

facade = HBnBFacade()
