from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository
from app import db

class PlacesRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)