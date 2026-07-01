from app.database import conectar_banco

def categoria_existe_no_banco(categoria_id, usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id
        FROM categorias
        WHERE id = %s AND usuario_id = %s;
        """,
        (categoria_id, usuario_id)
    )

    categoria = cursor.fetchone()

    cursor.close()
    conexao.close()

    return categoria is not None

def formatar_categoria_banco(categoria):
    return {
        "id": categoria[0],
        "nome": categoria[1],
        "usuario_id": categoria[2],
        "criado_em": categoria[3].isoformat()
    }


def criar_categoria_no_banco(categoria_validada, usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO categorias (nome, usuario_id)
        VALUES (%s, %s)
        RETURNING id, nome, usuario_id, criado_em;

        """,
        (
            categoria_validada["nome"],
            usuario_id,
        )
    )

    categoria = cursor.fetchone()
    conexao.commit()

    cursor.close()
    conexao.close()

    return formatar_categoria_banco(categoria)

def listar_categorias_do_banco(usuario_id):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, nome, usuario_id, criado_em
        FROM categorias
        WHERE usuario_id = %s
        ORDER BY nome ASC;
        """,
        (usuario_id,)
    )

    categoria_banco = cursor.fetchall()

    cursor.close()
    conexao.close()

    categorias = []

    for categoria in categoria_banco:
        categorias.append(formatar_categoria_banco(categoria))

    return categorias