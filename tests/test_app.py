from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'users': [
            {
                'username': 'barrywhite',
                'email': 'barry@example.com',
                'id': 1,
            }
        ]
    }


def test_read_users_by_id(client):
    response = client.get('users/1')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'id': 1,
        'username': 'barrywhite',
        'email': 'barry@example.com',
    }


def test_read_users_by_id_not_found(client):
    response = client.get('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_update_user(client):
    response = client.put(
        '/users/1',
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


def test_update_user_not_found(client):
    response = client.put(
        '/users/2',
        json={
            'password': '123456',
            'username': 'barry',
            'email': 'barrywhite@example.com',
            'id': 1,
        },
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}


def test_delete_user(client):
    response = client.delete('/users/1')

    assert response.json() == {'message': 'User deleted'}


def test_delete_user_not_found(client):
    response = client.delete('/users/2')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'User Not Found'}
