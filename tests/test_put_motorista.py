def test_put_motorista(client):
    response = client.put(
        "/motorista",
        json={
            "cpf": "33333333333",
            "nome": "Rodrigo",
            "email": "novoemail@mail",
            "telefone": "00000000000",
            "senha": "123456",
            "matricula": "000000",
        },
    )
    assert response.status_code == 422


def test_put_motorista_not_found(client):
    response = client.put(
        "/motorista",
        json={
            "cpf": "4444444444",
            "nome": "Rodrigo",
            "email": "not@mail.com",
            "telefone": "00000000000",
            "senha": "123456",
            "matricula": "000000",
        },
    )
    assert response.status_code == 422
