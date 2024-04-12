import pytest

@pytest.fixture
def user_json():
    return {
        "username": "aquaman",
        "password": "atlantis"
    }

@pytest.fixture
def db_user_json():
    return {
        "username": "aquaman",
        "password": "atlantis",
        "id": 1,
        "created_at": "2024-04-12T13:02:06.269896",
        "updated_at": "2024-04-12T13:02:06.269896"
    }