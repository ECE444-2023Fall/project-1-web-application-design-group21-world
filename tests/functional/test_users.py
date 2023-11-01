from flask import url_for

def test_user_insert(new_user, client):
    """Ensure that users can be added to User table"""
    test_user = dict(username=new_user.username, email=new_user.email)

    response = client.post(
        "/create",
        json=test_user, follow_redirects=True
    )
    assert response.status_code == 200
    assert f"{new_user.username}, {new_user.email}".encode('utf-8') in response.data

def test_get_users(client):
    response = client.get("/list")
    print(response.data)
    assert response.status_code == 200
    assert b"users are:" in response.data
