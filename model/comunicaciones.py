from utils.db import db
from dataclasses import dataclass
@dataclass
class Comunicaciones(db.Model):
    __tablename__ = 'comunicacion'
    id_comunicacion=db.Column(db.Integer, primary_key=True) 
    id_evaluacion = db.Column(db.Integer , db.ForeignKey('evaluacion_especialista.id_evaluacion'))
    recomendacion=db.Column(db.Text)

    comunicacion = db.relationship('Evaluacion_Especialistas', backref = 'evaluacion-comunicacion')

    def __init__(self,id_evaluacion,recomendacion): #definición del constructor
        self.id_evaluacion = id_evaluacion
        self.recomendacion = recomendacion
