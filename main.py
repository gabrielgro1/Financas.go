from flask import Flask
import os
from app.routes.transacoes import transacoes_bp
from app.errors import registrar_error_handlers
from app.routes.usuarios import usuario_bp
from app.routes.categorias import categorias_bp
from app.routes.auth import auth_bp


app = Flask(__name__)

registrar_error_handlers(app)

app.register_blueprint(auth_bp)
app.register_blueprint(usuario_bp)
app.register_blueprint(transacoes_bp)
app.register_blueprint(categorias_bp)

if __name__ == "__main__":
    app.run(
        port=int(os.getenv("PORT", 8000)),
        debug=os.getenv("DEBUG") == "1",
    )
