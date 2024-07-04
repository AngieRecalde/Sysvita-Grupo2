from sqlalchemy import DateTime
from utils.db import db
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Personas(db.Model):
    __tablename__ = 'personas'
    id_persona = db.Column(db.Integer, primary_key=True) 
    id_ubigeo = db.Column(db.Integer, db.ForeignKey('ubigeos.id_ubigeo'))
    nombres = db.Column(db.String(100))
    apellidos = db.Column(db.String(100))
    fecha_registro = db.Column(DateTime, default=datetime.utcnow, nullable=False)
    telefono = db.Column(db.String(15))
    edad = db.Column(db.Integer)
    fechaupdatepers = db.Column(DateTime, nullable=True)

    ubigeo = db.relationship('Ubigeos', backref='ubigeo-persona')

    def __init__(self, id_ubigeo, nombres, apellidos, telefono, edad, fecha_registro=None):
        self.id_ubigeo = id_ubigeo
        self.nombres = nombres
        self.apellidos = apellidos
        self.telefono = telefono
        self.edad = edad
        self.fecha_registro = fecha_registro or datetime.utcnow()
