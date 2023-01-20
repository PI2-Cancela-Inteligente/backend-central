def test_post_motorista_sem_cadastro(client):
    response = client.post(
        "/motorista",
        json={
            "cpf": "00000000000",
            "nome": "Teste",
            "email": "teste@mail.com",
            "telefone": "00000000000",
            "senha": "123456",
            "matricula": "000000",
        },
    )
    assert response.status_code == 200


def test_post_motorista_com_cadastro(client):
    response = client.post(
        "/motorista",
        json={
            "cpf": "11111111111",
            "nome": "Teste",
            "email": "crocs@mail.com",
        },
    )
    assert response.status_code == 200
