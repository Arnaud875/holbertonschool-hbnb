import unittest
from unittest.mock import patch, Mock
import requests

API = "http://localhost:5000/api/v1"

def req(endpoint, methods="GET", payload=None):
    response = requests.request(
        methods,
        f"{API}/{endpoint}",
        headers={"Content-Type": "application/json"} if methods in ["POST", "PUT"] else None,
        json=payload if methods in ["POST", "PUT"] else None
    )

    try:
        return response.json(), response.status_code
    except:
        raise ValueError(f"Invalid response of {endpoint} endpoint.")

def post(endpoint, payload):
    return req(endpoint, "POST", payload)

def put(endpoint, payload):
    return req(endpoint, "PUT", payload)

def get(endpoint):
    return req(endpoint, "GET")

def delete(endpoint):
    return req(endpoint, "DELETE")


class TestUserEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    def test_create_user(self, mock_put, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
        })

        print("Testing POST /users with valid input")
        data, status = post("users", {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"})
        print(f"Expected: 201, Actual: {status}, Data: {data}")

        self.assertEqual(status, 201)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "john.doe@example.com")

        id = data["id"]

        mock_post.return_value = Mock(status_code=400, json=lambda: {
            "error": "Email already registered"
        })
        print("Testing POST /users with duplicate email")
        data, status = post("users", {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"})
        print(f"Expected: 400, Actual: {status}, Data: {data}")

        self.assertEqual(status, 400)
        self.assertEqual(data["error"], "Email already registered")

        mock_post.return_value = Mock(status_code=400, json=lambda: {
            "errors": {"email": "'email' is a required field"}
        })
        print("Testing POST /users with missing email field")
        data, status = post("users", {"first_name": "John"})
        print(f"Expected: 400, Actual: {status}, Data: {data}")

        self.assertEqual(status, 400)
        self.assertIn("'email' is a required", data["errors"]["email"])

        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": id, "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
        })
        print(f"Testing GET /users/{id}")
        data, status = get(f"users/{id}")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["first_name"], "John")

    @patch('requests.put')
    def test_update_user(self, mock_put):
        data, status = post("users", {"first_name": "John2", "last_name": "Doe2", "email": "john.doe222@example.com"})
        id = data["id"]

        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "User updated successfully"
        })
        print(f"Testing PUT /users/{id} with valid update data")
        data, status = put(f"users/{id}", {"first_name": "Jane", "last_name": "Doe"})
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "User updated successfully")

        mock_put.return_value = Mock(status_code=400, json=lambda: {
            "error": "Invalid input data"
        })
        print(f"Testing PUT /users/{id} with invalid input")
        data, status = put(f"users/{id}", {"first_name": "A" * 51})
        print(f"Expected: 400, Actual: {status}, Data: {data}")

        self.assertEqual(status, 400)
        self.assertEqual(data["error"], "Invalid input data")


class TestAmenityEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    def test_amenity_endpoint(self, mock_put, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "name": "WI-FI"
        })
        print("Testing POST /amenities with valid input")
        data, status = post("amenities", {"name": "WI-FI"})
        print(f"Expected: 201, Actual: {status}, Data: {data}")

        self.assertEqual(status, 201)
        self.assertEqual(data["name"], "WI-FI")

        id = data["id"]

        mock_get.return_value = Mock(status_code=200, json=lambda: [
            {"name": "WI-FI"}, {"name": "hello"}
        ])

        post("amenities", {"name": "Fibre"})
        print("Testing GET /amenities")
        data, status = get("amenities")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "WI-FI")

        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "Amenity updated successfully"
        })
        print(f"Testing PUT /amenities/{id} with valid update")
        data, status = put(f"amenities/{id}", {"name": "Wiwi"})
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Amenity updated successfully")


class TestReviewEndpoint(unittest.TestCase):

    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    @patch('requests.delete')
    def test_review_endpoint(self, mock_delete, mock_put, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })

        print("Testing POST /reviews with valid input")
        data, status = post("reviews", {
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })
        print(f"Expected: 201, Actual: {status}, Data: {data}")

        self.assertEqual(status, 201)
        self.assertEqual(data["text"], "Great place to stay!")
        self.assertEqual(data["rating"], 5)

        mock_get.return_value = Mock(status_code=200, json=lambda: [
            {
                "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
                "text": "Great place to stay!",
                "rating": 5
            }
        ])

        print("Testing GET /reviews")
        data, status = get("reviews")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["text"], "Great place to stay!")

        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": "2fa85f64-5717-4562-b3fc-2c963f66afa6",
            "text": "Great place to stay!",
            "rating": 5,
            "user_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
            "place_id": "1fa85f64-5717-4562-b3fc-2c963f66afa6"
        })

        print("Testing GET /reviews/<id>")
        data, status = get("reviews/2fa85f64-5717-4562-b3fc-2c963f66afa6")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["text"], "Great place to stay!")

        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "Review updated successfully"
        })

        print("Testing PUT /reviews/<id> with valid input")
        data, status = put("reviews/2fa85f64-5717-4562-b3fc-2c963f66afa6", {
            "text": "Amazing experience!",
            "rating": 5
        })
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Review updated successfully")

        mock_delete.return_value = Mock(status_code=200, json=lambda: {
            "message": "Review deleted successfully"
        })

        print("Testing DELETE /reviews/<id>")
        data, status = delete("reviews/2fa85f64-5717-4562-b3fc-2c963f66afa6")
        print(f"Expected: 200, Actual: {status}, Data: {data}")

        self.assertEqual(status, 200)
        self.assertEqual(data["message"], "Review deleted successfully")

if __name__ == '__main__':
    unittest.main()
