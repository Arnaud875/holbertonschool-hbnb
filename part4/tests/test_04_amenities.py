"""
Testing amenities endpoint
"""
from utils import *

class TestAmenities:
    def test_create_amenity(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        result = check_response(
            auth_client.post("/api/v1/amenities/", json=shared_data.amenities_payload),
            status_code=201,
            template=shared_data.amenities_template(),
            expected_payload=payload_to_array(shared_data.amenities_payload),
            partial_match=True
        )

        shared_data.amenity_id = result["id"]

    def test_get_amenity(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.amenity_id != None

        check_response(
            auth_client.get(f"/api/v1/amenities/{shared_data.amenity_id}"),
            status_code=200,
            template=shared_data.amenities_template(),
            expected_payload=shared_data.amenities_payload,
            partial_match=True
        )

    def test_get_all_amenities(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.amenity_id != None

        new_amenity = shared_data.amenities_payload.copy()
        new_amenity["name"] = "YesSir!"

        r = auth_client.post("/api/v1/amenities/", json=new_amenity).get_json()
        shared_data.amenities.append({ "id": r["id"], "data": new_amenity })

        check_response(
            auth_client.get("/api/v1/amenities/"),
            status_code=200,
            array_template=shared_data.amenities_template(),
            array_payload=[shared_data.amenities_payload, new_amenity],
            partial_match=True
        )

    def test_modify_amenity(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.amenity_id != None

        shared_data.amenities_payload["name"] = "YouAreMyFriend"

        check_response(
            auth_client.put(f"/api/v1/amenities/{shared_data.amenity_id}", json=shared_data.amenities_payload),
            status_code=200,
            expected_payload=[{ "message": "Amenity updated successfully" }]
        )

        check_response(
            auth_client.get(f"/api/v1/amenities/{shared_data.amenity_id}"),
            status_code=200,
            template=shared_data.amenities_template(),
            expected_payload=shared_data.amenities_payload,
            partial_match=True
        )

    def test_add_amenity_to_place(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.amenity_id != None

        check_response(
            auth_client.post(f"/api/v1/places/{shared_data.place_id}/add_amenity/{shared_data.amenity_id}"),
            status_code=200,
            expected_payload=[{ "message": "Add amenity to place" }]
        )