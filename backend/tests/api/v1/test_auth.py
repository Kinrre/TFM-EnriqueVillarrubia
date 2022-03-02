from backend.database import Base
from .utils import client, engine

import pytest

@pytest.fixture(scope='session', autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_valid_user():
    """Test to create a valid user."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique', 'password': '123'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}


def test_valid_login():
    """Test to do a valid login."""
    response = client.post(
        '/api/v1/auth/token',
        data={'grant_type': 'password', 'username': 'Enrique', 'password': '123'}
    )
    assert response.status_code == 200
    assert response.json()['token_type'] == 'bearer'


def test_invalid_username():
    """Test to do a login with invalid username."""
    response = client.post(
        '/api/v1/auth/token',
        data={'grant_type': 'password', 'username': 'Enrique1', 'password': '123'}
    )
    assert response.status_code == 401


def test_invalid_password():
    """Test to do a login with invalid password."""
    response = client.post(
        '/api/v1/auth/token',
        data={'grant_type': 'password', 'username': 'Enrique', 'password': '1234'}
    )
    assert response.status_code == 401
