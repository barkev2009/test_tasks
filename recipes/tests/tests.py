import requests
import json
from recipes.config.config import config


def test_register_double():
    response = requests.put('http://127.0.0.1:8000/api/v1/register',
                            json=json.dumps({'new_nickname': 'user_1'}))
    assert response.status_code == 401


def test_check_out():
    response = requests.put('http://127.0.0.1:8000/api/v1/offline',
                            headers={'user': 'user_1'})
    assert response.status_code == 200


def test_check_in():
    response = requests.put('http://127.0.0.1:8000/api/v1/online',
                            headers={'user': 'user_1'})
    assert response.status_code == 200


def test_check_in_blocked():
    response = requests.put('http://127.0.0.1:8000/api/v1/online',
                            headers={'user': 'user_2'})
    assert response.status_code == 401


def test_alter_status_user():
    response = requests.put('http://127.0.0.1:8000/api/v1/alter',
                            headers={'user': 'admin', 'password': config['password']},
                            json={'object': 'user',
                                  'id': 50,
                                  'status': 'active'})
    assert response.status_code == 200


def test_alter_status_recipe():
    response = requests.put('http://127.0.0.1:8000/api/v1/alter',
                            headers={'user': 'admin', 'password': config['password']},
                            json={'object': 'recipe',
                                  'id': 1,
                                  'status': 'blocked'})
    assert response.status_code == 200


def test_alter_status_not_admin():
    response = requests.put('http://127.0.0.1:8000/api/v1/alter',
                            headers={'user': 'not_admin', 'password': config['password']},
                            json={'object': 'user',
                                  'id': 50,
                                  'status': 'active'})
    assert response.status_code == 401


def test_alter_status_non_existent_user():
    response = requests.put('http://127.0.0.1:8000/api/v1/alter',
                            headers={'user': 'admin', 'password': config['password']},
                            json={'object': 'user',
                                  'id': 150,
                                  'status': 'active'})
    assert response.status_code == 418


def test_add_recipe():
    response = requests.post('http://127.0.0.1:8000/api/v1/recipes',
                            headers={'user': 'user_1'},
                            json={'name': 'new_test_recipe',
                                  'type': 'drink',
                                  'descr': 'some test description'})
    assert response.status_code == 200


def test_add_recipe_incorrect_type():
    response = requests.post('http://127.0.0.1:8000/api/v1/recipes',
                            headers={'user': 'user_1'},
                            json={'name': 'new_test_recipe',
                                  'type': 'some_stuff',
                                  'descr': 'some test description'})
    assert response.status_code == 418


def test_add_recipe_not_auth():
    response = requests.post('http://127.0.0.1:8000/api/v1/recipes',
                            headers={'user': 'user_2'},
                            json={'name': 'new_test_recipe',
                                  'type': 'some_stuff',
                                  'descr': 'some test description'})
    assert response.status_code == 401


def test_get_recipes():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0', headers={'user': 'user_1'})
    assert response.status_code == 200


def test_get_recipes_all():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0?active_only=false', headers={'user': 'user_1'})
    assert response.status_code == 200


def test_get_recipes_not_auth():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0?active_only=false', headers={'user': 'user_2'})
    assert response.status_code == 401


def test_get_recipes_incorrect_path():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes', headers={'user': 'user_1'})
    assert response.status_code == 405


def test_sort_recipes_likes():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/sort?by=likes', headers={'user': 'user_1'})
    assert response.status_code == 200


def test_sort_recipes_name_not_desc():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/sort?by=name&desc=false',
                            headers={'user': 'user_1'})
    assert response.status_code == 200


def test_sort_recipes_date_incorrect_path():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/sort?by=name&desc=false',
                            headers={'user': 'user_1'})
    assert response.status_code == 500


def test_sort_recipes_date_incorrect_sorter():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/sort?by=wrong',
                            headers={'user': 'user_1'})
    assert response.status_code == 500


def test_sort_recipes_date_not_auth():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/sort?by=likes',
                            headers={'user': 'user_2'})
    assert response.status_code == 401


def test_filter_recipes_user_active():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/filter?by=user&named=user_1',
                            headers={'user': 'user_1'})
    assert response.status_code == 200


def test_filter_recipes_tag_all():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/filter?by=tag&named=tagname_1&active_only=false',
                            headers={'user': 'user_1'})
    assert response.status_code == 200


def test_filter_recipes_not_auth():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/filter?by=user&named=user_1',
                            headers={'user': 'user_2'})
    assert response.status_code == 401


def test_filter_recipes_incorrect_path():
    response = requests.get('http://127.0.0.1:8000/api/v1/recipes/0/filter?by=wrong&named=user_1',
                            headers={'user': 'user_1'})
    assert response.status_code == 500


def test_get_all_users():
    response = requests.get('http://127.0.0.1:8000/api/v1/users', headers={'user': 'user_1'})
    assert response.status_code == 200
