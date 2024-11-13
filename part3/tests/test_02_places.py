"""
Testing place endpoint
"""
from utils import *

class TestPlaces:
    def test_create_place(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.token != None
        shared_data.place_payload["owner"] = shared_data.user_id

        check_multiple_action([
            { "owner": "test", "status": 403, "excepted_payload": { "error": "Unauthorized action." } },
            { "price": -1 },
            { "latitude": -180 },
            { "longitude": 2000 }
        ], auth_client.post, shared_data.place_payload, "/api/v1/places/", 400, {"error": "Invalid input data"})

        result = check_response(
            auth_client.post("/api/v1/places/", json=shared_data.place_payload),
            status_code=201,
            template=shared_data.place_template(),
            expected_payload=payload_to_array(shared_data.place_payload),
            partial_match=True
        )

        shared_data.place_id = result["id"]

    def test_update_place(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        check_multiple_action([
            { "owner": "test", "status": 403, "excepted_payload": { "error": "Unauthorized action." } },
            { "price": -1 },
            { "latitude": -180 },
            { "longitude": 2000 }
        ], auth_client.post, shared_data.place_payload, "/api/v1/places/", 400, {"error": "Invalid input data"})

        check_response(
            auth_client.put(f"/api/v1/places/{shared_data.place_id}", json={"title": "My super place"}),
            status_code=200,
            expected_payload=[{"message": "Place updated successfully"}]
        )

        shared_data.place_payload["title"] = "My super place"

    def test_get_info_place(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        check_response(
            auth_client.get(f"/api/v1/places/{shared_data.place_id}"),
            status_code=200,
            template=shared_data.place_template() + ["id", "reviews", "amenities"],
            expected_payload=payload_to_array(shared_data.get_place_data())
        )

    def test_get_all_places(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        check_response(
            auth_client.get("/api/v1/places/"),
            status_code=200,
            array_template=array_without_value(shared_data.place_template(), ["price", "owner", "description"]),
            array_payload=[
                dict_without_keys(shared_data.place_payload, ["price", "owner", "description"])
            ],
            partial_match=True
        )