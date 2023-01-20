def test_delete_motorista(client):
    response = client.delete("/motorista?cpf=11111111111")
    assert response.status_code == 200
    assert response.json() == {"message": "Motorista deletado com sucesso"}


def test_delete_motorista_not_found(client):
    response = client.delete("/motorista?cpf=00000000000")
    assert response.status_code == 200
    assert response.json() == {"message": "Motorista não encontrado"}
