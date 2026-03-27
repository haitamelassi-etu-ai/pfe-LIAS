def register(client, email: str, role: str = "member", password: str = "Pass@1234"):
    return client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "first_name": "Test",
            "last_name": "User",
            "role": role,
        },
    )


def login(client, email: str, password: str = "Pass@1234"):
    return client.post(
        "/api/auth/login",
        data={"username": email, "password": password},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )


def test_document_upload_and_listing(client):
    register(client, "docmember@example.com")
    auth = login(client, "docmember@example.com")
    token = auth.json()["access_token"]

    upload = client.post(
        "/api/documents/upload",
        headers={"Authorization": f"Bearer {token}"},
        files={"upload": ("sample.txt", b"hello lias", "text/plain")},
    )
    assert upload.status_code == 200
    doc_id = upload.json()["id"]

    listed = client.get("/api/documents/my", headers={"Authorization": f"Bearer {token}"})
    assert listed.status_code == 200
    assert len(listed.json()) == 1

    downloaded = client.get(
        f"/api/documents/{doc_id}/download",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert downloaded.status_code == 200


def test_admin_pdf_export(client):
    register(client, "adminexport@example.com", role="admin")
    auth = login(client, "adminexport@example.com")
    token = auth.json()["access_token"]

    exported = client.get(
        "/api/exports/lab/summary.pdf",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert exported.status_code == 200
    assert exported.headers["content-type"].startswith("application/pdf")
