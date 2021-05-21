import pytest
from fastapi.testclient import TestClient
from web_blackjack import app


@pytest.fixture
def base_client():
    return TestClient(app)


def test_home(base_client):
    response = base_client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Blackjack!"}


def test_create(base_client):
    response = base_client.get('/game/create/1')
    response_json = response.json()
    assert response.status_code == 201
    assert response_json['success'] is True
    assert len(response_json['game_id']) == 36
    assert len(response_json['termination_password']) == 36


@pytest.fixture
def get_game(base_client):
    resp = base_client.get('/game/create/1')
    resp_json = resp.json()
    return resp_json


def test_initialize(get_game, base_client):
    game_id = get_game['game_id']
    resp = base_client.post(f'/game/{game_id}/initialize')
    resp_json = resp.json()
    assert resp_json['success'] is True
    assert len(resp_json['dealer_stack']) == 2
    assert len(resp_json['player_stacks']) == 1
    assert len(resp_json['player_stacks'][0]) == 2


@pytest.fixture
def get_init_game(get_game, base_client):
    resp = base_client.post(f'/game/{get_game["game_id"]}/initialize')
    return get_game


def test_get_stacks(get_init_game, base_client):
    game_id = get_init_game['game_id']
    resp = base_client.get(f'/game/{game_id}/stacks')
    resp_json = resp.json()
    assert resp_json['success'] is True
    assert len(resp_json['dealer_stack']) == 2
    assert len(resp_json['player_stacks']) == 1
    assert len(resp_json['player_stacks'][0]) == 2


def test_player_hit(get_init_game, base_client):
    game_id = get_init_game['game_id']
    resp = base_client.post(f'/game/{game_id}/player/0/hit')
    resp_json = resp.json()
    assert int(resp_json['player']) == 0
    assert len(resp_json['player_stack']) == 3


def test_player_stack(get_init_game, base_client):
    game_id = get_init_game['game_id']
    resp = base_client.get(f'/game/{game_id}/player/0/stack')
    resp_json = resp.json()
    assert int(resp_json['player']) == 0
    assert len(resp_json['player_stack']) == 2


def test_dealer_play(get_init_game, base_client):
    game_id = get_init_game['game_id']
    resp = base_client.post(f'/game/{game_id}/dealer/play')
    resp_json = resp.json()
    assert resp_json['player'] == 'dealer'
    assert len(resp_json['player_stack']) >= 2


@pytest.fixture
def get_dealer_won_game(get_init_game, base_client):
    resp = base_client.post(f'/game/{get_init_game["game_id"]}/dealer/play')
    return get_init_game


def test_get_winners(get_dealer_won_game, base_client):
    game_id = get_dealer_won_game['game_id']
    resp = base_client.get(f'/game/{game_id}/winners')
    resp_json = resp.json()
    assert resp_json['game_id'] == game_id
    assert len(resp_json['winners']) >= 1
    assert resp_json['winners'][0] in ['NONE', 'DEALER']


def test_delete_game(get_dealer_won_game, base_client):
    game_id = get_dealer_won_game['game_id']
    term_pass = get_dealer_won_game['termination_password']
    resp = base_client.post(f'/game/{game_id}/terminate')
    assert resp.status_code == 422
    resp = base_client.post(f'/game/{game_id}/terminate?password=fail')
    assert resp.status_code == 401
    resp = base_client.post(f'/game/{game_id}/terminate?password={term_pass}')
    resp_json = resp.json()
    assert resp_json['success'] is True
    assert resp_json['deleted_id'] == game_id


if __name__ == '__main__':
    pytest.main()
