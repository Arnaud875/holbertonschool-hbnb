from .base import BaseModel
from app import db

place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = "places"

    _title = db.Column("title", db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    _price = db.Column("price", db.Float, nullable=False)
    _latitude = db.Column("latitude", db.Float, nullable=False)
    _longitude = db.Column("longitude", db.Float, nullable=False)
    _owner_id = db.Column("owner", db.String(36), db.ForeignKey("users.id"), nullable=False)

    owner = db.relationship("User", back_populates="places")
    reviews = db.relationship("Review", back_populates="place", lazy="dynamic")
    amenities = db.relationship("Amenity", secondary=place_amenities, back_populates="places", lazy="dynamic")

    @property
    def owner_id(self):
        return self._owner_id

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if len(value) > 100:
            raise ValueError("Title must not exceed 100 characters")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Price must be positive")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not (-90.0 <= value <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not (-180.0 <= value <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = value
