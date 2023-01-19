# backend-central
Repositório do projeto Cancela certa da disciplina de Projeto Integrador 2

### Instalação

1. Faça o clone do projeto:

```bash
git clone https://github.com/PI2-Cancela-Inteligente/backend-central
```
2. Entre no diretório do projeto
  
  ```bash
  cd backend-central
  ```

3. Instale o ambiente virtual para o projeto:

```bash
sudo apt install python3.10-venv
```

4. Crie o ambiente virtual:

```bash
python3 -m venv .venv
```

5. Ative o ambiente virtual:

(Linux, Mac)
```bash
source .venv/bin/activate
```

(Windows)
```bash
.venv\Scripts\activate
```

6. Instale as dependências do projeto:

```bash
pip install -r requirements.txt
```


## Operação

### Observações

* O projeto utiliza o docker para subir a base de dados, portanto, é necessário que o docker esteja instalado na máquina.
* O projeto utiliza o docker-compose para subir a base de dados, portanto, é necessário que o docker-compose esteja instalado na máquina.


## Execução
1- Para subir a base de dados o seguinte comando deve ser executado:

```bash
docker-compose up --build
```
2- Para ativar o ambiente os seguintes comandos devem ser executados:
```bash
python3 -m venv .venv
```
```bash
source .venv/bin/activate
```
3- Para rodar a aplicação:
```bash
uvicorn src.main:app --host 0.0.0.0 --port 5000
```

## Endpoints

Para visualizar os endpoints da API, execute o comando:

```shell
    http://0.0.0.0:5000/docs