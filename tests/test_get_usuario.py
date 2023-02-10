def test_get_usuario(client):
    response = client.get("/usuario?id_usuario=2")
    assert response.status_code == 200
