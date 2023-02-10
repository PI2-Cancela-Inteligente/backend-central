def test_delete_cartao(client):
    response = client.delete("/cartao?numero=1111111111111111")
    assert response.status_code == 200
    assert response.json() == {"message": "Cartão deletado"}


def test_delete_cartao_not_found(client):
    response = client.delete("/cartao?numero=0000000000000000")
    assert response.status_code == 404
    assert response.json() == {"message": "Cartão não encontrado"}
