from flask import Flask
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import config

bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()
facade = None

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    from .services import HBnBFacade
    globals()["facade"] = HBnBFacade()

    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    import app.api.v1 as modules
    api.add_namespace(modules.admin_api, "/api/v1/admin")
    api.add_namespace(modules.users_api, path='/api/v1/users')
    api.add_namespace(modules.amenities_api, path="/api/v1/amenities")
    api.add_namespace(modules.reviews_api, path="/api/v1/reviews")
    api.add_namespace(modules.places_api, "/api/v1/places")
    api.add_namespace(modules.auth_api, "/api/v1/auth")
    return app