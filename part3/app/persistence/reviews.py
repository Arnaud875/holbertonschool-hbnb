from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app import db

class ReviewsRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)