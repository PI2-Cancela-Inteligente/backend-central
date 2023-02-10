def test_put_carro(client):
    response = client.put(
        "/carro?placa=HUA9876",
        json={
            "placa": "HUA9876",
            "cor": "Preto",
            "modelo": "Gol",
            "marca": "Volkswagen",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 200
