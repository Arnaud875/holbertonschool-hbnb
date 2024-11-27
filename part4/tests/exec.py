import requests



token = requests.post("http://localhost:5000/api/v1/auth/login", json={
    "email": "admin@admin.com",
    "password": "admin"
}).json()["access_token"]

# r = requests.post("http://localhost:5000/api/v1/places", headers={"Authorization": f"Bearer {token}"}, json={
#   "title": "Yes sir",
#   "description": "My super place",
#   "price": 12,
#   "latitude": 90,
#   "longitude": 70,
#   "owner": "36c9050e-ddd3-5545-9731-9f487208bbc1"
# })

r = requests.post(f"http://localhost:5000/api/v1/places/34e7d653-90d5-4e8d-a323-25d4bf0d9072/add_amenity/15d146e4-f486-4011-aea7-6bf48d8c07da", headers={
    "Authorization": f"Bearer {token}"
})

# 86af1e58-9374-417a-a712-7faf2f1b0356
print(r.json())