import pytest
from flaskr import db


def test_index_shows_auth_links_when_not_logged(client, app):
    response = client.get('/')
    assert b'Log In' in response.data
    assert b'Register' in response.data


def test_index_shows_content_when_logged(client, auth):
    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'test title' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\nbody' in response.data
    assert b'href="/1/update"' in response.data


def test_new_is_successful(client, auth, app):
    auth.login()
    response = client.get('/create')
    assert response.status_code == 200


def test_new_renders_create_view(client, auth, app):
    auth.login()
    response = client.get('/create')
    assert b'New Post' in response.data


@pytest.mark.parametrize('path', (
    '/create',
    '/1/update',
    '/1/delete',
))
def test_create_update_and_delete_redirect_to_login_when_not_logged(client, path):
    response = client.post(path)
    assert response.headers['Location'] == 'http://localhost/auth/login'


def test_create_validates_title_presence(client, auth):
    auth.login()
    response = client.post('/create', data={'title': '', 'body': ''})
    assert b'New Post' in response.data
    assert b'Title is required.' in response.data


def test_create_saves_post_in_database(client, auth, app):
    auth.login()
    client.post('/create', data={'title': 'created', 'body': ''})
    with app.app_context():
        assert db.get_posts_count() == 2


def test_create_redirects_to_index(client, auth, app):
    auth.login()
    response = client.post('/create', data={'title': 'created', 'body': ''})
    assert response.headers['Location'] == 'http://localhost/'


def test_edit_is_successful(client, auth, app):
    auth.login()
    response = client.get('/1/update')
    assert response.status_code == 200


def test_edit_renders_update_view(client, auth, app):
    auth.login()
    response = client.get('/1/update')
    assert b'Edit ' in response.data


def test_update_forbids_modifying_other_users_posts(client, auth, app):
    change_post_user_id(app)
    auth.login()
    assert client.post('/1/update', data={'title': 'test', 'body': 'test'}).status_code == 403
    assert client.post('/1/delete').status_code == 403


def test_users_can_not_see_edit_link_for_other_users_posts(client, auth, app):
    change_post_user_id(app)
    auth.login()
    response = client.get('/')
    assert b'href="/1/update"' not in response.data


@pytest.mark.parametrize('path', (
    '/2/update',
    '/2/delete',
))
def test_update_and_delete_can_not_modify_inexistent_posts(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_update_validates_title_presence(client, auth):
    auth.login()
    response = client.post('/1/update', data={'title': '', 'body': ''})
    assert b'Edit ' in response.data
    assert b'Title is required.' in response.data


def test_update_modifies_post_in_database(client, auth, app):
    auth.login()
    client.post('/1/update', data={'title': 'updated', 'body': ''})

    with app.app_context():
        post = db.get_post(1)
        assert post['title'] == 'updated'


def test_update_redirects_to_index(client, auth, app):
    auth.login()
    response = client.post('/1/update', data={'title': 'updated', 'body': ''})
    assert response.headers['Location'] == 'http://localhost/'


def test_delete_removes_post_from_database(client, auth, app):
    auth.login()
    client.post('/1/delete')
    with app.app_context():
        post = db.get_post(1)
        assert post is None


def test_delete_redirects_to_index(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers['Location'] == 'http://localhost/'


def change_post_user_id(app):
    with app.app_context():
        db.update_post_id(2, 1)
