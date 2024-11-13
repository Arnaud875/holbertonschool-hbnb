from .base import BaseModel
from app import bcrypt, db
import re

class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column("first_name", db.String(50), nullable=False)
    _last_name = db.Column("last_name", db.String(50), nullable=False)
    _email = db.Column("email", db.String(120), nullable=False, unique=True)
    _password = db.Column("password", db.String(128), nullable=False)
    _is_admin = db.Column("is_admin", db.Boolean, default=False)

    reviews = db.relationship('Review', back_populates='user', lazy='dynamic')
    places = db.relationship('Place', back_populates='owner', lazy='dynamic')

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if len(value) > 50:
            raise ValueError("First name must not exceed 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if len(value) > 50:
            raise ValueError("Last name must not exceed 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", value):
            raise ValueError("Invalid email format")
        self._email = value

    @property
    def is_admin(self):
        return self._is_admin

    @is_admin.setter
    def is_admin(self, value = False):
        self._is_admin = value

    @property
    def password(self):
        raise AttributeError("Password is a private attribut")

    @password.setter
    def password(self, password):
        self._password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self._password, password)
