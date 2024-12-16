from flask import Flask, request, jsonify
import re, sys, os
from app import create_app
from flask_sqlalchemy import SQLAlchemy  # Necesario para trabajar con PostgreSQL


app = create_app()
db = SQLAlchemy(app)  # Instancia de SQLAlchemy para PostgreSQL

# Simulación de sesiones de usuarios
user_sessions = {}


# Función para validar correo electrónico
def validar_correo(email):
    patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(patron, email)


from app import db  # Usar SQLAlchemy de tu aplicación

# Asumiendo que tienes un modelo de base de datos definido para Usuario
from models import Usuario  # Importa el modelo que defina tu tabla de usuarios

def guardar_o_actualizar_usuario(
    user_id, nombre=None, cedula=None, telefono=None, email=None, interes=None
):
    try:
        # Verificar si el usuario ya existe en la base de datos
        usuario = Usuario.query.filter_by(id_usuario=user_id).first()

        if usuario:
            # Si el usuario existe, actualizar los campos
            if nombre:
                usuario.nombre = nombre
            if cedula:
                usuario.cedula = cedula
            if telefono:
                usuario.telefono = telefono
            if email:
                usuario.email = email
            if interes:
                usuario.interes = interes

            db.session.commit()  # Guardar los cambios en la base de datos

        else:
            # Si el usuario no existe, crear un nuevo registro
            nuevo_usuario = Usuario(
                id_usuario=user_id,
                nombre=nombre,
                cedula=cedula,
                telefono=telefono,
                email=email,
                interes=interes,
            )
            db.session.add(nuevo_usuario)
            db.session.commit()  # Guardar el nuevo registro

    except Exception as err:
        print(f"Error al guardar o actualizar el usuario: {err}")



@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()  # Capturar datos enviados en la solicitud
    message = data.get("message")
    user_id = data.get("userId")

    # Validar si no se proporcionaron los datos necesarios
    if not message or not user_id:
        return jsonify({"error": "Faltan datos: 'message' o 'userId'."}), 400

    # Inicializar la sesión del usuario si no existe
    if user_id not in user_sessions:
        user_sessions[user_id] = {"step": 0, "name": None}

    user_session = user_sessions[user_id]
    step = user_session["step"]

    # Lógica de conversación basada en pasos
    if step == 0:
        reply = "¡Hola Bienvenido a FreeCode! Escribe tu nombre completo 😊"
        user_session["step"] += 1

    elif step == 1:
        user_session["name"] = message  # Guardar el nombre del usuario en la sesión
        guardar_o_actualizar_usuario(user_id, nombre=message)  # Guardar en MongoDB
        reply = (
            f"Hola {user_session['name']}! Ingresa tu Identificación sin puntos 😀\n"
        )
        user_session["step"] += 1

    elif step == 2:
        if not message.isdigit():
            reply = "La identificación debe ser un número. Inténtalo nuevamente 📛."
        else:
            user_session["cedula"] = message  # Guardar en la sesión
            guardar_o_actualizar_usuario(user_id, cedula=message)  # Guardar en MongoDB
            reply = f"Ingresa un numero de telefono para poder contactarte 📱\n"
            user_session["step"] += 1

    elif step == 3:
        user_session["phone"] = message  # Guardar en la sesión
        guardar_o_actualizar_usuario(user_id, telefono=message)  # Guardar en MongoDB
        reply = "Ingresa tu correo electronico para poder contactarte 📧\n"
        user_session["step"] += 1

    elif step == 4:
        if not validar_correo(message):
            reply = "El correo electrónico no es válido. Por favor, ingrésalo correctamente 📧."
        else:
            user_session["email"] = message  # Guardar en la sesión
            guardar_o_actualizar_usuario(user_id, email=message)  # Guardar en MongoDB
            reply = "¡Listo! Tu información ha sido registrada 🎉\n\n¿En qué puedo ayudarte hoy?\nPor favor, selecciona una opción 😉:\n1. Cursos Corta Duración\n2. Diplomados"
            user_session["step"] += 1

    elif step == 5:
        if message == "1":
            user_session["interes"] = "Cursos Corta Duración"
        elif message == "2":
            user_session["interes"] = "Diplomados"
        else:
            reply = "Opción no válida. Por favor, selecciona una opción correcta 📛\n1. Cursos Corta Duración\n2. Diplomados"
            return jsonify({"reply": reply})  # Salir si no es válido

        # Guardar el interés en MongoDB
        guardar_o_actualizar_usuario(user_id, interes=user_session["interes"])

        reply = f"¡Gracias por tu interés en nuestros {user_session['interes']}! Tu información ha sido guardada 🗂️."

        # Finalizar la sesión
        del user_sessions[user_id]

    return jsonify({"reply": reply})


# Iniciar el servidor en el puerto 5000
if __name__ == "__main__":
    app.run(port=5000, debug=True)
