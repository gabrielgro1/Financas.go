from werkzeug.security import generate_password_hash

from app.repositories.usuario_repository import (
    criar_usuario_no_banco,
    buscar_usuario_por_email
)
from app.validators.usuario_validator import validar_dados_usuario

def criar_usuario(dados):
    erro, usuario_validado = validar_dados_usuario(dados)

    if erro:
        return erro, None
    
    usuario_existente = buscar_usuario_por_email(usuario_validado["email"])
    
    if usuario_existente is not None:
        return {"erro": "email ja cadastrado"}, None
    
    senha_hash = generate_password_hash(usuario_validado["senha"])

    usuario = criar_usuario_no_banco(
        usuario_validado=usuario_validado,
        senha_hash=senha_hash
    )

    return None, usuario