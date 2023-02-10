def test_get_motorista(client):
    response = client.get("/motorista?cpf=22222222222")
    assert response.status_code == 200


def test_get_motorista_not_found(client):
    response = client.get("/motorista?cpf=00000000000")
    assert response.status_code == 404


def test_get_motoristas(client):
    response = client.get("/motorista")
    assert response.status_code == 200
