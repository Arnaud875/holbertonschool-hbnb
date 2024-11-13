from flask.testing import FlaskClient
from typing import Union, Dict, List, Any, Optional, Callable
from flask import Response
from dataclasses import dataclass, field
from datetime import datetime
from functools import wraps
import pytest
import json

class AuthenticatedClient:
    def __init__(self, client: FlaskClient, token: str = None):
        self.client = client
        self.token = token

    def _add_auth_header(self, kwargs: Dict) -> Dict:
        if self.token:
            headers = kwargs.get('headers', {})
            headers['Authorization'] = f'Bearer {self.token}'
            kwargs['headers'] = headers
        return kwargs

    def get(self, *args, **kwargs):
        return self.client.get(*args, **self._add_auth_header(kwargs))

    def post(self, *args, **kwargs):
        return self.client.post(*args, **self._add_auth_header(kwargs))

    def put(self, *args, **kwargs):
        return self.client.put(*args, **self._add_auth_header(kwargs))

    def delete(self, *args, **kwargs):
        return self.client.delete(*args, **self._add_auth_header(kwargs))

class SharedData:
    def __init__(self):
        self.user_id: int = None
        self.place_id: int = None
        self.review_id: int = None
        self.amenity_id: int = None
        self.token: str = None

        self.reviews = []
        self.amenities = []
        self.users = []

        self.user_payload = {
            "first_name": "Hello",
            "last_name": "World",
            "email": "hello.world@gmail.com",
            "password": "hellomyfriend"
        }

        self.place_payload = {
            'title': "My place",
            'description': "The best place",
            'price': 5000,
            'latitude': 70,
            'longitude': 90,
            'owner': None
        }

        self.review_payload = {
            'text': "This is my review",
            'rating': 5,
            'user_id': None,
            'place_id': None
        }

        self.amenities_payload = {
            "name": "Wi-Fi"
        }

    def get_place_data(self):
        return {
            "id": self.place_id,
            "title": self.place_payload["title"],
            "description": self.place_payload["description"],
            "price": self.place_payload["price"],
            "latitude": self.place_payload["latitude"],
            "longitude": self.place_payload["longitude"],
            "owner": {
                "id": self.user_id,
                "first_name": self.user_payload["first_name"],
                "last_name": self.user_payload["last_name"],
                "email": self.user_payload["email"]
            },
            "reviews": [],
            "amenities": []
        }

    def user_template(self):
        return ["id", "first_name", "last_name", "email"]

    def place_template(self):
        return ["title", "description", "price", "latitude", "longitude", "owner"]

    def reviews_template(self):
        return ["text", "rating", "user_id", "place_id"]

    def amenities_template(self):
        return ["name"]

def check_response(
    response: Response,
    status_code: int = 200,
    template: List[str] = None,
    expected_payload: Union[List[str], List[Dict[str, Any]], None] = None,
    exclude_payload: List[str] = None,
    array_payload: List[Dict] = None,
    array_template: List[str] = None,
    partial_match: bool = False,
) -> Dict:
    """
    Vérifie la réponse HTTP et son contenu.

    Args:
        response: Réponse Flask
        status_code: Code HTTP attendu
        template: Liste des champs attendus dans la réponse
        expected_payload: Valeurs attendues dans la réponse
        exclude_payload: Champs à exclure de la réponse
        array_payload: Liste de dictionnaires à comparer avec la réponse (pour les endpoints retournant des tableaux)
        array_template: Template pour chaque élément du tableau
        partial_match: Si True, permet des champs supplémentaires dans la réponse
    """
    assert response.status_code == status_code, \
        f"Status code incorrect. Attendu {status_code}, reçu {response.status_code}"

    # Si aucune vérification n'est demandée, retourner la réponse
    if not any([expected_payload, template, array_payload, array_template]):
        return response.get_json() if response.data else None

    try:
        response_data = response.get_json()
    except json.JSONDecodeError:
        raise AssertionError("La réponse n'est pas au format JSON valide")

    assert response_data is not None, "La réponse est vide"

    # Vérification des champs exclus
    if exclude_payload:
        forbidden_fields = [f for f in exclude_payload if f in response_data]
        assert not forbidden_fields, f"Champs interdits trouvés: {forbidden_fields}"

    # Vérification du template
    if template:
        missing_fields = [field for field in template if field not in response_data]
        assert not missing_fields, f"Champs manquants: {missing_fields}"

        if not partial_match:
            unexpected_fields = [
                field for field in response_data
                if field not in template
                and (not expected_payload or field not in [k for d in expected_payload if isinstance(d, dict) for k in d.keys()])
            ]
            assert not unexpected_fields, f"Champs inattendus: {unexpected_fields}"

    # Vérification des valeurs attendues
    if expected_payload:
        for item in expected_payload:
            if isinstance(item, dict):
                for key, expected_value in item.items():
                    assert key in response_data, f"Clé manquante: {key}"
                    assert response_data[key] == expected_value, \
                        f"Valeur incorrecte pour {key}. Attendu {expected_value}, reçu {response_data[key]}"
            else:
                assert item in response_data, f"Élément manquant: {item}"

    # Vérification du tableau
    if array_payload or array_template:
        assert isinstance(response_data, list), "La réponse devrait être un tableau"

        if array_template:
            for item in response_data:
                missing_fields = [field for field in array_template if field not in item]
                assert not missing_fields, f"Champs manquants dans un élément du tableau: {missing_fields}"

                if not partial_match:
                    unexpected_fields = [field for field in item if field not in array_template]
                    assert not unexpected_fields, f"Champs inattendus dans un élément du tableau: {unexpected_fields}"

        if array_payload:
            assert len(response_data) == len(array_payload), \
                f"Taille du tableau incorrecte. Attendu {len(array_payload)}, reçu {len(response_data)}"

            for expected_item in array_payload:
                matching_item = next(
                    (item for item in response_data
                        if all(item.get(k) == v for k, v in expected_item.items())),
                    None
                )
                assert matching_item is not None, \
                    f"Élément non trouvé dans la réponse: {expected_item}"

    return response_data

def check_multiple_action(
    optionals: Dict,
    method: any,
    payload: Dict,
    url: str,
    default_status_code: int,
    default_excepted_payload: Dict
):
    for i in optionals:
        new_payload = payload.copy()
        for k, v in i.items():
            if not k in ["status", "excepted_payload"] or new_payload.get(k):
                new_payload[k] = v

        status_code = i["status"] if i.get("status") else default_status_code
        excepted_payload = i["excepted_payload"] \
            if i.get("excepted_payload") else default_excepted_payload

        check_response(
            method(url, json=new_payload),
            status_code=status_code,
            expected_payload=[excepted_payload]
        )

def array_without_value(data: List, value_to_remove: List[str]) -> List:
    return [ i for i in data if i not in value_to_remove ]

def dict_without_keys(data: Dict, keys_to_remove: List[str]) -> Dict:
    return {k: v for k, v in data.items() if k not in keys_to_remove}

def payload_to_array(data: Dict) -> List[Dict]:
    return [ {k: v} for k, v in data.items() ]