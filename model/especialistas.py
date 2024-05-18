from utils.db import db
from dataclasses import dataclass
from sqlalchemy import Date

@dataclass
class Especialistas(db.Model):
    __tablename__ = 'especialistas'
    id_especialista=db.Column(db.Integer, primary_key=True) 
    nombre=db.Column(db.String(60))
    especialidad=db.Column(db.String(30))
    email=db.Column(db.String(30))
    password=db.Column(db.String(12))
    fecha_registro=db.Column(Date)
    telefono=db.Column(db.String(10))

    def __init__(self,nombre,email,password,fecha_registro,telefono,especialidad): #definición del constructor
        self.nombre=nombre
        self.email=email
        self.password=password
        self.fecha_registro=fecha_registro
        self.especialidad = especialidad
        self.telefono = telefono
