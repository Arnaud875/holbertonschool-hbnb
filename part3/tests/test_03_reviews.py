"""
Testing Reviews endpoint
"""
from utils import *

class TestReviews:
    def test_create_reviews(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None
        shared_data.review_payload["place_id"] = shared_data.place_id
        shared_data.review_payload["user_id"] = shared_data.user_id

        check_multiple_action([
            { "place_id": None, "status": 404, "excepted_payload": { "error": "Invalid place id" } },
            { "user_id": None, "status": 403, "excepted_payload": { "error": "Unauthorized action" } },
            { "user_id": shared_data.users[0]["id"], "status": 403, "excepted_payload": { "error": "Unauthorized action" } },
            { "rating": -1 }
        ], auth_client.post, shared_data.review_payload, "/api/v1/reviews/", 400, { "error": "Invalid input data" })

        result = check_response(
            auth_client.post("/api/v1/reviews/", json=shared_data.review_payload),
            status_code=201,
            template=shared_data.reviews_template(),
            expected_payload=payload_to_array(shared_data.review_payload),
            partial_match=True
        )

        shared_data.review_id = result["id"]

    def test_get_info_review(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        check_response(
            auth_client.get(f"/api/v1/reviews/{shared_data.review_id}"),
            status_code=200,
            expected_payload=payload_to_array(
                dict_without_keys(shared_data.review_payload, ["user_id", "place_id"])
            )
        )

    def test_get_all_reviews(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        new_reviews = shared_data.review_payload.copy()
        new_reviews["text"] = "Hello, my friend !"
        new_reviews["rating"] = 3

        result = auth_client.post("/api/v1/reviews/", json=new_reviews).get_json()
        shared_data.reviews.append({ "id": result["id"], "data": new_reviews })

        check_response(
            auth_client.get("/api/v1/reviews/"),
            status_code=200,
            array_template=array_without_value(shared_data.reviews_template(), ["user_id", "place_id"]),
            array_payload=[
                dict_without_keys(shared_data.review_payload, ["user_id", "place_id"]),
                dict_without_keys(new_reviews, ["user_id", "place_id"])
            ],
            partial_match=True
        )

    def test_get_reviews_from_place(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        # Ah c'est pas beau
        r = dict_without_keys(shared_data.review_payload, ["place_id"])
        r["id"] = shared_data.review_id

        check_response(
            auth_client.get(f"/api/v1/reviews/places/{shared_data.place_id}"), # Big flemme de modifier le endpoint
            status_code=200,
            array_template=array_without_value(shared_data.reviews_template(), ["place_id"]) + ["id"],
            array_payload=[r, dict_without_keys(shared_data.reviews[0]["data"], ["place_id"])]
        )

    def test_modify_review(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None
        shared_data.review_payload["text"] = "Why are you gay?"

        check_response(auth_client.put(f"/api/v1/reviews/1234", json={}), status_code=404)
        check_response(
            auth_client.put(f"/api/v1/reviews/{shared_data.review_id}", json=shared_data.review_payload),
            status_code=200,
            expected_payload=[{"message": "Review updated successfully"}]
        )

        r = dict_without_keys(shared_data.review_payload, ["place_id"])
        r["id"] = shared_data.review_id

        check_response(
            auth_client.get(f"/api/v1/reviews/places/{shared_data.place_id}"),
            status_code=200,
            array_template=array_without_value(shared_data.reviews_template(), ["place_id"]) + ["id"],
            array_payload=[r, dict_without_keys(shared_data.reviews[0]["data"], ["place_id"])]
        )

    def test_delete_review(self, auth_client: AuthenticatedClient, shared_data: SharedData):
        assert shared_data.place_id != None

        check_response(
            auth_client.delete(f"/api/v1/reviews/{shared_data.reviews[0]['id']}"),
            status_code=200,
            expected_payload=[{ "message": "Review deleted successfully" }]
        )

        shared_data.reviews.pop(0)

        r = dict_without_keys(shared_data.review_payload, ["place_id"])
        r["id"] = shared_data.review_id

        check_response(
            auth_client.get(f"/api/v1/reviews/places/{shared_data.place_id}"),
            status_code=200,
            array_template=array_without_value(shared_data.reviews_template(), ["place_id"]) + ["id"],
            array_payload=[r]
        )