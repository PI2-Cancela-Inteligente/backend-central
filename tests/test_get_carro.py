def test_get_carros(client):
    response = client.get("/carro")
    assert response.status_code == 200


def test_get_carro(client):
    response = client.get("/carro?placa=KEE0987")
    assert response.status_code == 200
