import pytest

from fastapi.testclient import TestClient

from ..templates.user_template import user_json
from ..database_test import configure_database, truncate_table
from ...main import app

from ...src.domain.user.models import User

api_route = "/api/user"
table="users"

client = TestClient(app)

@pytest.fixture
def setup_database():
    configure_database(app)
    yield
    truncate_table(table)
    
def test_get_user(setup_database):
    """Test with no users in the database"""
    response = client.get(api_route)
    assert response.status_code == 200
    assert response.json() == []

def test_create_user(setup_database, user_json):
    """ Test creating a user """
    response = client.post(api_route, json=user_json)
    assert response.status_code == 201
    assert response.json()["username"] == user_json["username"]
    
def test_user_by_id(setup_database, user_json):
    """ Test getting a user by id """
    response = client.post(api_route, json=user_json)
    user_id = response.json()["id"]
    response = client.get(f"{api_route}/{user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == user_json["username"]
    
def test_unique_username(setup_database, user_json):
    """ Test that username must be unique """
    response = client.post(api_route, json=user_json)
    assert response.status_code == 201
    response = client.post(api_route, json=user_json)
    assert response.status_code == 400    