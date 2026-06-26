import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

def conectar_banco():
    database_url = os.getenv("DATABASE_URL")

    if database_url is None:
        raise RuntimeError("DATABASE_URL nao configurada")
    
    return psycopg2.connect(database_url)