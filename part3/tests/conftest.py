"""
Execute tests: pytest -s -v --disable-warnings

Support endpoint (/api/v1):
    ✔️ POST /users
    GET /users
    GET /users/<user_id>
    ✔️ PUT /users/<user_id>


    ✔️ POST /login
    GET /protected

    POST /amenities
    GET /amenities
    GET /amenities/<amenity_id>

    ✔️ POST /places
    GET /places
    GET /places/<place_id>
    ✔️ PUT /places/<place_id>
    POST /<place_id>/add_amenity/<amenity_id>

    ✔️ POST /reviews
    GET /reviews
    GET /reviews/<review_id>
    PUT /reviews/<review_id>
    DELETE /reviews/<review_id>
    GET /places/<place_id>/reviews
"""

import sys
import pytest
sys.path.append("..")

from app import create_app, db
from typing import Dict
from flask.testing import FlaskClient
from utils import AuthenticatedClient, SharedData

app = None

@pytest.fixture(scope="session")
def application():
    return app

@pytest.fixture(scope="session")
def client():
    global app
    app = create_app()

    with app.app_context():
        db.create_all()

    with app.test_client() as client:
        yield client

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="session")
def auth_client(client: FlaskClient, shared_data: SharedData) -> AuthenticatedClient:
    return AuthenticatedClient(client, shared_data.token)

@pytest.fixture(scope="session")
def shared_data():
    return SharedData()