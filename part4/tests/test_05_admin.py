"""
Testing admin endpoint
"""
from utils import *
from flask.testing import FlaskClient
from flask_jwt_extended import create_access_token

auth_admin: AuthenticatedClient = None
admin_id: int = None

admin_user_payload = {
    "first_name": "Admin",
    "last_name": "Admin",
    "email": "admin.admin@gmail.com",
    "password": "admin"
}

"""
Peut-on récupérer les infos des admins dans le GET de user ?
"""

class TestAdmin:
    def test_create_admin_user(self, client: FlaskClient, auth_client: AuthenticatedClient, shared_data: SharedData, application):
        assert shared_data.token != None
        check_response(auth_client.post("/api/v1/admin/users/", json={}), status_code=403, expected_payload=[{ "error": "Admin privileges required" }])

        with application.app_context():
            fake_admin_token = create_access_token(identity={"id": "???", "is_admin": True})

        global auth_admin
        auth_admin = AuthenticatedClient(client, fake_admin_token)

        result = check_response(
            auth_admin.post("/api/v1/admin/users/", json=admin_user_payload),
            status_code=201,
            template=shared_data.user_template(),
            expected_payload=dict_without_keys(admin_user_payload, ["password"]),
            exclude_payload=["password"]
        )

        global admin_id
        admin_id = result["id"]

        result = check_response(
            client.post("/api/v1/auth/login", json=dict_without_keys(admin_user_payload, ["first_name", "last_name"])),
            status_code=200,
            expected_payload=["access_token"]
        )

        auth_admin = AuthenticatedClient(client, result["access_token"])

    def test_admin_modify_user(self, client: FlaskClient, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert auth_admin != None
        check_response(auth_client.put(f"/api/v1/admin/users/{shared_data.user_id}", json={}), status_code=403, 
                       expected_payload=[{ "error": "Admin privileges required" }])

        shared_data.user_payload["email"] = "azerty@gmail.com"
        shared_data.user_payload["password"] = "why_are_you_gay"

        check_response(
            auth_admin.put(f"/api/v1/admin/users/{shared_data.user_id}", json=shared_data.user_payload),
            status_code=200,
            template=shared_data.user_template(),
            expected_payload=payload_to_array(
                dict_without_keys(shared_data.user_payload, ["password"])
            ),
            exclude_payload=["password"]
        )

        check_response(
            client.post("/api/v1/auth/login", json=dict_without_keys(shared_data.user_payload, ["first_name", "last_name"])),
            status_code=200,
            expected_payload=["access_token"]
        )

        check_response(
            auth_admin.get(f"/api/v1/users/{shared_data.user_id}"),
            status_code=200,
            template=shared_data.user_template(),
            expected_payload=payload_to_array(
                dict_without_keys(shared_data.user_payload, ["password"])
            )
        )

    def test_admin_create_amenity(self, client: FlaskClient, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert auth_admin != None
        check_response(auth_client.post("/api/v1/admin/amenities/", json={}), status_code=403, expected_payload=[{ "error": "Admin privileges required" }])

        new_amenity = shared_data.amenities_payload.copy()
        new_amenity["name"] = "Hello"

        result = check_response(
            auth_admin.post("/api/v1/admin/amenities/", json=new_amenity),
            status_code=201,
            template=shared_data.amenities_template(),
            expected_payload=payload_to_array(new_amenity),
            partial_match=True
        )

        shared_data.amenities.append({ "id": result["id"], "data": new_amenity })

    def test_admin_modify_amenity(self, client: FlaskClient, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert auth_admin != None
        current_amenity = shared_data.amenities[1]

        check_response(auth_client.put(f"/api/v1/admin/amenities/{current_amenity['id']}", json={}), status_code=403, 
                       expected_payload=[{ "error": "Admin privileges required" }])

        current_amenity["data"]["name"] = "YouAreMyFriend"

        check_response(
            auth_admin.put(f"/api/v1/admin/amenities/{current_amenity['id']}", json=current_amenity["data"]),
            status_code=200,
            expected_payload=[{ "message": "Amenity updated successfully" }]
        )

    def test_admin_modify_and_delete_reviews(self, auth_client: FlaskClient, shared_data: SharedData):
        assert auth_admin != None
        shared_data.review_payload["text"] = "Hello my friend !"

        check_response(
            auth_admin.put(f"/api/v1/reviews/{shared_data.review_id}", json=shared_data.review_payload),
            status_code=200,
            expected_payload=[{ "message": "Review updated successfully" }]
        )

        new_reviews = shared_data.review_payload.copy()
        new_reviews["text"] = "Je sais pas"
        new_reviews["user_id"] = shared_data.user_id

        result = auth_client.post(f"/api/v1/reviews/", json=new_reviews).get_json()
        check_response(
            auth_admin.delete(f"/api/v1/reviews/{result['id']}"),
            status_code=200,
            expected_payload=[{ "message": "Review deleted successfully" }]
        )

    def test_admin_modify_and_delete_place(self, auth_client: FlaskClient, shared_data: SharedData):
        assert auth_admin != None

        new_place = shared_data.place_payload.copy()
        new_place["title"] = "????????????"
        new_place["owner"] = shared_data.user_id

        place_result = auth_client.post("/api/v1/places/", json=new_place).get_json()

        new_reviews = shared_data.review_payload.copy()
        new_reviews["text"] = "Mouais"
        new_reviews["place_id"] = place_result["id"]

        r1 = auth_client.post(f"/api/v1/reviews/", json=new_reviews).get_json()["id"]
        new_reviews["text"] = "Mouais2"
        r2 = auth_client.post(f"/api/v1/reviews/", json=new_reviews).get_json()["id"]

        new_amenity = shared_data.amenities_payload.copy()
        new_amenity["name"] = "Yes Sir1"

        a1 = auth_client.post("/api/v1/amenities/", json=new_amenity).get_json()["id"]
        new_amenity["name"] = "Yes Sir2"
        a2 = auth_client.post("/api/v1/amenities/", json=new_amenity).get_json()["id"]

        auth_client.post(f"/api/v1/places/{place_result['id']}/add_amenity/{a1}")
        auth_client.post(f"/api/v1/places/{place_result['id']}/add_amenity/{a2}")

        check_response(
            auth_admin.put(f"/api/v1/places/{place_result['id']}", json={"title": ":((((()))))"}),
            status_code=200,
            expected_payload=[{"message": "Place updated successfully"}]
        )


        check_response(
            auth_admin.delete(f"/api/v1/places/{place_result['id']}"),
            status_code=200,
            expected_payload=[{"message": "Place deleted successfully"}]
        )

        check_response(
            auth_client.get(f"/api/v1/places/{place_result['id']}"),
            status_code=404,
            expected_payload=[{"error": "Place not found"}]
        )

        reviews = auth_client.get("/api/v1/reviews/").get_json()
        amenities = auth_client.get("/api/v1/amenities/").get_json()

        assert r1 not in reviews
        assert r2 not in reviews

        assert a1 not in amenities
        assert a2 not in amenities