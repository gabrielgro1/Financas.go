import os
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from dotenv import load_dotenv
from flask import jsonify, request

load_dotenv()

def gerar_token(usuario_id):
    secret_key = os.getenv("SECRET_KEY")

    if secret_key is None:
        raise RuntimeError("SECRET_KEY nao configurada")

    payload = {
        "usuario_id": usuario_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }

    return jwt.encode(payload, secret_key, algorithm="HS256")

def obter_usuario_id_do_token():
    secret_key = os.getenv("SECRET_KEY")
    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return {"erro": "token nao enviado"}, None

    partes = auth_header.split()

    if len(partes) != 2 or partes[0].lower() != "bearer":
        return {"erro":"token invalido"}, None

    try:
        payload = jwt.decode(partes[1], secret_key, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return {"erro": "token expirado"}, None
    except jwt.InvalidTokenError:
        return {"erro": "token invalido"}, None

    return None, payload["usuario_id"]

def login_obrigatorio(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        erro, usuario_id = obter_usuario_id_do_token()

        if erro:
            return jsonify(erro), 401

        return func(*args, usuario_id=usuario_id, **kwargs)

    return wrapper


