"""
Testing user endpoint
"""
from flask.testing import FlaskClient
from utils import *

class TestUsers:
    def test_create_user(self, client: FlaskClient, shared_data: SharedData):
        result = check_response(
            client.post("/api/v1/users/", json=shared_data.user_payload),
            status_code=201,
            template=shared_data.user_template(),
            expected_payload=payload_to_array(
                dict_without_keys(shared_data.user_payload, ["password"])
            ),
            exclude_payload=["password"]
        )

        shared_data.user_id = result["id"]

    def test_login_user(self, client: FlaskClient, shared_data: SharedData):
        result = check_response(
            client.post("/api/v1/auth/login", json=dict_without_keys(shared_data.user_payload, ["first_name", "last_name"])),
            status_code=200,
            expected_payload=["access_token"]
        )

        shared_data.token = result["access_token"]

    def test_get_info_user(self, client: FlaskClient, shared_data: SharedData):
        check_response(
            client.get(f"/api/v1/users/{shared_data.user_id}"),
            status_code=200,
            template=shared_data.user_template(),
            expected_payload=payload_to_array(
                dict_without_keys(shared_data.user_payload, ["password"])
            )
        )

    def test_get_all_users(self, client: FlaskClient, shared_data: SharedData):
        new_user = shared_data.user_payload.copy()
        new_user["first_name"] = "Pablo"
        new_user["last_name"] = "LeBest"
        new_user["email"] = "pablo.lebest@yessir.com"

        result = client.post("/api/v1/users/", json=new_user).get_json()
        shared_data.users.append({ "id": result["id"], "data": new_user })

        expected_users = [
            dict_without_keys(new_user, ["password"]),
            dict_without_keys(shared_data.user_payload, ["password"])
        ]

        check_response(
            client.get("/api/v1/users/"),
            status_code=200,
            array_payload=expected_users,
            array_template=shared_data.user_template()
        )


    def test_modify_user(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.token != None

        check_multiple_action(
            [
                { "email": "gsdfhgjsjghjdg" },
                { "password": "Jean" }
            ],
            auth_client.put,
            shared_data.user_payload,
            f"/api/v1/users/{shared_data.user_id}",
            400,
            {"error": "You cannot modify email or password"}
        )

        check_response(
            auth_client.put(f"/api/v1/users/{shared_data.user_id}", json={"first_name": "Jean"}),
            status_code=200,
            template=shared_data.user_template(),
            expected_payload=[{"first_name": "Jean"}],
            exclude_payload=["password"]
        )

        shared_data.user_payload["first_name"] = "Jean"