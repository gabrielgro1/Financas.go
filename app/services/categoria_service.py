from app.repositories.categoria_repository import(
    criar_categoria_no_banco,
    listar_categorias_do_banco,
)
from app.validators.categoria_validator import validar_dados_categoria

def criar_categoria(dados, usuario_id):
    erro, categoria_validada = validar_dados_categoria(dados)

    if erro:
        return erro, None

    categoria = criar_categoria_no_banco(
        categoria_validada=categoria_validada,
        usuario_id=usuario_id
    )

    return None, categoria

def listar_categorias(usuario_id):
    categorias = listar_categorias_do_banco(usuario_id=usuario_id)

    return None, categorias

