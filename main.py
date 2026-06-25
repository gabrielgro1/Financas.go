from flask import Flask, jsonify, request
from dotenv import load_dotenv
import os
import psycopg2

app = Flask(__name__)

transacoes = []
load_dotenv()

def conectar_banco():
    database_url = os.getenv("DATABASE_URL")

    if database_url is None:
        raise RuntimeError("DATABASE_URL nao configurada")
    
    return psycopg2.connect(database_url)

def validar_dados_transacao(dados):
    tipo = dados.get("tipo")
    valor = dados.get("valor")
    descricao = dados.get("descricao")

    if tipo not in ["receita", "despesa"]:
        return {"erro": "tipo deve ser receita ou despesa"}, None

    if valor is None:
        return {"erro": "valor obrigatorio"}, None

    if valor <= 0:
        return {"erro": "valor deve ser maior que zero"}, None

    if not descricao:
        return {"erro": "descricao obrigatoria"}, None

    transacao_validada = {
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao
    }

    return None, transacao_validada

def buscar_transacao_por_id(transacao_id):
    for transacao in transacoes:
        if transacao["id"] == transacao_id:
            return transacao

    return None
def criar_transacao_no_banco(transacao_validada, usuario_id, categoria_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO transacoes (usuario_id, categoria_id, tipo, valor, descricao)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING id, usuario_id, categoria_id, tipo, valor, descricao, data, criado_em;
        """,
        (
            usuario_id,
            categoria_id,
            transacao_validada["tipo"],
            transacao_validada["valor"],
            transacao_validada["descricao"],
        )
    )
    transacao = cursor.fetchone()
    conexao.commit()

    cursor.close()
    conexao.close()

    return {
        "id": transacao[0],
        "usuario_id": transacao[1],
        "categoria_id": transacao[2],
        "tipo": transacao[3],
        "valor":float(transacao[4]),
        "descricao": transacao[5],
        "data": transacao[6].isoformat(),
        "criado_em": transacao[7].isoformat(),
    }



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

    nova_transacao = {
        "id": len(transacoes) + 1,
        "tipo": transacao_validada["tipo"],
        "valor": transacao_validada["valor"],
        "descricao": transacao_validada["descricao"],
    }

    transacoes.append(nova_transacao)

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
    
    transacoes_filtradas = []

    for transacao in transacoes:
        if tipo is not None and transacao["tipo"] != tipo:
            continue
        if valor_minimo is not None and transacao["valor"] < valor_minimo:
            continue
    
        transacoes_filtradas.append(transacao)
    return jsonify({"transacoes": transacoes_filtradas}),200

@app.get("/transacoes/<int:transacao_id>")
def buscar_transacao(transacao_id):
    transacao = buscar_transacao_por_id(transacao_id)

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    return jsonify({"transacao": transacao}), 200


@app.delete("/transacoes/<int:transacao_id>")
def deletar_transacao(transacao_id):
    transacao = buscar_transacao_por_id(transacao_id)

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    transacoes.remove(transacao)

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
    transacao = buscar_transacao_por_id(transacao_id)

    if transacao is None:
        return jsonify({"erro": "transacao nao encontrada"}), 404

    transacao["tipo"] = transacao_validada["tipo"]
    transacao["valor"] = transacao_validada["valor"]
    transacao["descricao"] = transacao_validada["descricao"]

    return jsonify({
                "mensagem": "transacao atualizada",
                "transacao": transacao
            }), 200



@app.get("/resumo")
def obter_resumo():
    total_receitas = 0
    total_despesas = 0

    for transacao in transacoes:
        if transacao["tipo"] == "receita":
            total_receitas += transacao["valor"]

        if transacao["tipo"] == "despesa":
            total_despesas += transacao["valor"]

    saldo = total_receitas - total_despesas


    return jsonify({
        "total_receitas": total_receitas,
        "total_despesas": total_despesas,
        "saldo": saldo
    }), 200




if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    app.run(port=port, debug=True)
