from flask import Blueprint, jsonify
from app import mongo

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return jsonify({"message": "¡Bienvenido a tu ChatBot con Flask y MongoDB!"})


@main.route("/data")
def get_data():
    # Accede a una colección de MongoDB y retorna datos
    collection = mongo.db.tu_coleccion
    data = collection.find_one()  # Obtén el primer documento como ejemplo
    return jsonify({"data": data})
