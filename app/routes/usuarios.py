from flask import Blueprint, jsonify, request

from app.services.usuario_service import criar_usuario as criar_usuario_service

usuario_bp = Blueprint("usuarios", __name__)

@usuario_bp.post("/usuarios")
def criar_usuario():
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400
    
    erro, usuario = criar_usuario_service(dados)

    if erro:
        return jsonify(erro), 400
    
    return jsonify({
        "mensagem": "usuario criado",
        "usuario": usuario
    }), 201