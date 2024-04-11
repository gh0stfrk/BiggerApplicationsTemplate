import pytest

from fastapi.testclient import TestClient
from ..database_test import configure_database, truncate_table
from ...main import app

api_route = "/api/user"
table="users"

client = TestClient(app)

@pytest.fixture
def setup_database():
    configure_database(app)

class TestUser:
    def setup_method(self, method):
        truncate_table(table)
    
    def test_get_user(self):
        response = client.get(api_route)
        assert response.status_code == 200
        assert response.json() == []
        