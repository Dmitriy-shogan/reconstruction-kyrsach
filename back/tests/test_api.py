import pytest
from unittest.mock import patch
from auth import create_jwt_token, hash_password

DEFAULT_USER_MOCK = (1, "testuser", "STUDENT", "Test User", "test@example.com", "Group-1")

@pytest.mark.asyncio
async def test_register_success(client, mock_db):
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.side_effect = [None, (1,)]
    
    response = await client.post("/api/auth/register", json={
        "login": "testuser",
        "password": "password123",
        "full_name": "Test User",
        "email": "test@example.com",
        "group_name": "Group-1"
    })
    
    assert response.status_code == 201
    assert response.json()["user_id"] == 1

@pytest.mark.asyncio
async def test_register_existing_user(client, mock_db):
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = (1,)
    
    response = await client.post("/api/auth/register", json={
        "login": "existinguser",
        "password": "password123",
        "full_name": "Test User",
        "email": "test@example.com",
        "group_name": "Group-1"
    })
    
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_success(client, mock_db):
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = (1, hash_password("password123"), "STUDENT")
    
    response = await client.post("/api/auth/login", json={
        "login": "testuser",
        "password": "password123"
    })
    
    assert response.status_code == 200
    assert "access_token" in response.json()

@pytest.mark.asyncio
async def test_login_invalid(client, mock_db):
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = None
    
    response = await client.post("/api/auth/login", json={
        "login": "wronguser",
        "password": "wrongpassword"
    })
    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_get_me(client, mock_db):
    token = create_jwt_token(1, "STUDENT")
    headers = {"Authorization": f"Bearer {token}"}
    
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = DEFAULT_USER_MOCK
    
    response = await client.get("/api/users/me", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["login"] == "testuser"

@pytest.mark.asyncio
async def test_update_me(client, mock_db):
    token = create_jwt_token(1, "STUDENT")
    headers = {"Authorization": f"Bearer {token}"}
    
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.side_effect = [
        DEFAULT_USER_MOCK, 
        (1, "testuser", "STUDENT", "Updated Name", "test@example.com", "Group-2")
    ]
    
    response = await client.patch("/api/users/me", headers=headers, json={
        "full_name": "Updated Name",
        "group_name": "Group-2"
    })
    
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"

@pytest.mark.asyncio
async def test_get_projects(client, mock_db):
    token = create_jwt_token(1, "STUDENT")
    headers = {"Authorization": f"Bearer {token}"}
    
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = DEFAULT_USER_MOCK
    mock_cursor.fetchall.return_value = [(1, "test.zip", "DONE", "2023-10-10T10:00:00")]
    
    response = await client.get("/api/projects/", headers=headers)
    
    assert response.status_code == 200
    assert len(response.json()) == 1

@pytest.mark.asyncio
async def test_create_project(client, mock_db):
    token = create_jwt_token(1, "STUDENT")
    headers = {"Authorization": f"Bearer {token}"}
    
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.side_effect = [DEFAULT_USER_MOCK, (1,)]
    
    files = {"file": ("test.zip", b"fake zip content", "application/zip")}
    
    with patch('routers.projects.asyncio.create_task') as mock_task:
        response = await client.post("/api/projects/", files=files, headers=headers)
        
    assert response.status_code == 201
    assert response.json()["project_id"] == 1
    mock_task.assert_called_once()

@pytest.mark.asyncio
async def test_create_project_invalid_extension(client, mock_db):
    token = create_jwt_token(1, "STUDENT")
    headers = {"Authorization": f"Bearer {token}"}
    
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = DEFAULT_USER_MOCK
    
    files = {"file": ("test.txt", b"fake text content", "text/plain")}
    
    response = await client.post("/api/projects/", files=files, headers=headers)
    
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_get_news(client, mock_db):
    token = create_jwt_token(1, "STUDENT")
    headers = {"Authorization": f"Bearer {token}"}
    
    mock_cursor, mock_conn = mock_db
    mock_cursor.fetchone.return_value = DEFAULT_USER_MOCK
    mock_cursor.fetchall.return_value = [(1, "News Title", "News Content", "2023-10-10T10:00:00")]
    
    response = await client.get("/api/news/", headers=headers)
    
    assert response.status_code == 200
    assert len(response.json()) == 1