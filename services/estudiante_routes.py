from flask import Blueprint, request, jsonify, make_response
from utils.db import db
from datetime import datetime
from model.estudiantes import Estudiantes
from schemas.estudiantes_schema import estudiantes_schema,estudiante_schema

estudiante_routes = Blueprint('estudiante_routes', __name__)

@estudiante_routes.route('/estudiante_routes/create', methods=['POST'])
def create_Estudiantes():
    nombre = request.json.get('nombre')
    genero = request.json.get('genero')
    password = request.json.get('password')
    fecha_registro_str = request.json.get('fecha_registro')  # Obtener la fecha como cadena
    edad = request.json.get('edad')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    carrera = request.json.get('carrera')
    try:
        fecha_registro = datetime.strptime(fecha_registro_str, '%Y-%m-%d').date()  # Convertir la cadena a objeto date
    except ValueError:
        data["status_code"] = 400
        data["msg"] = "El formato de fecha es inválido. Utilice el formato YYYY-MM-DD."
        return jsonify(data), 400
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
@estudiante_routes.route('/estudiante_routes/buscar/<int:id>', methods = ['GET'])
def get_Estudiante(id):
    estudiante = Estudiantes.query.get(id)

    if not estudiante:
        data = {
            'message' : 'Estudiante no encontrado',
            'status' : 404
        }
        return make_response(jsonify(data),404)
    
    result = estudiante_schema.dump(estudiante)
    data = {
        'message' : 'Estudiante encontrado',
        'status' : 200,
        'data': result
    }
    return make_response(jsonify(data),200)
@estudiante_routes.route('/estudiante_routes/modificar/<int:id>',methods = ['PUT'])
def updateEstudiante(id):
    estudiante = Estudiantes.query.get(id)

    if not estudiante:
        data = {
            'message': 'Estudiante no encontrado',
            'status' : 404
        }
        return make_response(jsonify(data),404)
    nombre = request.json.get('nombre')
    genero = request.json.get('genero')
    password = request.json.get('password')
    fecha_registro_str = request.json.get('fecha_registro')  # Obtener la fecha como cadena
    edad = request.json.get('edad')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    carrera = request.json.get('carrera')
    try:
        fecha_registro = datetime.strptime(fecha_registro_str, '%Y-%m-%d').date()  # Convertir la cadena a objeto date
    except ValueError:
        data = {
            'message': 'El formato de fecha es inválido. Utilice el formato YYYY-MM-DD.',
            'status': 400,
        }
        return jsonify(data), 400
    

    estudiante.nombre = nombre
    estudiante.password = password
    estudiante.fecha_registro = fecha_registro
    estudiante.edad = edad
    estudiante.genero = genero
    estudiante.email = email
    estudiante.telefono = telefono
    estudiante.carrera = carrera

    db.session.commit()
    result = estudiante_schema.dump(estudiante)
    data = {
        'message': 'Estudiante modificado',
        'status': 200,
        'data': result
    }

    return make_response(jsonify(data),200)
@estudiante_routes.route('/estudiante_routes/eliminar/<int:id>', methods = ['DELETE'])
def delete_Estudiante(id):
    estudiante = Estudiantes.query.get(id)
    if not estudiante: 
        data = {
            'message': 'Estudiante no encontrado',
            'status' : 404
        }
        return make_response(jsonify(data),404)
    
    db.session.delete(estudiante)
    db.session.commit()

    data = {
        'message' : 'Estudiante eliminado',
        'status' : 200
    }
    return make_response(jsonify(data),200)
