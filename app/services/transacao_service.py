from app.repositories.transacao_repository import (
    buscar_transacao_no_banco,
    criar_transacao_no_banco,
    deletar_transacao_no_banco,
    editar_transacao_no_banco,
    listar_transacoes_do_banco,
    obter_resumo_do_banco,
)
from app.validators.transacao_validator import validar_dados_transacao
from app.repositories.categoria_repository import categoria_existe_no_banco

def criar_transacao(dados, usuario_id):
    erro, transacao_validada = validar_dados_transacao(dados)

    if erro:
        return erro, None

    if not categoria_existe_no_banco(transacao_validada["categoria_id"], usuario_id):
        return {"erro": "categoria nao encontrada"}, None
    
    transacao = criar_transacao_no_banco(
        transacao_validada=transacao_validada,
        usuario_id=usuario_id,
        categoria_id=transacao_validada["categoria_id"]
    )

    return None, transacao

def editar_transacao(transacao_id, dados, usuario_id):
    erro, transacao_validada = validar_dados_transacao(dados)

    if erro:
        return erro, None
    
    if not categoria_existe_no_banco(transacao_validada["categoria_id"], usuario_id):
        return {"erro": "categoria nao encontrada"}, None


    transacao = editar_transacao_no_banco(
        transacao_id=transacao_id,
        usuario_id=usuario_id,
        transacao_validada=transacao_validada
    )

    return None, transacao

def listar_transacoes(usuario_id, tipo=None, valor_minimo=None):
    if tipo is not None and tipo not in ["receita", "despesa"]:
        return {"erro": "tipo deve ser receita ou despesa"}, None
    if valor_minimo is not None:
        try:
            valor_minimo = float(valor_minimo)
        except ValueError:
            return {"erro": "valor_minimo deve ser numero"}, None

    transacoes = listar_transacoes_do_banco(
        usuario_id=usuario_id,
        tipo=tipo,
        valor_minimo=valor_minimo
    )

    return None, transacoes


def buscar_transacao(transacao_id, usuario_id):
    transacao = buscar_transacao_no_banco(
        transacao_id=transacao_id,
        usuario_id=usuario_id
    )

    return None, transacao


def deletar_transacao(transacao_id, usuario_id):
    transacao = deletar_transacao_no_banco(
        transacao_id=transacao_id,
        usuario_id=usuario_id
    )

    return None, transacao


def obter_resumo(usuario_id):
    resumo = obter_resumo_do_banco(usuario_id=usuario_id)

    return None, resumo

