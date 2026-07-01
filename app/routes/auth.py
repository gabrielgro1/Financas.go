from flask import Blueprint, jsonify, request

from app.services.auth_service import fazer_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.post("/login")
def login():
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400

    erro, resultado = fazer_login(dados)

    if erro:
        status = 401 if erro["erro"] == "email ou senha invalidos" else 400
        return jsonify(erro), status

    return jsonify(resultado), 200