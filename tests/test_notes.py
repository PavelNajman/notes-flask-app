import pytest
from http import HTTPStatus
from flask_jwt_extended import create_access_token
from app import db, create_app

test_user_jwt = None
other_user_jwt = None


@pytest.fixture()
def app():
    app = create_app("testing")

    with app.app_context():
        db.create_all()

    with app.app_context():
        global test_user_jwt
        access_token = create_access_token("test_user", fresh=True)
        test_user_jwt = {"Authorization": "Bearer {}".format(access_token)}
        global other_user_jwt
        access_token = create_access_token("other_user", fresh=True)
        other_user_jwt = {"Authorization": "Bearer {}".format(access_token)}

    yield app

    with app.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


def make_post_note_request(client):
    return client.post(
        "/note", json={"title": "title", "body": "body"}, headers=test_user_jwt
    )


def check_response(response, expected_status_code):
    assert response.status_code == expected_status_code
    assert response.json["id"]
    assert response.json["title"] == "title"
    assert response.json["body"] == "body"


def test_post_note(client):
    """
    A note can be inserted into the database with a post request that contains note title and body.
    A response contains note unique id and the sent title and body.
    """
    response = make_post_note_request(client)
    check_response(response, HTTPStatus.CREATED)


def test_post_existing_note(client):
    """
    Two notes with the same title and body can be inserted into the database.
    """
    response_1 = make_post_note_request(client)
    response_2 = make_post_note_request(client)
    check_response(response_1, HTTPStatus.CREATED)
    check_response(response_1, HTTPStatus.CREATED)
    assert response_1.json["id"] != response_2.json["id"]


def test_invalid_post_note(client):
    """
    A post note request with invalid data yields 422 error.
    """
    response = client.post("/note", json={}, headers=test_user_jwt)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_get_note(client):
    """
    An existing note can be retrived from the database using a get request to the /note/<note_id> endpoint.
    A response contains note unique id, title, and body.
    """
    response = make_post_note_request(client)
    check_response(response, HTTPStatus.CREATED)
    response = client.get(f"/note/{response.json['id']}", headers=test_user_jwt)
    check_response(response, HTTPStatus.OK)


def test_get_nonexisting_note(client):
    """
    A request to get a nonexisting note yields 404 error.
    """
    response = client.get(f"/note/0", headers=test_user_jwt)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_other_user_note(client):
    """
    A request to get an other user's note yields 404 error.
    """
    response = make_post_note_request(client)
    check_response(response, HTTPStatus.CREATED)
    response = client.get(f"/note/{response.json['id']}", headers=other_user_jwt)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_update_note(client):
    """
    An existing note can be upgraded using a put request to the /note/<note_id> endpoint.
    A response contains note original unique id, updated title, and body.
    """
    response_1 = make_post_note_request(client)
    check_response(response_1, HTTPStatus.CREATED)
    response_2 = client.put(
        f"/note/{response_1.json['id']}",
        json={"title": "title2", "body": "body2"},
        headers=test_user_jwt,
    )
    assert response_2.status_code == HTTPStatus.OK
    assert response_2.json["id"] == response_1.json["id"]
    assert response_2.json["title"] == "title2"
    assert response_2.json["body"] == "body2"


def test_update_nonexisting_note(client):
    """
    A request to update a nonexisting note yields 404 error.
    """
    response = client.put(
        f"/note/0", json={"title": "title2", "body": "body2"}, headers=test_user_jwt
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_invalid_update_request(client):
    """
    Aa update note request with invalid data yields 422 error.
    """
    response = client.put("/note/0", json={}, headers=test_user_jwt)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


def test_update_other_user_note(client):
    """
    A request to update an other user's note yields 404 error.
    """
    response = make_post_note_request(client)
    check_response(response, HTTPStatus.CREATED)
    response = client.get(
        f"/note/{response.json['id']}",
        json={"title": "title2", "body": "body2"},
        headers=other_user_jwt,
    )
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_note(client):
    """
    A note can be deleted from the database using a delete request to the /note/<note_id> endpoint.
    A deleted node id, title and body is returned in response.
    """
    response = make_post_note_request(client)
    check_response(response, HTTPStatus.CREATED)
    response = client.delete(f"/note/{response.json['id']}", headers=test_user_jwt)
    check_response(response, HTTPStatus.OK)


def test_delete_nonexisting_note(client):
    """
    A request to delete a nonexisting note yields 404 error.
    """
    response = client.delete(f"/note/0", headers=test_user_jwt)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_delete_other_user_note(client):
    """
    A request to delete an other user's note yields 404 error.
    """
    response = make_post_note_request(client)
    check_response(response, HTTPStatus.CREATED)
    response = client.delete(f"/note/{response.json['id']}", headers=other_user_jwt)
    assert response.status_code == HTTPStatus.NOT_FOUND


def test_get_all_notes(client):
    """
    All user's notes can be retrieved using a get request to the /note endpoint.
    """
    response_1 = make_post_note_request(client)
    check_response(response_1, HTTPStatus.CREATED)
    response_2 = make_post_note_request(client)
    check_response(response_2, HTTPStatus.CREATED)
    # other user's note should not be included in the get all notes response of the test_user
    response_3 = client.post(
        "/note", json={"title": "title", "body": "body"}, headers=other_user_jwt
    )
    check_response(response_3, HTTPStatus.CREATED)
    response_4 = client.get("/note", headers=test_user_jwt)
    assert response_4.status_code == HTTPStatus.OK
    assert len(response_4.json) == 2
    assert response_4.json[0] == response_1.json
    assert response_4.json[1] == response_2.json
