def test_get_carros(client):
    response = client.get("/carro")
    assert response.status_code == 200
