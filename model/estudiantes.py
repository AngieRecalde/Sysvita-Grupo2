from utils.db import db
from dataclasses import dataclass
from datetime import date
from datetime import datetime

@dataclass
class Estudiantes(db.Model):
    __tablename__ = 'estudiantes'
    id_estudiante = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer , db.ForeignKey('personas.id_persona')) 
    carrera = db.Column(db.String(100))

    persona2 = db.relationship('Personas', backref = 'persona-estudiante')
    def __init__(self,id_persona,carrera): #definición del constructor
        self.carrera = carrera
        self.id_persona = id_persona

