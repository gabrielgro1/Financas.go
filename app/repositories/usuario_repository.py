from app.database import conectar_banco

def formatar_usuario_banco(usuario):
    return {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2],
        "criado_em": usuario[3].isoformat()
    }

def criar_usuario_no_banco(usuario_validado, senha_hash):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
    INSERT INTO usuarios (nome, email, senha_hash)
    VALUES (%s, %s, %s)
    RETURNING id, nome, email, criado_em;
        """,
    (
        usuario_validado["nome"],
        usuario_validado["email"],
        senha_hash,
    )
)

    usuario = cursor.fetchone()
    conexao.commit()

    cursor.close()
    conexao.close()

    return formatar_usuario_banco(usuario)

def buscar_usuario_por_email(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, nome, email, criado_em
        FROM usuarios
        WHERE email = %s;
        """,
        (email,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario is None:
        return None
    return formatar_usuario_banco(usuario)

def buscar_usuario_com_senha_por_email(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT id, nome, email, senha_hash, criado_em
        FROM usuarios
        WHERE email = %s;
        """,
        (email,)
    )

    usuario = cursor.fetchone()

    cursor.close()
    conexao.close()

    if usuario is None:
        return None

    return {
        "id": usuario[0],
        "nome": usuario[1],
        "email": usuario[2],
        "senha_hash": usuario[3],
        "criado_em": usuario[4].isoformat()
    }