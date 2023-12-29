from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
import datetime

#criação do banco de dados postgresql com docker

# docker run --name my_container -p 5434:5432 -e POSTGRES_USER=my_user -e POSTGRES_PASSWORD=my_user2023 -e POSTGRES_DB=my_db -d postgres:16.0

# Contantes para configurações do banco de dados
USER = 'my_user'
SECRET = 'my_user2023'
HOST = 'localhost' #seria o ip do banco de dados neste caso como é local é localhost.
DATABASE = 'my_db'
PORT = '5434' #porta padrão do postgresql é 5432 mas comos estamos usando o docker, foi alterado para 5434.

connection = f'postgresql+psycopg2://{USER}:{SECRET}@{HOST}:{PORT}/{DATABASE}' #string de conexão com o banco de dados.

engine = create_engine(connection, echo=True) #echo=True é para mostrar logs do que está acontecendo no banco de dados.
sesion = sessionmaker(bind=engine) #criando uma sessão com o banco de dados.

Base = declarative_base() #criando uma base para criar as tabelas.

class Cadastro_login(Base):
    __tablename__ = 'cadastro_login' #nome da tabela no banco de dados.
    id = Column(Integer, primary_key=True)
    nome = Column(String(100))
    email = Column(String(100))
    senha = Column(String(250))

class Tokens(Base):
    __tablename__ = 'tokens' #nome da tabela no banco de dados.
    id = Column(Integer, primary_key=True)
    token = Column(String(100))
    data_criacao = Column(DateTime, default=datetime.datetime.now())
    id_usuario = Column(Integer, ForeignKey('cadastro_login.id'))

Base.metadata.create_all(engine) #criando as tabelas no banco de dados.