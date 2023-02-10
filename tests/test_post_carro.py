def test_post_carro(client):
    response = client.post(
        "/carro",
        json={
            "placa": "AAA-0000",
            "cor": "Preto",
            "modelo": "Gol",
            "marca": "Volkswagen",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 201


def test_post_carro_sem_cpf(client):
    response = client.post(
        "/carro",
        json={
            "placa": "AAA-0000",
            "cor": "Preto",
            "modelo": "Gol",
            "marca": "Volkswagen",
        },
    )
    assert response.status_code == 422


def test_post_carro_sem_placa(client):
    response = client.post(
        "/carro",
        json={
            "cor": "Preto",
            "modelo": "Gol",
            "marca": "Volkswagen",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 422


def test_post_carro_sem_cor(client):
    response = client.post(
        "/carro",
        json={
            "placa": "AAA-0000",
            "modelo": "Gol",
            "marca": "Volkswagen",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 422


def test_post_carro_sem_modelo(client):
    response = client.post(
        "/carro",
        json={
            "placa": "AAA-0000",
            "cor": "Preto",
            "marca": "Volkswagen",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 422


def test_post_carro_sem_marca(client):
    response = client.post(
        "/carro",
        json={
            "placa": "AAA-0000",
            "cor": "Preto",
            "modelo": "Gol",
            "cpf": "22222222222",
        },
    )
    assert response.status_code == 422
