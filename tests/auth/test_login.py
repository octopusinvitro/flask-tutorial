from flask import g, session


def test_new_is_successful(client, app):
    response = client.get('/auth/login')
    assert response.status_code == 200


def test_new_renders_login_view(client, app):
    response = client.get('/auth/login')
    assert 'Log In' in str(response.data)


def test_create_validates_username_correctness(client, app):
    response = client.post('/auth/login', data={'username': 'idontexist', 'password': 'test'})
    assert 'Log In' in str(response.data)
    assert b'Incorrect username.' in response.data


def test_create_validates_password_correctness(client, app):
    response = client.post('/auth/login', data={'username': 'test', 'password': 'incorrect'})
    assert 'Log In' in str(response.data)
    assert b'Incorrect password.' in response.data


def test_create_when_logged_sets_user_cookie(client, app):
    client.post('/auth/login', data={'username': 'test', 'password': 'test'})
    with client:
        client.get('/')
        assert session['user_id'] == 1


def test_create_when_logged_sets_user_global(client, app):
    client.post('/auth/login', data={'username': 'test', 'password': 'test'})
    with client:
        client.get('/')
        assert g.user['username'] == 'test'


def test_create_redirects_to_index(client, app):
    response = client.post('/auth/login', data={'username': 'test', 'password': 'test'})
    assert response.headers['Location'] == 'http://localhost/'


def test_logout_unsets_user_cookie(client, auth):
    client.post('/auth/login', data={'username': 'test', 'password': 'test'})
    with client:
        client.get('/auth/logout')
        assert 'user_id' not in session


def test_logout_redirects_to_index(client, auth):
    client.post('/auth/login', data={'username': 'test', 'password': 'test'})
    with client:
        response = client.get('/auth/logout')
        assert response.headers['Location'] == 'http://localhost/'
