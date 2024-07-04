from flask import Blueprint, request, jsonify, make_response
from model.personas import Personas
from model.usuarios import Usuarios
from model.estudiantes import Estudiantes
from model.especialistas import Especialistas
from model.roles import Roles
from model.ubigeos import Ubigeos
from utils.db import db
from schemas.usuarios_schema import usuario_schema
from sqlalchemy.exc import SQLAlchemyError
import logging
from flask_jwt_extended import create_access_token

registro_routes = Blueprint('registro_routes', __name__)
@registro_routes.route('/registro_routes', methods=['POST'])
def registrar_usuario():
    try:
        data = request.json
        logging.debug(f"Datos recibidos en request.json: {data}")

        # Verificar datos requeridos comunes
        required_fields = ['nombres', 'apellidos', 'email', 'password_hash', 'telefono', 'edad', 'departamento', 'provincia', 'distrito', 'rol']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'El campo {field} es requerido'}), 400

        # Verificar si el email ya existe
        usuario_existente = Usuarios.query.filter_by(email=data['email']).first()
        if usuario_existente:
            return jsonify({'message': 'El email ya se encuentra registrado'}), 400

        # Verificar campos específicos según el rol
        if data['rol'] == 'Estudiante':
            if 'carrera' not in data:
                return jsonify({'message': 'El campo carrera es requerido para estudiantes'}), 400
        elif data['rol'] == 'Especialista':
            if 'especialidad' not in data:
                return jsonify({'message': 'El campo especialidad es requerido para especialistas'}), 400
        else:
            return jsonify({'message': 'Rol no válido. Debe ser Estudiante o Especialista'}), 400

        # Verificar si el ubigeo existe, si no, crearlo
        ubigeo = Ubigeos.query.filter_by(
            departamento=data['departamento'],
            provincia=data['provincia'],
            distrito=data['distrito']
        ).first()

        if not ubigeo:
            ubigeo = Ubigeos(
                departamento=data['departamento'],
                provincia=data['provincia'],
                distrito=data['distrito'],
                poblacion='a',  # Agregar valores por defecto si es necesario
                superficie='a',
                y=0.0,
                x=0.0
            )
            db.session.add(ubigeo)
            db.session.flush()

        # Crear nueva persona
        nueva_persona = Personas(
            id_ubigeo=ubigeo.id_ubigeo,
            nombres=data['nombres'],
            apellidos=data['apellidos'],
            telefono=data['telefono'],
            edad=data['edad']
        )
        db.session.add(nueva_persona)
        db.session.flush()

        # Obtener el rol
        rol = Roles.query.filter_by(nombre_rol=data['rol']).first()
        if not rol:
            return jsonify({'message': f'Rol {data["rol"]} no encontrado'}), 404

        # Crear nuevo usuario
        nuevo_usuario = Usuarios(
            id_persona=nueva_persona.id_persona,
            id_rol=rol.id_rol,
            email=data['email'],
            password=data['password_hash']
        )
        db.session.add(nuevo_usuario)
        db.session.flush()

        # Crear registro específico según el rol
        if data['rol'] == 'Estudiante':
            nuevo_especifico = Estudiantes(
                id_persona=nueva_persona.id_persona,
                carrera=data['carrera']
            )
        else:  # Especialista
            nuevo_especifico = Especialistas(
                id_persona=nueva_persona.id_persona,
                especialidad=data['especialidad']
            )
        db.session.add(nuevo_especifico)

        db.session.commit()

        result = usuario_schema.dump(nuevo_usuario)
        data = {
            'message': f'Nuevo {data["rol"]} registrado exitosamente',
            'status': 201,
            'data': result
        }
        return make_response(jsonify(data), 201)

    except SQLAlchemyError as e:
        db.session.rollback()
        data = {
            'message': 'Error al procesar la solicitud',
            'status': 500,
            'error': str(e)
        }
        return make_response(jsonify(data), 500)
@registro_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        
        # Verificar datos requeridos
        if not data or not data.get('email') or not data.get('password_hash'):
            return jsonify({'message': 'Email y contraseña son requeridos'}), 400

        # Buscar usuario por email
        usuario = Usuarios.query.filter_by(email=data['email']).first()

        if not usuario or not usuario.check_password(data['password_hash']):
            return jsonify({'message': 'Email o contraseña incorrectos'}), 401

        # Obtener el rol del usuario
        rol = Roles.query.get(usuario.id_rol)

        # Crear token de acceso
        access_token = create_access_token(identity=usuario.id_usuario)

        # Simular redirección basada en el rol
        if rol.nombre_rol == 'Estudiante':
            simulated_redirect = 'Redirigiendo a Dashboard de Estudiante'
        elif rol.nombre_rol == 'Especialista':
            simulated_redirect = 'Redirigiendo a Dashboard de Especialista'
        else:
            simulated_redirect = 'Redirigiendo a Dashboard General'

        response_data = {
            'message': 'Login exitoso',
            'access_token': access_token,
            'user_id': usuario.id_usuario,
            'rol': rol.nombre_rol,
            'simulated_redirect': simulated_redirect
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({
            'message': 'Error al procesar la solicitud de login',
            'error': str(e)
        }), 500
@registro_routes.route('/departamentos', methods=['GET'])
def get_departamentos():
    departamentos = Ubigeos.query.with_entities(Ubigeos.departamento).distinct().all()
    return jsonify([d.departamento for d in departamentos])

@registro_routes.route('/provincias/<departamento>', methods=['GET'])
def get_provincias(departamento):
    provincias = Ubigeos.query.with_entities(Ubigeos.provincia).filter_by(departamento=departamento).distinct().all()
    return jsonify([p.provincia for p in provincias])

@registro_routes.route('/distritos/<departamento>/<provincia>', methods=['GET'])
def get_distritos(departamento, provincia):
    distritos = Ubigeos.query.with_entities(Ubigeos.distrito).filter_by(departamento=departamento, provincia=provincia).distinct().all()
    return jsonify([d.distrito for d in distritos])
