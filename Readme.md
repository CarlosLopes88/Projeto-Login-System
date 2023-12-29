## Descrição

Neste projeto desenvolvido e liguagem de programação python, buscou-se criar um sistemas de login integrado ao banco de dados via ORM, onde para cadastrarmos os usuários e realizarmos os logins estamos utilizando o framewor FastAPI para realizar as chamadas.

Esse projeto utiliza o framework Python, FastAPI, SQLAlchemy, Uvicorn, Psycopg2, Docker e Postgres para o seu desenvolvimento.

## Estrutura do Projeto
- **models:** Contém as classes de modelo para representar as entidades do sistema;
- **api:** É o script que contém os endpoints da API realiza a criptografia das senhas e as validações dos parametros passados;
- **requirements:** Contém os pacotes instalados dentro da virtual env;
- **README.md:** Este arquivo.

## Execução do projeto

Para inicializar o projeto temos os seguintes passos:

- **Criação do banco de dados localmente:** docker run --name my_container -p 5434:5432 -e POSTGRES_USER=my_user -e POSTGRES_PASSWORD=my_user2023 -e POSTGRES_DB=my_db -d postgres:16.0 (Lembre-se de instalar o docker em sua máquina)

- **Criação do ambiente virtual:** 

    - python -m venv .venv (windows)
    - Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    - .\.venv\Scripts\activate

- **Executar os arquivos:**

    - Comando model: python model.py

    - Comando para executar o servidor das APIs: uvicorn api:app --reload