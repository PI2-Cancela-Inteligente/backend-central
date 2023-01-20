def test_post_carro(client):
    response = client.post(
        "/carro",
        json={
            "placa": "AAA-0000",
            "modelo": "Gol",
            "marca": "Volkswagen",
            "ano": 2019,
            "cpf": "000.000.000-00",
        },
    )
    assert response.status_code == 200
