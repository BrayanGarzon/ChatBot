from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

# Inicializa la base de datos
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la URI de PostgreSQL usando la variable de entorno
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')  # Obtener la URL de la variable de entorno
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva el seguimiento de modificaciones (no necesario)

    # Inicializa SQLAlchemy con la aplicación
    db.init_app(app)

    # Importar y registrar las rutas
    from .routes import main
    app.register_blueprint(main)

    return app



# from flask import Flask
# from flask_pymongo import PyMongo

# # Inicializa la variable mongo para que sea accesible globalmente
# mongo = PyMongo()


# def create_app():
#     app = Flask(__name__)

#     # Configuración de la URI de MongoDB Atlas
#     app.config["MONGO_URI"] = (
#         "mongodb+srv://brayangarzondev:WsYi8WI0cZsgeha6@chatbotbd.rko8t.mongodb.net/?retryWrites=true&w=majority&appName=ChatBotBD"
#     )

#     # Inicializa PyMongo con la aplicación
#     mongo.init_app(app)

#     # Importar y registrar las rutas
#     from .routes import main

#     app.register_blueprint(main)

#     return app
