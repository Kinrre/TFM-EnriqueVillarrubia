from backend.database import Base
from .utils import client, engine, login

import pytest

@pytest.fixture(scope='session', autouse=True)
def reset_database(request):
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


def test_create_valid_game():
    """Test to create a valid game."""
    token = login('Enrique', '123')
    response = client.post(
        '/api/v1/users/me/games/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'chess', 'board_size': 6, 'initial_board': '1pppp1/1pppp1/6/6/1PPPP1/1PPPP1', 'maximum_movements': 50, 'pieces': []}
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Chess'
    assert response.json()['owner_id'] == 1
    assert response.json()['is_trained'] == False
    assert response.json()['board_size'] == 6
    assert response.json()['initial_board'] == '1pppp1/1pppp1/6/6/1PPPP1/1PPPP1'


def test_create_invalid_game_1():
    """Test to create a invalid game 1."""
    token = login('Enrique', '123')
    response = client.post(
        '/api/v1/users/me/games/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'che|ss', 'board_size': 6, 'initial_board': '1pppp1/1pppp1/6/6/1PPPP1/1PPPP1', 'maximum_movements': 50, 'pieces': []}
    )
    assert response.status_code == 400


def test_create_invalid_game_2():
    """Test to create a invalid game 2."""
    token = login('Enrique', '123')
    response = client.post(
        '/api/v1/users/me/games/',
        headers={'Authorization': f'Bearer {token}'},
        json={'name': 'chess   ', 'board_size': 6, 'initial_board': '1pppp1/1pppp1/6/6/1PPPP1/1PPPP1', 'maximum_movements': 50, 'pieces': []}
    )
    assert response.status_code == 400


def test_create_game_not_logged():
    """Test to create a game beeing not logged."""
    response = client.post(
        '/api/v1/users/me/games/',
        json={'name': 'chess'}
    )
    assert response.status_code == 401


def test_read_games():
    """Test to read valids games."""
    response = client.get(
        '/api/v1/games/',
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_current_games():
    """Test to read current games."""
    token = login('Enrique', '123')
    response = client.get(
        '/api/v1/users/me/games/',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_read_current_specific_game():
    """Test to read current games."""
    token = login('Enrique', '123')
    response = client.get(
        '/api/v1/users/me/games/chess',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Chess'


def test_update_game_1():
    """Test to update a game 1."""
    token = login('Enrique', '123')
    response = client.put(
        '/api/v1/users/me/games/chess',
        headers={'Authorization': f'Bearer {token}'},
        json={'new_name': 'Chess2', 'is_trained': True}
    )
    assert response.status_code == 200
    response = client.get(
        '/api/v1/users/me/games/chess2',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Chess2'
    assert response.json()['is_trained'] == True


def test_update_game_2():
    """Test to update a game 2."""
    token = login('Enrique', '123')
    response = client.put(
        '/api/v1/users/me/games/chess2',
        headers={'Authorization': f'Bearer {token}'},
        json={'new_name': 'Chess3'}
    )
    assert response.status_code == 200
    response = client.get(
        '/api/v1/users/me/games/chess3',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Chess3'
    assert response.json()['is_trained'] == True


def test_update_game_3():
    """Test to update a game 3."""
    token = login('Enrique', '123')
    response = client.put(
        '/api/v1/users/me/games/chess3',
        headers={'Authorization': f'Bearer {token}'},
        json={'is_trained': False}
    )
    assert response.status_code == 200
    response = client.get(
        '/api/v1/users/me/games/chess3',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 200
    assert response.json()['name'] == 'Chess3'
    assert response.json()['is_trained'] == False


def test_delete_game():
    """Test to delete a game."""
    token = login('Enrique', '123')
    response = client.delete(
        '/api/v1/users/me/games/chess3',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == 204
    assert response.json() == None
