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