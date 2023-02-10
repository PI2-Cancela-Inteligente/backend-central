def test_put_usuario(client):
    response = client.put(
        "/usuario?id_usuario=2",
        json={
            "email": "baodemais@mail.com",
            "senha": "123456",
            "is_admin": False,
        },
    )
    assert response.status_code == 200


def test_put_usuario_not_found(client):
    response = client.put(
        "/usuario?id_usuario=100",
        json={
            "email": "notfoun@mail.com",
            "senha": "123456",
            "is_admin": False,
        },
    )
    assert response.status_code == 404
