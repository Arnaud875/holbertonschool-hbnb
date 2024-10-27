import unittest
from unittest.mock import patch, Mock
import requests

unittest.TestLoader.sortTestMethodsUsing = None
"""
Addr: http://localhost:5000/api/v1

User:
POST /api/v1/users/
Content-Type: application/json
{"first_name": "John","last_name": "Doe","email": "john.doe@example.com"}

Expected Response:
{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","first_name": "John","last_name": "Doe","email": "john.doe@example.com"}
201 Created: When the user is successfully created.
400 Bad Request: If the email is already registered or input data is invalid.

GET /api/v1/users/<user_id>
Content-Type: application/json

Expected Response:
{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","first_name": "John","last_name": "Doe","email": "john.doe@x.com"}
200 OK: When the user is successfully retrieved.
404 Not Found: If the user does not exist.

GET /api/v1/users/
Content-Type: application/json

Expected Response:
[{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","first_name": "John","last_name": "Doe","email": "john.doe@example.com"},]
200 OK: When the list of users is successfully retrieved.

PUT /api/v1/users/<user_id>
Content-Type: application/json
{"first_name": "Jane","last_name": "Doe","email": "jane.doe@example.com"}

Expected Response:
{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","first_name": "Jane","last_name": "Doe","email": "jane.doe@example.com"}
200 OK: When the user is successfully updated.
404 Not Found: If the user does not exist.
400 Bad Request: If input data is invalid.

Amenities:
POST /api/v1/amenities/
Content-Type: application/json
{"name": "Wi-Fi"}

Expected Response:
{"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6","name": "Wi-Fi"}
201 Created: When the amenity is successfully created.
400 Bad Request: If input data is invalid.

GET /api/v1/amenities/
Content-Type: application/json

Expected Response:
[{"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6","name": "Wi-Fi"},{"id": "2fa85f64-5717-4562-b3fc-2c963f66afa6","name": "Air Conditioning"}]
200 OK: List of amenities retrieved successfully.

GET /api/v1/amenities/<amenity_id>
Content-Type: application/json

Expected Response:
{"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6","name": "Wi-Fi"}
200 OK: When the amenity is successfully retrieved.
404 Not Found: If the amenity does not exist.

PUT /api/v1/amenities/<amenity_id>
Content-Type: application/json
{"name": "Air Conditioning"}

Expected Response:
{"message": "Amenity updated successfully"}
200 OK: When the amenity is successfully updated.
404 Not Found: If the amenity does not exist.
400 Bad Request: If input data is invalid.

Places:

POST /api/v1/places/
Content-Type: application/json
{"title": "Cozy Apartment","description": "A nice place to stay","price": 100.0,"latitude": 37.7749,"longitude": -122.4194,"owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}

Expected Response:
{"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6","title": "Cozy Apartment","description": "A nice place to stay","price": 100.0,"latitude": 37.7749,"longitude": -122.4194,"owner_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6"}
201 Created: When the place is successfully created.
400 Bad Request: If input data is invalid.

GET /api/v1/places/
Content-Type: application/json

Expected Response:
[{"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6","title": "Cozy Apartment","latitude": 37.7749,"longitude": -122.4194},]
200 OK: List of places retrieved successfully.

GET /api/v1/places/<place_id>
Content-Type: application/json

Expected Response:
{"id": "1fa85f64-5717-4562-b3fc-2c963f66afa6","title": "Cozy Apartment","description": "A nice place to stay","latitude": 37.7749,"longitude": -122.4194,
"owner": {"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","first_name": "John","last_name": "Doe","email": "john.doe@example.com"},
"amenities": [{"id": "4fa85f64-5717-4562-b3fc-2c963f66afa6","name": "Wi-Fi"},{"id": "5fa85f64-5717-4562-b3fc-2c963f66afa6","name": "Air Conditioning"}]}
200 OK: When the place and its associated owner and amenities are successfully retrieved.
404 Not Found: If the place does not exist.

PUT /api/v1/places/<place_id>
Content-Type: application/json
{"title": "Luxury Condo","description": "An upscale place to stay","price": 200.0}

Expected Response:
{"message": "Place updated successfully"}
200 OK: When the place is successfully updated.
404 Not Found: If the place does not exist.
400 Bad Request: If input data is invalid.

Reviews:

POST /api/v1/reviews/
Content-Type: application/json
{"text": "Great place to stay!","rating": 5,"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"}

Expected Response:
{"id": "2fa85f64-5717-4562-b3fc-2c963f66afa6","text": "Great place to stay!","rating": 5,"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"}
201 Created: When the review is successfully created.
400 Bad Request: If input data is invalid.

GET /api/v1/reviews/
Expected Response:
[{"id": "2fa85f64-5717-4562-b3fc-2c963f66afa6","text": "Great place to stay!","rating": 5},]
200 OK: List of reviews retrieved successfully.

GET /api/v1/reviews/<review_id>
Expected Response:
{"id": "2fa85f64-5717-4562-b3fc-2c963f66afa6","text": "Great place to stay!","rating": 5,"user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"}
200 OK: When the review is successfully retrieved.
404 Not Found: If the review does not exist.


PUT /api/v1/reviews/<review_id>
Content-Type: application/json
{"text": "Amazing stay!","rating": 4}

Expected Response:
{"message": "Review updated successfully"}
200 OK: When the review is successfully updated.
404 Not Found: If the review does not exist.
400 Bad Request: If input data is invalid.


DELETE /api/v1/reviews/<review_id>
Expected Response:
{"message": "Review deleted successfully"}
200 OK: When the review is successfully deleted.
404 Not Found: If the review does not exist.

GET /api/v1/places/<place_id>/reviews
Expected Response:
[{"id": "2fa85f64-5717-4562-b3fc-2c963f66afa6","text": "Great place to stay!","rating": 5},{"id": "3fa85f64-5717-4562-b3fc-2c963f66afa6","text": "Very comfortable and clean.","rating": 4}]
200 OK: List of reviews for the place retrieved successfully.
404 Not Found: If the place does not exist.

"""

