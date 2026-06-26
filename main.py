from flask import Flask, jsonify, request
from app.validators.transacao_validator import validar_dados_transacao
from app.repositories.transacao_repository import (
    buscar_transacao_no_banco,
    criar_transacao_no_banco,
    deletar_transacao_no_banco,
    editar_transacao_no_banco,
    listar_transacoes_do_banco,
    obter_resumo_do_banco,
)

import os


app = Flask(__name__)


@app.get("/ping")
def ping():
    return jsonify({"status": "ok"})

@app.post("/echo")
def echo():
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON válido"}), 400

    return jsonify(dados), 200


@app.post("/transacoes")
def criar_transacao():
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400

    erro, transacao_validada = validar_dados_transacao(dados)

    if erro:
        return jsonify(erro), 400
    
    nova_transacao = criar_transacao_no_banco(
        transacao_validada= transacao_validada,
        usuario_id=1,
        categoria_id=1
    )

    return jsonify({
        "mensagem": "transacao criada",
        "transacao": nova_transacao

    }), 201

@app.get("/transacoes")
def listar_transacoes():
    tipo = request.args.get("tipo")
    valor_minimo = request.args.get("valor_minimo")

    if tipo is not None and tipo not in ["receita", "despesa"]:
        return jsonify({"erro": "tipo deve ser receita ou despesa"}), 400

    if valor_minimo is not None:
        try:
            valor_minimo = float(valor_minimo)
        except ValueError:
            return jsonify({"erro": "valor_minimo deve ser numero"}), 400
    
    transacoes_banco = listar_transacoes_do_banco(
        usuario_id=1,
        tipo=tipo,
        valor_minimo=valor_minimo
    )

    return jsonify({"transacoes": transacoes_banco}),200

@app.get("/transacoes/<int:transacao_id>")
def buscar_transacao(transacao_id):
    transacao = buscar_transacao_no_banco(
        transacao_id=transacao_id,
        usuario_id=1
    )

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    return jsonify({"transacao": transacao}), 200


@app.delete("/transacoes/<int:transacao_id>")
def deletar_transacao(transacao_id):
    transacao = deletar_transacao_no_banco(
        transacao_id=transacao_id,
        usuario_id=1
    )

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404


    return jsonify({"mensagem": "transacao removida",
                    "transacao": transacao
                    }), 200


@app.put("/transacoes/<int:transacao_id>")
def editar_transacao(transacao_id):
    dados = request.get_json(silent=True)

    if dados is None:
        return jsonify({"erro": "envie um JSON valido"}), 400

    erro, transacao_validada = validar_dados_transacao(dados)
    if erro:
        return jsonify(erro), 400

    transacao = editar_transacao_no_banco(
        transacao_id=transacao_id,
        usuario_id=1,
        transacao_validada=transacao_validada
    )

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    return jsonify({
        "mensagem": "transacao atualizada",
        "transacao": transacao
    }), 200



@app.get("/resumo")
def obter_resumo():
    resumo = obter_resumo_do_banco(usuario_id=1)

    return jsonify(resumo), 200




if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(port=port, debug=True)
