from werkzeug.security import check_password_hash

from app.repositories.usuario_repository import buscar_usuario_com_senha_por_email
from app.security import gerar_token
from app.validators.auth_validator import validar_dados_login

def fazer_login(dados):
    erro, login_validado = validar_dados_login(dados)

    if erro:
        return erro, None

    usuario = buscar_usuario_com_senha_por_email(login_validado["email"])

    if usuario is None:
        return {"erro": "email ou senha invalidos"}, None

    senha_correta = check_password_hash(
        usuario["senha_hash"],
        login_validado["senha"]
    )

    if not senha_correta:
        return {"erro": "email ou senha invalidos"}, None

    token = gerar_token(usuario["id"])

    return None, {
        "token": token,
        "usuario": {
            "id": usuario["id"],
            "nome": usuario["nome"],
            "email": usuario["email"]
        }
    }