import unittest
import requests

BASE_URL_USERS = "http://localhost:5000/api/v1/users/"
BASE_URL_AMENITIES = "http://localhost:5000/api/v1/amenities/"
BASE_URL_PLACES = "http://localhost:5000/api/v1/places/"
BASE_URL_REVIEWS = "http://localhost:5000/api/v1/reviews/"

user_id = None
amenities_id = None
place_id = None
review_id = None

class Test_1_UserAPI(unittest.TestCase):

    def setUp(self):
        # Called before each test, can be used to initialize any data or state.
        self.test_user = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        }
        self.headers = {"Content-Type": "application/json"}
        self.user_id = None

    def test_1_create_user_success(self):
        response = requests.post(BASE_URL_USERS, json=self.test_user, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], self.test_user["first_name"])
        self.assertEqual(data["last_name"], self.test_user["last_name"])
        self.assertEqual(data["email"], self.test_user["email"])

        global user_id
        user_id = data["id"]

    def test_2_create_user_duplicate_email(self):
        # Assuming this email is already used by a user.
        response = requests.post(BASE_URL_USERS, json=self.test_user, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_3_create_user_invalid_data(self):
        # Missing required fields in the payload
        invalid_user = {"first_name": "Incomplete"}
        response = requests.post(BASE_URL_USERS, json=invalid_user, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_4_get_user_success(self):
        # Retrieve the user by ID
        response = requests.get(f"{BASE_URL_USERS}{user_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], self.test_user["first_name"])
        self.assertEqual(data["last_name"], self.test_user["last_name"])
        self.assertEqual(data["email"], self.test_user["email"])

    def test_5_get_user_not_found(self):
        # Use a non-existent user ID
        response = requests.get(f"{BASE_URL_USERS}nonexistent_id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_6_list_users_success(self):
        response = requests.get(BASE_URL_USERS, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_7_update_user_success(self):
        # Update user data
        updated_user = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
        response = requests.put(f"{BASE_URL_USERS}{user_id}", json=updated_user, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["first_name"], updated_user["first_name"])
        self.assertEqual(data["last_name"], updated_user["last_name"])
        self.assertEqual(data["email"], updated_user["email"])

    def test_8_update_user_not_found(self):
        # Attempt to update a non-existent user
        updated_user = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
        response = requests.put(f"{BASE_URL_USERS}nonexistent_id", json=updated_user, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_9_update_user_invalid_data(self):
        # Attempt update with invalid data
        invalid_user = {"email": "not-an-email"}
        response = requests.put(f"{BASE_URL_USERS}{user_id}", json=invalid_user, headers=self.headers)
        self.assertEqual(response.status_code, 400)

class Test_2_AmenityAPI(unittest.TestCase):

    def setUp(self):
        # Initialisation des données et des en-têtes pour chaque test
        self.test_amenity = {"name": "Wi-Fi"}
        self.updated_amenity = {"name": "Air Conditioning"}
        self.headers = {"Content-Type": "application/json"}
        self.amenity_id = None

    def test_1_create_amenity_success(self):
        # Création d'une nouvelle amenity avec succès
        response = requests.post(BASE_URL_AMENITIES, json=self.test_amenity, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], self.test_amenity["name"])

        # Sauvegarde de l'ID pour utilisation dans d'autres tests
        self.amenity_id = data["id"]

        global amenities_id
        amenities_id = data["id"]

    def test_2_create_amenity_invalid_data(self):
        # Tentative de création avec des données invalides (nom manquant)
        invalid_amenity = {}
        response = requests.post(BASE_URL_AMENITIES, json=invalid_amenity, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_3_get_amenity_list_success(self):
        # Récupération de la liste des amenities
        response = requests.get(BASE_URL_AMENITIES, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_4_get_amenity_by_id_success(self):
        # Vérification de l'ID de l'amenity créé
        if not self.amenity_id:
            self.test_1_create_amenity_success()

        # Récupération de l'amenity spécifique
        response = requests.get(f"{BASE_URL_AMENITIES}{self.amenity_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], self.amenity_id)
        self.assertEqual(data["name"], self.test_amenity["name"])

    def test_5_get_amenity_by_id_not_found(self):
        # Tentative de récupération d'une amenity non existante
        response = requests.get(f"{BASE_URL_AMENITIES}nonexistent_id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_6_update_amenity_success(self):
        # Vérification de l'ID de l'amenity créé
        if not self.amenity_id:
            self.test_1_create_amenity_success()

        # Mise à jour de l'amenity
        response = requests.put(f"{BASE_URL_AMENITIES}{self.amenity_id}", json=self.updated_amenity, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Amenity updated successfully")

    def test_7_update_amenity_not_found(self):
        # Tentative de mise à jour d'une amenity non existante
        response = requests.put(f"{BASE_URL_AMENITIES}nonexistent_id", json=self.updated_amenity, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_8_update_amenity_invalid_data(self):
        # Mise à jour avec des données invalides
        invalid_data = {"name": ""}
        if not self.amenity_id:
            self.test_1_create_amenity_success()

        response = requests.put(f"{BASE_URL_AMENITIES}{self.amenity_id}", json=invalid_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)

class Test_3_PlaceAPI(unittest.TestCase):

    def setUp(self):
        self.headers = {"Content-Type": "application/json"}
        self.place_data = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100.0,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner": user_id
        }
        self.place_id = None

    def test_1_create_place_success(self):
        response = requests.post(BASE_URL_PLACES, json=self.place_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], self.place_data["title"])
        self.place_id = data["id"]

        global place_id
        place_id = data["id"]

    def test_2_create_place_invalid_data(self):
        invalid_data = {"title": "Incomplete Place"}
        response = requests.post(BASE_URL_PLACES, json=invalid_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_3_get_all_places(self):
        response = requests.get(BASE_URL_PLACES, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_4_get_place_by_id_success(self):
        response = requests.get(f"{BASE_URL_PLACES}{place_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], place_id)
        self.assertEqual(data["title"], self.place_data["title"])
        self.assertIn("owner", data)
        self.assertIn("amenities", data)

    def test_5_get_place_by_id_not_found(self):
        response = requests.get(f"{BASE_URL_PLACES}nonexistent_id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_6_update_place_success(self):
        updated_data = {
            "title": "Luxury Condo",
            "description": "An upscale place to stay",
            "price": 200.0
        }
        response = requests.put(f"{BASE_URL_PLACES}{place_id}", json=updated_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["message"], "Place updated successfully")

    def test_7_update_place_not_found(self):
        updated_data = {
            "title": "Nonexistent Condo",
            "description": "Non-existent description",
            "price": 200.0
        }
        response = requests.put(f"{BASE_URL_PLACES}nonexistent_id", json=updated_data, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_8_update_place_invalid_data(self):
        invalid_data = {"price": "invalid-price"}
        response = requests.put(f"{BASE_URL_PLACES}{place_id}", json=invalid_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_9_add_amenity(self):
        response = requests.post(f"{BASE_URL_PLACES}{place_id}/add_amenity/{amenities_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)

class Test_4_ReviewAPI(unittest.TestCase):

    def setUp(self):
        self.headers = {"Content-Type": "application/json"}
        self.review_data = {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }

    def test_01_create_review_success(self):
        response = requests.post(BASE_URL_REVIEWS, json=self.review_data, headers=self.headers)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertIn("id", data)

        global review_id
        review_id = data["id"]

    def test_02_create_review_invalid_data(self):
        invalid_data = {"text": "Incomplete"}
        response = requests.post(BASE_URL_REVIEWS, json=invalid_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_03_get_reviews_success(self):
        response = requests.get(BASE_URL_REVIEWS, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_04_get_review_success(self):
        response = requests.get(f"{BASE_URL_REVIEWS}{review_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], review_id)

    def test_05_get_review_not_found(self):
        response = requests.get(f"{BASE_URL_REVIEWS}nonexistent_id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_06_update_review_success(self):
        updated_data = {"text": "Amazing stay!", "rating": 4}
        response = requests.put(f"{BASE_URL_REVIEWS}{review_id}", json=updated_data, headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Review updated successfully")

    def test_07_update_review_not_found(self):
        updated_data = {"text": "Amazing stay!", "rating": 4}
        response = requests.put(f"{BASE_URL_REVIEWS}nonexistent_id", json=updated_data, headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_08_update_review_invalid_data(self):
        invalid_data = {"rating": "not-a-number"}
        response = requests.put(f"{BASE_URL_REVIEWS}{review_id}", json=invalid_data, headers=self.headers)
        self.assertEqual(response.status_code, 400)

    def test_09_delete_review_success(self):
        response = requests.delete(f"{BASE_URL_REVIEWS}{review_id}", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Review deleted successfully")

    def test_10_delete_review_not_found(self):
        response = requests.delete(f"{BASE_URL_REVIEWS}nonexistent_id", headers=self.headers)
        self.assertEqual(response.status_code, 404)

    def test_11_get_reviews_for_place_success(self):
        ureview_data = {
            "text": "Hello",
            "rating": 3,
            "user_id": user_id,
            "place_id": place_id
        }
        requests.post(BASE_URL_REVIEWS, json=self.review_data, headers=self.headers)
        requests.post(BASE_URL_REVIEWS, json=ureview_data, headers=self.headers)

        response = requests.get(f"{BASE_URL_REVIEWS}places/{self.review_data['place_id']}/reviews", headers=self.headers)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIsInstance(data, list)

    def test_12_get_reviews_for_place_not_found(self):
        response = requests.get(f"{BASE_URL_REVIEWS}places/nonexistent_id/reviews", headers=self.headers)
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()