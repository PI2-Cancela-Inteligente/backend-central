def test_post_usuario(client):
    response = client.post(
        "/usuario",
        json={
            "email": "testepost@mail.com",
            "senha": "123456",
            "is_admin": False,
        },
    )
    assert response.status_code == 200


def test_post_usuario_com_cadastro(client):
    response = client.post(
        "/usuario",
        json={
            "email": "rodoupho@mail.com",
            "senha": "123456",
            "is_admin": False,
        },
    )
    assert response.status_code == 200
