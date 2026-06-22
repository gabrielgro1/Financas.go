from flask import Flask, jsonify, request

app = Flask(__name__)

transacoes = []


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
        return jsonify({"erro": "envie um Json valido"}), 400

    tipo = dados.get("tipo")
    valor = dados.get("valor")
    descricao = dados.get("descricao")

    if tipo not in ["receita", "despesa"]:
        return jsonify({"erro": "tipo deve ser receita ou despesa"}), 400

    if valor is None:
        return jsonify({"erro": "valor obrigatorio"}), 400

    if valor <= 0:
        return jsonify({"erro": "valor deve ser maior que zero"}), 400

    if not descricao:
        return jsonify({"erro": "descricao obrigatoria"}), 400

    nova_transacao = {
        "id": len(transacoes) + 1,
        "tipo": tipo,
        "valor": valor,
        "descricao": descricao,
    }
    
    transacoes.append(nova_transacao)
    
    return jsonify({
        "mensagem": "transacao criada",
        "transacao": nova_transacao
    
    }), 201

@app.get("/transacoes")

def listar_transacoes():
    return jsonify({"transacoes": transacoes}), 200

@app.get("/transacoes/<int:transacao_id>")

def buscar_transacao(transacao_id):
    for transacao in transacoes:
        if transacao["id"] == transacao_id:
            return jsonify({"transacao": transacao}), 200
        
    return jsonify({"erro": "transacao nao encontrada"}), 404

@app.delete("/transacoes/<int:transacao_id>")

def deletar_transacao(transacao_id):
    for transacao in transacoes:
        if transacao["id"] == transacao_id:
             transacoes.remove(transacao)
             return jsonify({"mensagem": "transacao removida"}), 200
    
    return jsonify({"erro": "transacao nao encontrada"}), 404



if __name__ == "__main__":
    app.run(port=8000, debug=True)
