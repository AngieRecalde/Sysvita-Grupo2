from flask import Blueprint, request, jsonify, make_response
from model.estudiantes import Estudiantes
from model.usuarios import Usuarios
from utils.db import db
from datetime import datetime
from schemas.estudiantes_schema import estudiantes_schema, estudiante_schema
from sqlalchemy.exc import SQLAlchemyError
import logging
import bcrypt

estudiante_routes = Blueprint('estudiantes_routes', __name__)

@estudiante_routes.route('/estudiantes_routes/listar', methods=['GET'])
def getEstudiantes():
    result = {}
    estudiantes = Estudiantes.query.all()

    estudiantes_data = []
    for estudiante in estudiantes:
        estudiante_data = {
            "id_estudiante": estudiante.id_estudiante,
            "nombre": estudiante.nombre,
            "genero": estudiante.genero,
            "fecha_registro": str(estudiante.fecha_registro),  # Convertir fecha a cadena
            "edad": estudiante.edad,
            "telefono": estudiante.telefono,
            "carrera": estudiante.carrera
        }
        estudiantes_data.append(estudiante_data)

    result["data"] = estudiantes_data
    result["status_code"] = 200
    result["msg"] = "Se recuperaron los estudiantes sin inconvenientes"
    return jsonify(result), 200

@estudiante_routes.route('/estudiantes_routes/insert', methods=['POST'])
def insertEstudiantes():
    try:
        data = request.json
        logging.debug(f"Datos recibidos: {data}")

        # Validar que se proporcionó una contraseña
        password = data.get('password')
        if not password:
            return jsonify({'message': 'Se debe proporcionar una contraseña'}), 400

        # Crear un nuevo usuario
        email = data.get('email')
        perfil = 'Estudiante'  # Asignar perfil como 'Estudiante'
        new_usuario = Usuarios(email, password,perfil)
        db.session.add(new_usuario)
        db.session.flush()  # Asignar el id_usuario generado

        # Crear un nuevo estudiante con el id_usuario generado
        nombre = data.get('nombre')
        genero = data.get('genero')
        fecha_registro_str = data.get('fecha_registro')
        edad = data.get('edad')
        telefono = data.get('telefono')
        carrera = data.get('carrera')
        new_estudiante = Estudiantes(nombre, genero, new_usuario.id_usuario, fecha_registro_str, edad, telefono, carrera)
        db.session.add(new_estudiante)
        db.session.commit()

        result = estudiante_schema.dump(new_estudiante)
        data = {
            'message': 'Nuevo estudiante registrado',
            'status': 201,
            'data': result
        }
        return make_response(jsonify(data), 201)
    except ValueError as e:
        data = {
            'message': 'Error en el formato de fecha',
            'status': 400,
            'error': str(e)
        }
        return make_response(jsonify(data), 400)
    except SQLAlchemyError as e:
        db.session.rollback()
        data = {
            'message': 'Error al procesar la solicitud',
            'status': 500,
            'error': str(e)
        }
        return make_response(jsonify(data), 500)
    
@estudiante_routes.route('/estudiantes_routes/login', methods=['POST'])
def login():
    data = request.json
    email2 = data.get('email')
    password2 = data.get('password')

    # Obtener todos los usuarios con el mismo correo electrónico
    users = Usuarios.query.filter_by(email=email2).all()

    if not users:
        # Si no hay usuarios con ese correo electrónico
        return jsonify({'message': 'Credenciales inválidas'}), 401

    for user in users:
        if user.check_password(password2):
            # Inicio de sesión exitoso
            return jsonify({'message': 'Inicio de sesión exitoso', 'id_usuario': user.id_usuario}), 200
    
    # Si ninguna combinación de correo electrónico y contraseña coincide
    return jsonify({'message': 'Credenciales inválidas'}), 401
