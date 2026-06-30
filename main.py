from flask import Flask
from app.routes.transacoes import transacoes_bp
from app.errors import registrar_error_handlers
from app.routes.usuarios import usuario_bp

app = Flask(__name__)

registrar_error_handlers(app)

app.register_blueprint(usuario_bp)
app.register_blueprint(transacoes_bp)

if __name__ == "__main__":
    app.run(port=8000, debug=True)