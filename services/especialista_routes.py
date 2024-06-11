from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from datetime import datetime
from model.especialistas import Especialistas
from schemas.especialistas_schema import especialistas_schema,especialista_schema

especialista_routes = Blueprint('especialista_routes', __name__)

@especialista_routes.route('/especialista_routes/create', methods=['POST'])
def create_Especialista():
    nombre = request.json.get('nombre')
    especialidad = request.json.get('especialidad')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    fecha_registro_str2 = request.json.get('fecha_registro')  # Obtener la fecha como cadena
    password = request.json.get('password')
    try:
        # Convertir la cadena de fecha a objeto date
        fecha_registro2 = datetime.strptime(fecha_registro_str2, '%Y-%m-%d').date()
    except ValueError:
        data["status_code"] = 400
        data["msg"] = "El formato de fecha es inválido. Utilice el formato YYYY-MM-DD."
        return jsonify(data), 400

    new_especialista = Especialistas(nombre,especialidad,email, telefono,fecha_registro2,password)

    db.session.add(new_especialista)
    db.session.commit()

    result = especialista_schema.dump(new_especialista)
    data = {
        'message': 'Nuevo especialista registrado',
        'status': 201,
        'data': result
    }
    return make_response(jsonify(data), 201)

@especialista_routes.route('/especialista_routes/buscar/<int:id>', methods=['GET'])
def get_Especialista(id):
    especialista = Especialistas.query.get(id)

    if not especialista:
        data1 = {
            'message': 'Especialista no encontrado',
            'status': 404
        }
        return make_response(jsonify(data1), 404)

    # Convertir el objeto especialista a un diccionario
    especialista_data = especialista_schema.dump(especialista)
    
    data1 = {
        'message': 'Especialista encontrado',
        'status': 200,
        'data': especialista_data  # Incluir los datos del especialista en la respuesta
    }
    return make_response(jsonify(data1), 200)

@especialista_routes.route('/especialista_routes/modificar/<int:id>', methods=['PUT'])
def updateEspecialista(id):
    especialista = Especialistas.query.get(id)

    if not especialista:
        data = {
            'message': 'Especialista no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    nombre = request.json.get('nombre')
    especialidad = request.json.get('especialidad')
    password = request.json.get('password')
    fecha_registro_str = request.json.get('fecha_registro')  # Obtener la fecha como cadena
    email = request.json.get('email')
    telefono = request.json.get('telefono')

    data = {}

    try:
        fecha_registro = datetime.strptime(fecha_registro_str, '%Y-%m-%d').date()  # Convertir la cadena a objeto date
    except ValueError:
        data = {
            'message': 'El formato de fecha es inválido. Utilice el formato YYYY-MM-DD.',
            'status': 400,
        }
        return jsonify(data), 400

    especialista.nombre = nombre
    especialista.especialidad = especialidad
    especialista.password = password
    especialista.fecha_registro = fecha_registro
    especialista.email = email
    especialista.telefono = telefono

    db.session.commit()
    result = especialista_schema.dump(especialista)
    data = {
        'message': 'Especialista modificado',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data), 200)

@especialista_routes.route('/especialista_routes/eliminar/<int:id>', methods=['DELETE'])
def delete_Especialista(id):
    especialista = Especialistas.query.get(id)
    if not especialista: 
        data = {
            'message': 'Especialista no encontrado',
            'status': 404
        }
        return make_response(jsonify(data), 404)

    db.session.delete(especialista)
    db.session.commit()

    data = {
        'message': 'Especialista eliminado',
        'status': 200
    }
    return make_response(jsonify(data), 200)
