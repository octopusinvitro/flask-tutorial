from flaskr import db


def test_new_is_successful(client, app):
    response = client.get('/auth/register')
    assert response.status_code == 200


def test_new_renders_register_view(client, app):
    response = client.get('/auth/register')
    assert 'Register' in str(response.data)


def test_create_validates_username_presence(client, app):
    response = client.post('/auth/register', data={'username': '', 'password': 'test'})
    assert b'Username is required.' in response.data


def test_create_validates_password_presence(client, app):
    response = client.post('/auth/register', data={'username': 'name', 'password': ''})
    assert b'Password is required.' in response.data


def test_create_validates_user_is_new(client, app):
    response = client.post('/auth/register', data={'username': 'test', 'password': 'test'})
    assert b'already registered' in response.data


def test_create_saves_login_in_database(client, app):
    client.post('/auth/register', data={'username': 'user', 'password': 'pass'})
    with app.app_context():
        assert db.get_user('username', 'user') is not None


def test_create_hashes_password(client, app):
    client.post('/auth/register', data={'username': 'admin', 'password': 'secret'})
    with app.app_context():
        admin = db.get_user('username', 'admin')
        assert 'pbkdf2:sha256:' in admin['password']


def test_create_redirects_to_login(client, app):
    response = client.post('/auth/register', data={'username': 'a', 'password': 'a'})
    assert response.headers['Location'] == 'http://localhost/auth/login'
