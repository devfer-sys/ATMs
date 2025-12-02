from flask import Flask

def create_app():
    app = Flask(__name__)

    # Importar controladores y registrar rutas
    from .controllers import main
    app.register_blueprint(main)

    return app
