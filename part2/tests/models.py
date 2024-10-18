import sys
sys.path.append("..")

from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
import unittest

# Support all models

class TestUser(unittest.TestCase):
    def test_user_creation(self):
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(user.email, "john@example.com")
        self.assertFalse(user.is_admin)

    def test_invalid_user_name_length(self):
        with self.assertRaises(ValueError):
            User(first_name="A" * 51, last_name="Doe", email="jane@example.com")

    def test_invalid_user_email(self):
        with self.assertRaises(ValueError):
            User(first_name="Jane", last_name="Doe", email="invalidemail")

class TestPlace(unittest.TestCase):
    def test_place_creation(self):
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        place = Place(title="Beautiful Place", description="A great place to stay",
                      price=100.0, latitude=45.0, longitude=-73.0, owner=user)
        self.assertEqual(place.title, "Beautiful Place")
        self.assertEqual(place.price, 100.0)

    def test_invalid_place_price(self):
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        with self.assertRaises(ValueError):
            Place(title="Cheap Place", description="A very cheap place",
                  price=-50.0, latitude=45.0, longitude=-73.0, owner=user)

    def test_invalid_latitude_longitude(self):
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        with self.assertRaises(ValueError):
            Place(title="Weird Place", description="Weird location",
                  price=100.0, latitude=100.0, longitude=-200.0, owner=user)

class TestReview(unittest.TestCase):
    def test_review_creation(self):
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        place = Place(title="Beautiful Place", description="A great place to stay",
                      price=100.0, latitude=45.0, longitude=-73.0, owner=user)
        review = Review(text="Amazing stay", rating=5, place=place, user=user)
        self.assertEqual(review.rating, 5)

    def test_invalid_rating(self):
        user = User(first_name="John", last_name="Doe", email="john@example.com")
        place = Place(title="Beautiful Place", description="A great place to stay",
                      price=100.0, latitude=45.0, longitude=-73.0, owner=user)
        with self.assertRaises(ValueError):
            Review(text="Not great", rating=6, place=place, user=user)

class TestAmenity(unittest.TestCase):
    def test_amenity_creation(self):
        amenity = Amenity(name="Wi-Fi")
        self.assertEqual(amenity.name, "Wi-Fi")

    def test_invalid_amenity_name_length(self):
        with self.assertRaises(ValueError):
            Amenity(name="A" * 51)

if __name__ == '__main__':
    unittest.main()