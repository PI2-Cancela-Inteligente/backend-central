def test_put_motorista(client):
    response = client.put(
        "/motorista",
        json={
            "cpf": "11111111111",
            "nome": "Rodrigo",
            "email": "bigode@mail.com",
            "telefone": "00000000000",
            "senha": "123456",
            "matricula": "000000",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Motorista atualizado com sucesso"}


def test_put_motorista_not_found(client):
    response = client.put(
        "/motorista",
        json={
            "cpf": "00000000000",
            "nome": "Rodrigo",
            "email": "not@mail.com",
            "telefone": "00000000000",
            "senha": "123456",
            "matricula": "000000",
        },
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Motorista não encontrado"}
