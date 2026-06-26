from app.database import conectar_banco


def buscar_transacao_no_banco(transacao_id, usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute(
        """
        SELECT id, usuario_id, categoria_id, tipo, valor, descricao, data, criado_em
        FROM transacoes
        WHERE id = %s AND usuario_id = %s;
    """,
    (transacao_id, usuario_id)
    )

    transacao = cursor.fetchone()

    cursor.close()
    conexao.close()

    if transacao is None:
        return None

    return formatar_transacao_banco(transacao)


def formatar_transacao_banco(transacao):
    return {
        "id": transacao[0],
        "usuario_id": transacao[1],
        "categoria_id": transacao[2],
        "tipo": transacao[3],
        "valor": float(transacao[4]),
        "descricao": transacao[5],
        "data": transacao[6].isoformat(),
        "criado_em": transacao[7].isoformat(),
    }


def editar_transacao_no_banco(transacao_id, usuario_id, transacao_validada):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        UPDATE transacoes
        SET tipo = %s,
            valor = %s,
            descricao = %s
        WHERE id = %s AND usuario_id = %s
        RETURNING id, usuario_id, categoria_id, tipo, valor, descricao, data, criado_em;
        """,
        (
            transacao_validada["tipo"],
            transacao_validada["valor"],
            transacao_validada["descricao"],
            transacao_id,
            usuario_id,
        )
    )

    transacao = cursor.fetchone()
    conexao.commit()

    cursor.close()
    conexao.close()

    if transacao is None:
        return None
    return formatar_transacao_banco(transacao)

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

    return formatar_transacao_banco(transacao)

def listar_transacoes_do_banco(usuario_id, tipo=None, valor_minimo=None):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    sql = """
        SELECT id, usuario_id, categoria_id, tipo, valor, descricao, data, criado_em
        FROM transacoes
        WHERE usuario_id = %s

"""
    parametros = [usuario_id]

    if tipo is not None:
        sql += " AND tipo = %s"
        parametros.append(tipo)

    if valor_minimo is not None:
        sql += " AND valor >= %s"
        parametros.append(valor_minimo)

    sql += " ORDER BY data DESC"

    cursor.execute(sql, parametros)
    transacoes_banco = cursor.fetchall()

    cursor.close()
    conexao.close()

    resultado = []

    for transacao in transacoes_banco:
        resultado.append(formatar_transacao_banco(transacao))

    return resultado
def deletar_transacao_no_banco(transacao_id, usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        DELETE FROM transacoes
        WHERE id= %s AND usuario_id = %s
        RETURNING id, usuario_id, categoria_id, tipo, valor, descricao, data, criado_em;
        """,
        (transacao_id, usuario_id)
    )
    
    transacao = cursor.fetchone()
    conexao.commit()
    
    cursor.close()
    conexao.close()

    if transacao is None:
        return None
    return formatar_transacao_banco(transacao)
def obter_resumo_do_banco(usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT
            COALESCE(SUM(CASE WHEN tipo = 'receita' THEN valor ELSE 0 END), 0) AS total_receitas,
            COALESCE(SUM(CASE WHEN tipo = 'despesa' THEN valor ELSE 0 END), 0) AS total_despesas
        FROM transacoes
        WHERE usuario_id = %s;
        """,
        (usuario_id,)
    )
    
    total_receitas, total_despesas = cursor.fetchone()
    saldo = total_receitas - total_despesas
    
    cursor.close()
    conexao.close()

    return {
        "total_receitas": float(total_receitas),
        "total_despesas": float(total_despesas),
        "saldo": float(saldo),
    }
    