def test_delete_usuario(client):
    response = client.delete("/usuario?id_usuario=1")
    assert response.status_code == 200
    assert response.json() == {"message": "Usuario deletado com sucesso"}


def test_delete_usuario_not_found(client):
    response = client.delete("/usuario?id_usuario=100")
    assert response.status_code == 404
    assert response.json() == {"message": "Usuario não encontrado"}
