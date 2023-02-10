# def test_estaciona(client):
#     response = client.post(
#         "/estaciona",
#         json={"placa": "KEE0987"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {"message": "Estacionamento Entrada Registrada"}


# def test_estaciona_not_found(client):
#     response = client.post(
#         "/estaciona",
#         json={"placa": "AAA-9999"},
#     )
#     assert response.status_code == 200
#     assert response.json() == {"message": "Carro não encontrado"}
