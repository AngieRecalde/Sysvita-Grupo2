from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from datetime import datetime
from model.estudiantes import Estudiantes
from schemas.estudiantes_schema import estudiante_schema, estudiantes_schema

estudiante_routes = Blueprint('estudiante_routes', __name__)

@estudiante_routes.route('/sysvita/estudiantes/create', methods=['POST'])
def create_Estudiantes():
    nombre = request.json.get('nombre')
    genero = request.json.get('genero')
    password = request.json.get('password')
    fecha_registro_str = request.json.get('fecha_registro')  # Obtener la fecha como cadena
    edad = request.json.get('edad')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    carrera = request.json.get('carrera')

    if not all([nombre, genero, password, fecha_registro_str, edad, email, telefono, carrera]):
        result["status_code"] = 400
        result["msg"] = "Faltan datos"
        return jsonify(result), 400

    try:
        fecha_registro = datetime.strptime(fecha_registro_str, '%Y-%m-%d').date()  # Convertir la cadena a objeto date
    except ValueError:
        result["status_code"] = 400
        result["msg"] = "El formato de fecha es inválido. Utilice el formato YYYY-MM-DD."
        return jsonify(result), 400
    
    new_estudiante = Estudiantes(nombre, email, genero, password, fecha_registro, edad, telefono, carrera)

    db.session.add(new_estudiante)
    db.session.commit()

    result = estudiante_schema.dump(new_estudiante)
    data = {
        'message': 'Nuevo estudiantes registrado',
        'status': 201,
        'data': result
    }
    return make_response(jsonify(data),201)