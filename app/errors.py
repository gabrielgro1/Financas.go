import psycopg2
from flask import jsonify


def registrar_error_handlers(app):
    @app.errorhandler(psycopg2.OperationalError)
    def tratar_erro_conexao_banco(erro):
        return jsonify({
            "erro": "erro ao conectar com o banco de dados"
        }), 503
    
    @app.errorhandler(psycopg2.Error)
    def tratar_erro_banco(erro):
        return jsonify({
            "erro": "erro interno no banco de dados"
        }), 500