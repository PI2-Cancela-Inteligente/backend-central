# backend-central
Repositório do projeto Cancela certa da disciplina de Projeto Integrador 2

## Execução

### Observações

* O projeto utiliza o docker para subir a base de dados, portanto, é necessário que o docker esteja instalado na máquina.
* O projeto utiliza o docker-compose para subir a base de dados, portanto, é necessário que o docker-compose esteja instalado na máquina.


## Execução
1- Para subir a base de dados e a aplicação, o seguinte comando deve ser executado:

```bash
docker-compose up --build
```
E acessar a url http://0.0.0.0:5000/docs

## Testes

Para executar os testes, execute o comando:

```bash
docker exec -it app pytest --cov -vv
```

## Endpoints

Para visualizar os endpoints da API, execute o comando:

```shell
    http://0.0.0.0:5000/docs