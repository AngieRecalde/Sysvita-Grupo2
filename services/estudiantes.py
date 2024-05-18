from flask import Blueprint, request, jsonify
from model.estudiantes import Estudiantes
from utils.db import db
from datetime import datetime


#crear un blueprint para las rutas de Predio
estudiantes=Blueprint('estudiantes',__name__) 
def estudiante_to_dict(estudiante):
    return {
        'id_estudiante': estudiante.id_estudiante,
        'nombre': estudiante.nombre,
        'genero': estudiante.genero,
        'password': estudiante.password,
        'fecha_registro': estudiante.fecha_registro.isoformat() if estudiante.fecha_registro else None,
        'edad': estudiante.edad,
        'email': estudiante.email,
        'telefono': estudiante.telefono,
        'carrera': estudiante.carrera
    }


@estudiantes.route('/sysvita/estudiantes',methods=['GET'])
def getMensaje():
    result={}
    result["data"]='PROYECTO-SYSVITA'
    return jsonify(result)

@estudiantes.route('/sysvita/estudiantes/listar', methods=['GET'])
def getEstudiantes():
    result = {}
    estudiantes_data = [estudiante_to_dict(estudiante) for estudiante in Estudiantes.query.all()]
    result["data"] = estudiantes_data
    result["status_code"] = 200
    result["msg"] = "Se recuperaron los estudiantes sin inconvenientes"
    return jsonify(result), 200

@estudiantes.route('/sysvita/estudiantes/insert', methods=['POST'])
def insertEstudiantes():
    result = {}
    body = request.get_json()
    nombre = body.get('nombre')
    genero = body.get('genero')
    password = body.get('password')
    fecha_registro_str = body.get('fecha_registro')  # Obtener la fecha como cadena
    edad = body.get('edad')
    email = body.get('email')
    telefono = body.get('telefono')
    carrera = body.get('carrera')

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

    estudiante = Estudiantes(nombre, email, genero, password, fecha_registro, edad, telefono, carrera)
    db.session.add(estudiante)
    db.session.commit()
    result["data"] = estudiante
    result["status_code"] = 201
    result["msg"] = "Se agregó el estudiante"
    return jsonify(result), 201

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
    
        result["msg"] = "El predio no existe"
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