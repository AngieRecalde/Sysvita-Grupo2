from flask import Blueprint, request, jsonify
from model.especialistas import Especialistas
from utils.db import db

#crear un blueprint para las rutas de Predio
especialistas=Blueprint('especialistas',__name__) 

@especialistas.route('/sysvita/especialistas',methods=['GET'])
def getMensaje():
    result={}
    result["data"]='PROYECTO-SYSVITA'
    return jsonify(result)

@especialistas.route('/sysvita/especialistas/listar',methods=['GET'])
def getEspecialistas():
    result={}
    especialistas=Especialistas.query.all()
    result["data"]=especialistas
    result["status_code"]=200
    result["msg"]="Se recupero los datos de especialistas sin inconvenientes"
    return jsonify(result),200

@especialistas.route('/sysvita/especialistas/insert',methods=['POST'])
def insertEspecialistas():
    result={}
    body=request.get_json()
    
    nombre = body.get('nombre')
    especialidad = body.get('especialidad')
    email = body.get('telefono')
    password = body.get('correo')
    fecha_registro = body.get('direccion')
    telefono = body.get('idubigeo')

    #verifica que todos los datos esten presentes
    if not all([nombre, especialidad, email, telefono, password, fecha_registro, telefono]):
        result["status_code"] = 400
        result["msg"] = "Faltan datos"
        return jsonify(result), 400
    
    especialistas = Especialistas(nombre, especialidad, email, telefono, password, fecha_registro, telefono)
    db.session.add(especialistas)
    db.session.commit()
    result["data"] = especialistas
    result["status_code"] = 201
    result["msg"] = "Se agregó los datos de especialista"
    return jsonify(result), 201

@especialistas.route('/especialistas/v1/update',methods=['POST'])
def update():
    result={}
    body=request.get_json()
    id_especialista = body.get('id_especialista')
    nombre = body.get('nombre')
    especialidad = body.get('especialidad')
    email = body.get('telefono')
    password = body.get('correo')
    fecha_registro = body.get('direccion')
    telefono = body.get('idubigeo')

    
    if not all([id_especialista, nombre, especialidad, email, telefono, password, fecha_registro, telefono]):
        result["status_code"] = 400
        result["msg"] = "Faltan datos"
        return jsonify(result), 400
    
    #Encuentra  a actualizar
    especialistas = Especialistas.query.get(id_especialista)
    if not especialistas:
        result["status_code"] = 400
        result["msg"] = "El especialista no existe"
        return jsonify(result), 400
    
    # Actualiza los valores del predio
    especialistas.nombre = nombre
    especialistas.especialidad = especialidad
    especialistas.email = email
    especialistas.telefono = telefono
    especialistas.password = password
    especialistas.fecha_registro = fecha_registro
    especialistas.telefono = telefono
    #guarda los cambios   
    db.session.commit()
    
    result["data"]=especialistas
    result["status_code"]=202
    result["msg"]="Se modificó los datos de especialista"
    return jsonify(result),202

@especialistas.route('/especialistas/v1/delete',methods=['DELETE'])
def deleteEspecialistas():
    result={}
    body=request.get_json()
    id_especialista = body.get('id_especialista')   
    if not id_especialista:  # Verifica que se proporciona un ID
        result["status_code"]=400
        result["msg"]="Debe consignar un id valido"
        return jsonify(result),400
    #Encuentra predio a eliminar
    especialistas = Especialistas.query.get(id_especialista)
    if not especialistas:
        result["status_code"]=400
        result["msg"]="El especialista no existe"
        return jsonify(result),400
    #elimina el especialista
    db.session.delete(especialistas)
    db.session.commit()
    
    result["data"]=especialistas
    result["status_code"]=200
    result["msg"]="Se eliminó el especialista"
    return jsonify(result),200