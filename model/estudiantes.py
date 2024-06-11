from utils.db import db
from dataclasses import dataclass
from sqlalchemy import Date


@dataclass
class Estudiantes(db.Model):
    __tablename__ = 'estudiantes'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(60))  
    email = db.Column(db.String(20))  
    genero = db.Column(db.String(10))  
    password = db.Column(db.String(10))  
    fecha_registro = db.Column(Date)  
    edad = db.Column(db.String(2))  
    telefono = db.Column(db.String(15))  
    carrera = db.Column(db.String(20))

    def __init__(self,nombre,email,genero,password,fecha_registro,edad,telefono,carrera): #definición del constructor
        self.nombre=nombre
        self.email=email
        self.genero = genero
        self.password=password
        self.fecha_registro=fecha_registro
        self.edad = edad
        self.telefono = telefono
        self.carrera = carrera

