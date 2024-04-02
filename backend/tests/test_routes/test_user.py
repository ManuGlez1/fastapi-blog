def test_create_user(client):
    data = {"email": "test@test.com", "password": "supersecret"}
    response = client.post("/users/", json = data)
    assert response.status_code == 201
    assert response.json()["email"] == "test@test.com"