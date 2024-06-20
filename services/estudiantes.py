from flask import Blueprint, request, jsonify, make_response,redirect,url_for
from model.estudiantes import Estudiantes
from utils.db import db
from datetime import datetime
from schemas.estudiantes_schema import estudiantes_schema, estudiante_schema

estudiantes=Blueprint('estudiantes',__name__) 

@estudiantes.route('/sysvita/estudiantes',methods=['GET'])
def getMensaje():
    result={}
    result["data"]='PROYECTO-SYSVITA'
    return jsonify(result)

@estudiantes.route('/sysvita/estudiantes/listar', methods=['GET'])
def getEstudiantes():
    result = {}
    estudiantes = Estudiantes.query.all()
    
    estudiantes_data = []
    for estudiante in estudiantes:
        estudiante_data = {
            "id_estudiante": estudiante.id_estudiante,
            "nombre": estudiante.nombre,
            "genero": estudiante.genero,
            "password": estudiante.password,
            "fecha_registro": estudiante.fecha_registro.strftime('%Y-%m-%d'),
            "edad": estudiante.edad,
            "email": estudiante.email,
            "telefono": estudiante.telefono,
            "carrera": estudiante.carrera
        }
        estudiantes_data.append(estudiante_data)
    
    result["data"] = estudiantes_data
    result["status_code"] = 200
    result["msg"] = "Se recuperaron los estudiantes sin inconvenientes"
    return jsonify(result), 200

@estudiantes.route('/sysvita/estudiantes/insert', methods=['POST'])
def insertEstudiantes():
    nombre = request.json.get('nombre')
    genero = request.json.get('genero')
    password = request.json.get('password')
    fecha_registro_str = request.json.get('fecha_registro')  # Obtener la fecha como cadena
    edad = request.json.get('edad')
    email = request.json.get('email')
    telefono = request.json.get('telefono')
    carrera = request.json.get('carrera')
    try:
        fecha_registro = datetime.strptime(fecha_registro_str, '%Y-%m-%d').date() # Convertir la cadena a objeto datetime
    except ValueError:
        data["status_code"] = 400
        data["msg"] = "El formato de fecha es inválido. Utilice el formato 'yy-mm-dd'."
        return jsonify(data), 400
    new_estudiante = Estudiantes(nombre, email, genero, password, fecha_registro, edad, telefono, carrera)
    db.session.add(new_estudiante)
    db.session.commit()
    result = estudiantes_schema.dump(new_estudiante)
    data = {
        'message': 'Nuevo estudiante registrado',
        'status': 201,
        'data': result
    }
    return make_response(jsonify(data),201)

@estudiantes.route('/sysvita/estudiantes/update',methods=['POST'])
def update():
    result={}
    body=request.get_json()
    id_estudiante = body.get('id_estudiante')
    nombre = body.get('nombre')
    email = body.get('email')
    genero = body.get('genero')
    telefono = body.get('telefono')
    password = body.get('password')
    fecha_registro = body.get('fecha_registro')
    edad = body.get('edad')
    carrera = body.get('carrera')
    
    if not all([id_estudiante, nombre, email, genero, telefono, password, fecha_registro, edad, carrera]):
        result["status_code"] = 400
        result["msg"] = "Faltan datos"
        return jsonify(result), 400
    #Encuentra el predio a actualizar
    estudiante = Estudiantes.query.get(id_estudiante)
    if not estudiante:
        result["status_code"] = 400
        return jsonify(result), 400
    
    # Actualiza los valores del predio
    estudiante.nombre = nombre
    estudiante.genero = genero
    estudiante.password = password
    estudiante.fecha_registro = fecha_registro
    estudiante.edad = edad 
    estudiante.email = email
    estudiante.telefono = telefono
    estudiante.carrera = carrera
    #guarda los cambios   
    db.session.commit()
    
    result["data"]=estudiante
    result["status_code"]=202
    result["msg"]="Se modificó el estudiante"
    return jsonify(result),202

@estudiantes.route('/sysvita/estudiantes/delete',methods=['DELETE'])
def deleteEstudiantes():
    result={}
    body=request.get_json()
    id_estudiante = body.get('id_estudiante')   
    if not id_estudiante:  # Verifica que se proporciona un ID
        result["status_code"]=400
        result["msg"]="Debe consignar un id valido"
        return jsonify(result),400
    #Encuentra predio a eliminar
    estudiante = Estudiantes.query.get(id_estudiante)
    if not estudiante:
        result["status_code"]=400
        result["msg"]="El estudiante no existe"
        return jsonify(result),400
    #elimina el predio
    db.session.delete(estudiante)
    db.session.commit()
    
    result["data"]=estudiante
    result["status_code"]=200
    result["msg"]="Se eliminó el estudiante"
    return jsonify(result),200