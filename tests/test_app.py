from http import HTTPStatus

from fast_zero.schemas import UserPublic
from fast_zero.security import create_access_token


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Olá Mundo!'}


def test_read_root_html_deve_retornar_ok_e_ola_mundo(client):
    response = client.get('/html')

    assert response.status_code == HTTPStatus.OK
    assert (
        response.text
        == """
    <html>
      <head>
          <title> Fastapi do zero com Dunossauro. </title>
      </head>
      <body>
          <h1> Olá Mundo! </h1>
      </body>
    </html>"""
    )


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'barrywhite',
            'email': 'barry@example.com',
            'password': 'password',
        },
    )

    # Retornou o status_code correto?
    assert response.status_code == HTTPStatus.CREATED
    # Validar UserPublic Schema
    assert response.json() == {
        'username': 'barrywhite',
        'email': 'barry@example.com',
        'id': 1,
    }


def test_create_user_username_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'mockUser',
            'email': 'barry@example.com',
            'password': 'password',
        },
    )

    # Retornou o status_code correto?
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Retornou a mensagem correta?
    assert response.json() == {'detail': 'Username already exists'}


def test_create_user_email_already_exists(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'barrywhite',
            'email': 'mock@barrylabs.com',
            'password': 'password',
        },
    )

    # Retornou o status_code correto?
    assert response.status_code == HTTPStatus.BAD_REQUEST
    # Retornou a mensagem correta?
    assert response.json() == {'detail': 'E-mail already exists'}


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_read_users_with_user(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': [user_schema]}


def test_read_users_by_id(client, user):
    user_schema = UserPublic.model_validate(user).model_dump()

    response = client.get('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_schema


def test_read_users_by_id_not_found(client, user):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123456',
            'username': 'barry',
            'email': 'barrywhite@example.com',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'barry',
        'email': 'barrywhite@example.com',
        'id': 1,
    }


def test_update_user_not_permission(client, user, token):
    response = client.put(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': '123456',
            'username': 'barry',
            'email': 'barrywhite@example.com',
        },
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_permission(client, user, token):
    response = client.delete(
        '/users/2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Not enough permission'}


def test_delete_user_invalid_username(client, user):
    token_bad_email = create_access_token(data={'sub': 'mock2@barrylabs.com'})

    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token_bad_email}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.email, 'password': user.clean_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_invalid_creds(client):
    response = client.post(
        '/token', data={'username': 'Barry', 'password': '1239876'}
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {'detail': 'Incorrect username or password'}
