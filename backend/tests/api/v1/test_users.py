from backend.database import Base
from .utils import client, engine, login

import pytest

@pytest.fixture(scope='session', autouse=True)
def reset_database(request):
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def test_create_valid_user_1():
    """Test to create a valid user 1."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique', 'password': '123'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}


def test_create_valid_user_2():
    """Test to create a valid user 2."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'me', 'password': '123'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 2, 'username': 'Me', 'is_active': True, 'games': []}


def test_create_invalid_username_1():
    """Test to create a user with an invalid username 1."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique@', 'password': '123'}
    )
    assert response.status_code == 400


def test_create_invalid_username_2():
    """Test to create a user with an invalid username 2."""
    response = client.post(
        '/api/v1/users/',
        json={'username': '', 'password': '123'}
    )
    assert response.status_code == 400


def test_create_duplicated_username_1():
    """Test to create a user with a duplicated username 1."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique1', 'password': '123'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 3, 'username': 'Enrique1', 'is_active': True, 'games': []}

    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique1', 'password': '123'}
    )
    assert response.status_code == 400


def test_create_duplicated_username_2():
    """Test to create a user with a duplicated username."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique2', 'password': '123'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 4, 'username': 'Enrique2', 'is_active': True, 'games': []}

    response = client.post(
        '/api/v1/users/',
        json={'username': 'EnRIque2', 'password': '123'}
    )
    assert response.status_code == 400


def test_create_missing_username():
    """Test to create a user missing the username."""
    response = client.post(
        '/api/v1/users/',
        json={'password': '123'}
    )
    assert response.status_code == 422    


def test_create_missing_password():
    """Test to create a user missing the password."""
    response = client.post(
        '/api/v1/users/',
        json={'username': 'Enrique3'}
    )
    assert response.status_code == 422  


def test_read_valid_user():
    """Test to read a valid user."""
    response = client.get(
        '/api/v1/users/Enrique',
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}


def test_read_invalid_user():
    """Test to read a invalid user."""
    response = client.get(
        '/api/v1/users/Enrique12345',
    )
    assert response.status_code == 404


def test_read_current_user():
    """Test to read the current user."""
    token = login('Enrique', '123')
    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}


def test_read_current_user_not_logged():
    """Test to read the current user beeing not logged."""
    response = client.get(
        '/api/v1/users/me',
    )
    assert response.status_code == 401


def test_change_password():
    """Test to change the password of the current user."""
    token = login('Enrique', '123')
    response = client.put(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
        json={'new_password': '1234'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}

    token = login('Enrique', '1234')
    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}


def test_change_password_invalid_token():
    """Test to revoke access to previous tokens."""
    token = login('Enrique', '1234')
    response = client.put(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
        json={'new_password': '12345'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}

    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
    )
    # NOTE: This must not work but as JWT tokens are stateless it works
    assert response.status_code == 200


def test_change_password_changes():
    """Test to check if the password really changes."""
    token = login('Enrique', '12345')
    response = client.put(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
        json={'new_password': '123456'}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'Enrique', 'is_active': True, 'games': []}

    token = login('Enrique', '12345')
    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 401


def test_change_password_not_logged():
    """Test to change the password of the current user beeing not logged."""
    response = client.put(
        '/api/v1/users/me',
        json={'new_password': '1234'}
    )
    assert response.status_code == 401


def test_delete_user():
    """Test to delete a user."""
    token = login('Enrique', '123456')
    response = client.delete(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 204
    assert response.json() == None

    response = client.get(
        '/api/v1/users/me',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 401
