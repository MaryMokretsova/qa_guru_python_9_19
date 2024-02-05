import requests
from jsonschema import validate
from resources.schemas import create_post_user_schema, list_user_schema, update_user_schema, get_user_schema


# 1. на каждый из методов GET/POST/PUT/DELETE ручек reqres.in
# 3. На разные статус-коды 200/201/204/404/400

def test_get_user_check_status_code():
    response = requests.get('https://reqres.in/api/users/2')
    assert response.status_code == 200


def test_post_user_check_status_code():
    response = requests.post('https://reqres.in/api/users', data={"name":"morpheus","job":"leader"})
    assert response.status_code == 201


def test_put_user_check_status_code():
    response = requests.put('https://reqres.in/api/users/2', data={"name":"morpheus","job":"zion resident"})
    assert response.status_code == 200


def test_delete_user_check_status_code():
    response = requests.delete('https://reqres.in/api/users/2')
    assert response.status_code == 204


def test_registration_successful():
    response = requests.post('https://reqres.in/api/register', data={"email":"eve.holt@reqres.in","password":"pistol"})
    assert response.status_code == 200
    assert response.json()['token']


def test_registration_without_email_and_password():
    response = requests.post('https://reqres.in/api/register')
    assert response.status_code == 400
    assert response.json()['error']


def test_get_resource_not_found():
    response = requests.get('https://reqres.in/api/unknown/23')
    assert response.status_code == 404


# 2. Позитивные/Негативные тесты на одну из ручек.
# 5. С ответом

def test_login_successful():
    response = requests.post('https://reqres.in/api/login', data={"email":"eve.holt@reqres.in","password":"cityslicka"})
    assert response.status_code == 200
    body = response.json()
    assert body['token'] == 'QpwL5tke4Pnpja7X4'


def test_login_without_password():
    response = requests.post('https://reqres.in/api/login', data={"email":"peter@klaven"})
    assert response.status_code == 400
    body = response.json()
    assert body['error'] == 'Missing password'


# 5. и без ответа
def test_delete_user_check_empty_response():
    response = requests.delete('https://reqres.in/api/users/2')
    print(response.text)
    assert response.text == ''


def test_single_user_not_found_returns_empty_body():
    response = requests.get('https://reqres.in/api/users/23')
    assert response.status_code == 404
    body = response.json()
    assert body == {}


# На разные схемы (4-5 схем)

def test_create_user_validate_schema():
    response = requests.post('https://reqres.in/api/users', data={"name":"morpheus","job":"leader"})
    validate(response.json(), schema=create_post_user_schema)


def test_get_user_validate_schema():
    response = requests.get('https://reqres.in/api/users/2')
    validate(response.json(), schema=get_user_schema)


def test_list_users_validate_schema():
    response = requests.get('https://reqres.in/api/users?page=2', params={"page": 2})
    validate(response.json(), schema=list_user_schema)


def test_update_user_validate_schema():
    response = requests.patch('https://reqres.in/api/users/2', data={"name":"morpheus","job":"zion resident"})
    validate(response.json(), schema=update_user_schema)


def test_change_status_code():
    response = requests.post('https://reqres.in/api/users')
    assert response.status_code == 201
    last_link = '?page=2'
    response = requests.get(f"https://reqres.in/api/users/{last_link}")
    assert response.status_code == 200


# 6. На бизнес-логику
def test_if_username_and_job_updated():
    name = 'alla'
    job = 'doctor'
    response = requests.post('https://reqres.in/api/users', json={"name": name, "job": job})
    body = response.json()
    assert body["name"] == name
    assert body["job"] == job
