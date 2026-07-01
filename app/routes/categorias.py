from flask import Blueprint, jsonify, request

from app.services.categoria_service import (
    criar_categoria as criar_categoria_service,
    listar_categorias as listar_categorias_service,
)

from app.security import login_obrigatorio

categorias_bp = Blueprint("categorias", __name__)

@categorias_bp.get("/categorias")
@login_obrigatorio
def listar_categorias(usuario_id):
    erro, categorias = listar_categorias_service(usuario_id=usuario_id)

    if erro:
        return jsonify(erro), 400

    return jsonify({"categorias": categorias}), 200

@categorias_bp.post("/categorias")
@login_obrigatorio
def criar_categoria(usuario_id):
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400

    erro, categoria = criar_categoria_service(
        dados=dados,
        usuario_id=usuario_id
    )

    if erro:
        return jsonify(erro), 400

    return jsonify({
        "mensagem": "categoria criada",
        "categoria": categoria
    }), 201