from flask import Blueprint, jsonify
from app import db
from models import Usuario  # Importa el modelo de usuario

main = Blueprint("main", __name__)

@main.route("/")
def index():
    return jsonify({"message": "¡Bienvenido a tu ChatBot con Flask y PostgreSQL!"})

@main.route("/data")
def get_data():
    # Accede a los datos de PostgreSQL usando SQLAlchemy
    usuario = Usuario.query.first()  # Obtén el primer usuario
    if usuario:
        return jsonify({"data": {"id": usuario.id, "nombre": usuario.nombre}})
    else:
        return jsonify({"data": "No hay datos"})
