from utils.db import db
from dataclasses import dataclass
@dataclass
class Tratamientos(db.Model):
    __tablename__ = 'tratamiento'
    id_tratamiento=db.Column(db.Integer, primary_key=True) 
    id_evaluacion = db.Column(db.Integer , db.ForeignKey('evaluacion_especialista.id_evaluacion'), nullable=False)
    descripcion=db.Column(db.Text)

    # Relationship to reference back to Evaluacion_Especialistas
    evaluacion = db.relationship('Evaluacion_Especialistas', backref='tratamientos', primaryjoin='Tratamientos.id_evaluacion == Evaluacion_Especialistas.id_evaluacion')


    def __init__(self,id_evaluacion,descripcion): #definición del constructor
        self.id_evaluacion = id_evaluacion
        self.descripcion = descripcion
