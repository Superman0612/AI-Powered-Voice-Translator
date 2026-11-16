import uuid
from fastapi import status

def test_user_registration(client):
    unique_user = f"user_{uuid.uuid4().hex[:8]}"
    email = f"{unique_user}@example.com"
    payload = {
        "email": email,
        "username": unique_user,
        "password": "StrongPassword123!",
        "full_name": "Test Engineer"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == email
    assert data["username"] == unique_user
    assert "hashed_password" not in data
    assert "id" in data

def test_duplicate_email_registration_fails(client):
    payload = {
        "email": "shubhamdevatwal2121@gmail.com",
        "username": f"admin_dup_{uuid.uuid4().hex[:4]}",
        "password": "Password123!"
    }
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in response.json()["detail"].lower()

def test_login_success(client):
    payload = {
        "email": "shubhamdevatwal2121@gmail.com",
        "password": "Shubham@404"
    }
    response = client.post("/api/v1/auth/login/json", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_password(client):
    payload = {
        "email": "shubhamdevatwal2121@gmail.com",
        "password": "WrongPassword123"
    }
    response = client.post("/api/v1/auth/login/json", json=payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_get_current_user_profile(client, auth_headers):
    response = client.get("/api/v1/auth/me", headers=auth_headers)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["username"] == "mca_student"
    assert data["is_active"] is True

def test_unauthenticated_request_rejected(client):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

