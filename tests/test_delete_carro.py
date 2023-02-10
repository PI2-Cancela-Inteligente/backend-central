def test_delete_carro(client):
    response = client.delete("/carro?placa=RFS0D21")
    assert response.status_code == 200


def test_delete_carro_not_found(client):
    response = client.delete("/carro?placa=AAA-0000")
    assert response.status_code == 404
    assert response.json() == {"message": "Carro não encontrado"}
