def register(client, email: str, password: str = "Pass@1234"):
    return client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Test",
            "last_name": "User",
            "role": "member",
        },
    )


def login(client, email: str, password: str = "Pass@1234"):
    return client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def test_register_and_login_flow(client):
    reg = register(client, "membre1@example.com")
    assert reg.status_code == 200
    token = reg.json()["access_token"]
    assert token

    auth = login(client, "membre1@example.com")
    assert auth.status_code == 200
    assert auth.json().get("access_token")


def test_forgot_and_reset_password_flow(client):
    register(client, "membre2@example.com", "OldPass@123")

    forgot = client.post("/api/auth/forgot-password", json={"email": "membre2@example.com"})
    assert forgot.status_code == 200
    reset_token = forgot.json().get("reset_token")
    assert reset_token

    reset = client.post(
        "/api/auth/reset-password",
        json={"token": reset_token, "new_password": "NewPass@123"},
    )
    assert reset.status_code == 200

    auth = login(client, "membre2@example.com", "NewPass@123")
    assert auth.status_code == 200


def test_change_password_when_authenticated(client):
    register(client, "membre3@example.com", "StartPass@123")
    auth = login(client, "membre3@example.com", "StartPass@123")
    token = auth.json()["access_token"]

    response = client.post(
        "/api/auth/change-password",
        json={"current_password": "StartPass@123", "new_password": "UpdatedPass@123"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200

    auth_updated = login(client, "membre3@example.com", "UpdatedPass@123")
    assert auth_updated.status_code == 200
