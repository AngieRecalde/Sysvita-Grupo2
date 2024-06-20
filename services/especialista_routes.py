from flask import Blueprint, request, jsonify, make_response
from model.especialistas import Especialistas
from model.usuarios import Usuarios
from utils.db import db
from schemas.especialista_schema import especialistas_schema, especialista_schema
from sqlalchemy.exc import SQLAlchemyError
import logging

#crear un blueprint para las rutas de Predio
especialista_routes=Blueprint('especialista_routes',__name__) 


@especialista_routes.route('/especialista_routes/listar',methods=['GET'])
def getEspecialistas():
    result={}
    especialistas=Especialistas.query.all()
    especialistas_data = []
    for especialista in especialistas:
        especialista_data = {
            "id_especialista": especialista.id_especialista,
            "nombre":especialista.nombre,
            "especialidad":especialista.especialidad,
            "fecha_registro": str(especialista.fecha_registro),  
            "telefono": especialista.telefono,
            "id_usuario": especialista.id_usuario,
        }
        especialistas_data.append(especialista_data)

    result["data"]=especialistas_data
    result["status_code"]=200
    result["msg"]="Se recupero los datos de especialistas sin inconvenientes"
    return jsonify(result),200

@especialista_routes.route('/especialista_routes/insert', methods=['POST'])
def insertEspecialistas():
    try:
        data = request.json
        # Imprimir el contenido de request.json para depurar
        logging.debug(f"Datos recibidos en request.json: {data}")

        password = data.get('password')
        if not password:
            return jsonify({'message': 'Se debe proporcionar una contraseña'}), 400

        # Crear un nuevo usuario
        email = data.get('email')
        perfil = 'Especialista'  # Asignar perfil como 'Especialista'
        new_usuario = Usuarios(email, password, perfil)
        db.session.add(new_usuario)
        db.session.flush()  # Asignar el id_usuario generado

        # Obtener el id_usuario generado
        id_usuario = new_usuario.id_usuario

        # Crear un nuevo especialista
        nombre = data.get('nombre')
        especialidad = data.get('especialidad')
        fecha_registro = data.get('fecha_registro')
        telefono = data.get('telefono')
        new_especialista = Especialistas(nombre, id_usuario, fecha_registro, telefono, especialidad)
        db.session.add(new_especialista)
        db.session.commit()

        result = especialista_schema.dump(new_especialista)
        data = {
            'message': 'Nuevo especialista registrado',
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
@especialista_routes.route('/especialista_routes/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    # Obtener todos los usuarios con el mismo correo electrónico
    users = Usuarios.query.filter_by(email=email).all()

    if not users:
        # Si no hay usuarios con ese correo electrónico
        return jsonify({'message': 'Credenciales inválidas'}), 401

    for user in users:
        if user.check_password(password):
            # Inicio de sesión exitoso
            return jsonify({'message': 'Inicio de sesión exitoso', 'id_usuario': user.id_usuario}), 200
    
    # Si ninguna combinación de correo electrónico y contraseña coincide
    return jsonify({'message': 'Credenciales inválidas'}), 401