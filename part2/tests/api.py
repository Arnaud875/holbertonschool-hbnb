import unittest
from unittest.mock import patch, Mock
import requests

# Support User and Amenity endpoint

API = "http://localhost:5000/api/v1"

def req(endpoint, methods = "GET", payload = None):
    response = requests.request(
        methods,
        f"{API}/{endpoint}",
        headers={"Content-Type": "application/json"} if methods == "POST" or methods == "PUT" else None,
        json=payload if methods == "POST" or methods == "PUT" else None
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


class TestUserEndpoint(unittest.TestCase):
    @patch('requests.post')
    @patch('requests.get')
    def test_user_endpoint(self, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
        })

        data, status = post("users", {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"})
        self.assertEqual(status, 201)
        self.assertEqual(data["first_name"], "John")
        self.assertEqual(data["last_name"], "Doe")
        self.assertEqual(data["email"], "john.doe@example.com")

        id = data["id"]

        mock_post.return_value = Mock(status_code=400, json=lambda: {
            "error": "Email already registered"
        })
        data, status = post("users", {"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"})
        self.assertEqual(status, 400)
        self.assertEqual(data["error"], "Email already registered")

        mock_post.return_value = Mock(status_code=400, json=lambda: {
            "errors": {"email": "'email' is a required field"}
        })
        data, status = post("users", {"yes": "sir"})
        self.assertEqual(status, 400)
        self.assertIn("'email' is a required", data["errors"]["email"])

        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"
        })
        data, status = get(f"users/{id}")
        self.assertEqual(status, 200)
        self.assertEqual(data["first_name"], "John")

        data, status = post("users", {"first_name": "A" * 51, "last_name": "Doe", "email": "hello@gmail.com"})
        self.assertEqual(data["error"], "First name and Last name must not exceed 50 characters")

        data, status = post("users", {"first_name": "A", "last_name": "B" * 51, "email": "hello@gmail.com"})
        self.assertEqual(data["error"], "First name and Last name must not exceed 50 characters")

        data, status = post("users", {"first_name": "A", "last_name": "Doe", "email": "hellogmailcom"})
        self.assertEqual(data["error"], "Invalid email format")


class TestAmenityEndpoint(unittest.TestCase):
    @patch('requests.post')
    @patch('requests.get')
    @patch('requests.put')
    def test_amenity_endpoint(self, mock_put, mock_get, mock_post):
        mock_post.return_value = Mock(status_code=201, json=lambda: {
            "name": "WI-FI"
        })
        data, status = post("amenities", {"name": "WI-FI"})
        self.assertEqual(status, 201)
        self.assertEqual(data["name"], "WI-FI")

        id = data["id"]

        data, status = post("amenities", {"name": "hello"})

        mock_get.return_value = Mock(status_code=200, json=lambda: [
            {"name": "WI-FI"},
            {"name": "hello"}
        ])
        data, status = get("amenities")
        self.assertEqual(status, 200)
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]["name"], "WI-FI")

        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": id, "name": "WI-FI"
        })
        data, status = get(f"amenities/{id}")
        self.assertEqual(status, 200)
        self.assertEqual(data["id"], id)

        mock_get.return_value = Mock(status_code=404, json=lambda: {
            "error": "Amenity not found"
        })
        data, status = get("amenities/invalid_id")
        self.assertEqual(status, 404)
        self.assertEqual(data["error"], "Amenity not found")

        mock_put.return_value = Mock(status_code=200, json=lambda: {
            "message": "Amenity updated successfully"
        })
        data, status = put(f"amenities/{id}", {"name": "Wiwi"})
        self.assertEqual(data["message"], "Amenity updated successfully")

        mock_get.return_value = Mock(status_code=200, json=lambda: {
            "id": id, "name": "Wiwi"
        })
        data, status = get(f"amenities/{id}")
        self.assertEqual(status, 200)
        self.assertEqual(data["name"], "Wiwi")

        data, status = post("amenities", {"name": "A" * 51})
        self.assertEqual(data["error"], "Name must not exceed 50 characters")


if __name__ == '__main__':
    unittest.main()
