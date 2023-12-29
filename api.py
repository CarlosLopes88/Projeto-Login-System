from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from model import USER, SECRET, HOST, DATABASE, PORT, connection, Cadastro_login, Tokens
from secrets import token_hex
import re
import hashlib

app = FastAPI()

def conectar_db():
    engine = create_engine(connection, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

@app.post('/cadastro')
def cadastrar_usuario(nome: str, email: str, senha: str):
    try:
        with conectar_db() as session:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()

            usuario_existente = session.query(Cadastro_login).filter_by(email=email, senha=senha_hash).first()

            if usuario_existente:
                return {'status': 'erro', 'mensagem': 'Usuário já cadastrado'}
            elif len(senha) < 10:
                return {'status': 'erro', 'mensagem': 'Senha deve ter no mínimo 10 caracteres'}
            elif len(nome) < 3:
                return {'status': 'erro', 'mensagem': 'Nome deve ter no mínimo 3 caracteres'}
            elif '@' not in email or '.' not in email or email.count('@') > 1 or email.count('.') > 1:
                return {'status': 'erro', 'mensagem': 'Email inválido'}
            elif not re.search(r"[A-Z]", senha):
                return {'status': 'erro', 'mensagem': 'A senha deve conter pelo menos uma letra maiúscula'}
            elif not re.search(r"[a-z]", senha):
                return {'status': 'erro', 'mensagem': 'A senha deve conter pelo menos uma letra minúscula'}
            elif not re.search(r"[0-9]", senha):
                return {'status': 'erro', 'mensagem': 'A senha deve conter pelo menos um número'}
            elif not re.search(r"[!@#$%^&*(),.?\":{}|<>]", senha):
                return {'status': 'erro', 'mensagem': 'A senha deve conter pelo menos um caractere especial'}
            else:
                usuario = Cadastro_login(nome=nome, email=email, senha=senha_hash)
                session.add(usuario)
                session.commit()
                return {'status': 'Usuário cadastrado com sucesso'}
    except Exception as e:
        return {'status': 'erro', 'mensagem': f'Erro no servidor: {str(e)}'}

@app.post('/login')
def login(email: str, senha: str):
    try:
        with conectar_db() as session:
            senha_hash = hashlib.sha256(senha.encode()).hexdigest()

            usuario = session.query(Cadastro_login).filter_by(email=email, senha=senha_hash).first()

            if usuario:
                token = token_hex(50)
                if session.query(Tokens).filter_by(id_usuario=usuario.id).first():
                    token_criado = session.query(Tokens).filter_by(id_usuario=usuario.id).first()
                    token_criado.token = token
                    session.commit()
                else:
                    token_criado = Tokens(token=token, id_usuario=usuario.id)
                    session.add(token_criado)
                    session.commit()
                return {'status': 'Login realizado com sucesso', 'token': token}
            else:
                return {'status': 'erro', 'mensagem': 'Email ou senha incorretos'}
    except Exception as e:
        return {'status': 'erro', 'mensagem': f'Erro no servidor: {str(e)}'}
