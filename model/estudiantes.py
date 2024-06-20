from sqlalchemy import DateTime
from utils.db import db
from dataclasses import dataclass
from datetime import date
from datetime import datetime

@dataclass
class Estudiantes(db.Model):
    __tablename__ = 'estudiantes'
    fecha_registro: date
    id_estudiante = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer , db.ForeignKey('usuarios.id_usuario'))
    nombre = db.Column(db.String(60))  
    genero = db.Column(db.String(10))   
    fecha_registro = db.Column(DateTime)  
    edad = db.Column(db.String(2))  
    telefono = db.Column(db.String(15))  
    carrera = db.Column(db.String(20))

    usuario = db.relationship('Usuarios', backref = 'usuario-estudiante')
    def __init__(self,nombre,genero,id_usuario,fecha_registro,edad,telefono,carrera): #definición del constructor
        self.nombre=nombre
        self.genero = genero
        self.fecha_registro=fecha_registro
        self.edad = edad
        self.telefono = telefono
        self.carrera = carrera
        self.id_usuario = id_usuario

