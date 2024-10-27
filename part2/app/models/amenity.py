from .base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if len(value) == 0 or len(value) > 50:
            raise ValueError("Name must not exceed 50 characters")
        self.__name = value