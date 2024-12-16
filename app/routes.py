from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario  # Asegúrate de tener el modelo adecuado importado

main = Blueprint("main", __name__)

# Ruta GET que ya tienes
@main.route("/")
def index():
    return jsonify({"message": "¡Bienvenido a tu ChatBot con Flask y PostgreSQL!"})

# Ruta POST para recibir datos
@main.route("/add_usuario", methods=["POST"])
def add_usuario():
    # Obtener los datos enviados en la solicitud POST
    data = request.get_json()  # Obtiene los datos en formato JSON

    # Verificar si se recibieron los datos necesarios
    if "nombre" not in data:
        return jsonify({"error": "Falta el campo 'nombre'"}), 400

    # Crear un nuevo usuario (suponiendo que tu modelo tiene un campo 'nombre')
    nuevo_usuario = Usuario(nombre=data["nombre"])

    try:
        # Agregar el usuario a la base de datos
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Devolver una respuesta de éxito
        return jsonify({"message": "Usuario creado exitosamente", "id": nuevo_usuario.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
