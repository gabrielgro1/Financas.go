from flask import Blueprint, jsonify, request

from app.services.transacao_service import (
    criar_transacao as criar_transacao_service,
    editar_transacao as editar_transacao_service,
    buscar_transacao as buscar_transacao_service,
    deletar_transacao as deletar_transacao_service,
    obter_resumo as obter_resumo_service,
    listar_transacoes as listar_transacoes_service,
)

from app.security import login_obrigatorio

transacoes_bp = Blueprint("transacoes", __name__)

@transacoes_bp.get("/transacoes")
@login_obrigatorio
def listar_transacoes(usuario_id):
    tipo = request.args.get("tipo")
    valor_minimo = request.args.get("valor_minimo")

    erro, transacoes_banco = listar_transacoes_service(
        usuario_id=usuario_id,
        tipo=tipo,
        valor_minimo=valor_minimo
    )

    if erro:
        return jsonify(erro), 400

    return jsonify({"transacoes": transacoes_banco}), 200

@transacoes_bp.post("/transacoes")
@login_obrigatorio
def criar_transacao(usuario_id):
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400

    erro, transacao = criar_transacao_service(
        dados=dados,
        usuario_id=usuario_id
    )

    if erro:
        return jsonify(erro), 400

    return jsonify({
        "mensagem": "transacao criada",
        "transacao": transacao
    }), 201

@transacoes_bp.get("/transacoes/<int:transacao_id>")
@login_obrigatorio
def buscar_transacao(transacao_id, usuario_id):
    erro, transacao = buscar_transacao_service(
        transacao_id=transacao_id,
        usuario_id=usuario_id
    )

    if erro:
        return jsonify(erro), 400

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    return jsonify({"transacao": transacao}), 200



@transacoes_bp.delete("/transacoes/<int:transacao_id>")
@login_obrigatorio
def deletar_transacao(transacao_id, usuario_id):
    erro, transacao = deletar_transacao_service(
        transacao_id=transacao_id,
        usuario_id=usuario_id
    )

    if erro:
        return jsonify(erro), 400

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404


    return jsonify({"mensagem": "transacao removida",
                    "transacao": transacao
                    }), 200


@transacoes_bp.put("/transacoes/<int:transacao_id>")
@login_obrigatorio
def editar_transacao(transacao_id, usuario_id):
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400

    erro, transacao = editar_transacao_service(
        transacao_id=transacao_id,
        dados=dados,
        usuario_id=usuario_id
    )
    if erro:
        return jsonify(erro), 400

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    return jsonify({
        "mensagem": "transacao atualizada",
        "transacao": transacao
    }), 200


@transacoes_bp.get("/resumo")
@login_obrigatorio
def obter_resumo(usuario_id):
    erro, resumo = obter_resumo_service(usuario_id=usuario_id)

    if erro:
        return jsonify(erro), 400

    return jsonify(resumo), 200
