def test_post_motorista_sem_cadastro(client):
    response = client.post(
        "/motorista",
        json={
            "cpf": "9827272726",
            "nome": "Teste",
            "email": "teste@mail.com",
            "telefone": "00000000000",
            "senha": "123456",
            "matricula": "000000",
        },
    )
    assert response.status_code == 500


def test_post_motorista_com_cadastro(client):
    response = client.post(
        "/motorista",
        json={
            "cpf": "332324234",
            "nome": "Teste",
            "email": "ceilandia@mail.com",
        },
    )
    assert response.status_code == 201
