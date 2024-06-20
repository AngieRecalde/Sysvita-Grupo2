
from sqlalchemy import DateTime
from utils.db import db
from dataclasses import dataclass
@dataclass
class Especialistas(db.Model):
    __tablename__ = 'especialistas'
    id_especialista=db.Column(db.Integer, primary_key=True) 
    id_usuario = db.Column(db.Integer , db.ForeignKey('usuarios.id_usuario'))
    nombre=db.Column(db.String(60))
    especialidad=db.Column(db.String(30))
    fecha_registro=db.Column(DateTime)
    telefono=db.Column(db.String(10))

    usuario2 = db.relationship('Usuarios', backref = 'usuario-especialista')

    def __init__(self,nombre,id_usuario,fecha_registro,telefono,especialidad): #definición del constructor
        self.nombre=nombre
        self.id_usuario = id_usuario
        self.fecha_registro=fecha_registro
        self.especialidad = especialidad
        self.telefono = telefono
