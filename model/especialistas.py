from utils.db import db
from dataclasses import dataclass
@dataclass
class Especialistas(db.Model):
    __tablename__ = 'especialistas'
    id_especialista=db.Column(db.Integer, primary_key=True) 
    id_persona = db.Column(db.Integer , db.ForeignKey('personas.id_persona'))
    especialidad=db.Column(db.String(100))

    persona1 = db.relationship('Personas', backref = 'persona-especialista')

    def __init__(self,id_persona,especialidad): #definición del constructor
        self.id_persona = id_persona
        self.especialidad = especialidad
