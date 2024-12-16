from flask import Flask
from flask_pymongo import PyMongo

# Inicializa la variable mongo para que sea accesible globalmente
mongo = PyMongo()


def create_app():
    app = Flask(__name__)

    # Configuración de la URI de MongoDB Atlas
    app.config["MONGO_URI"] = (
        "mongodb+srv://brayangarzondev:WsYi8WI0cZsgeha6@chatbotbd.rko8t.mongodb.net/?retryWrites=true&w=majority&appName=ChatBotBD"
    )

    # Inicializa PyMongo con la aplicación
    mongo.init_app(app)

    # Importar y registrar las rutas
    from .routes import main

    app.register_blueprint(main)

    return app
