from .base import BaseModel
from .place import place_amenities
from app import db

class Amenity(BaseModel):
    __tablename__ = "amenities"

    _name = db.Column("name", db.String(50), nullable=False)

    places = db.relationship("Place", secondary=place_amenities, back_populates="amenities", lazy="dynamic")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        self._name = value