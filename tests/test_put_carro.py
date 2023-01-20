def test_put_carro(client):
    response = client.put(
        "/carro?placa=RFS0D21",
        json={
            "placa": "RFS0D21",
            "cor": "Preto",
            "modelo": "Gol",
            "marca": "Volkswagen",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 200
