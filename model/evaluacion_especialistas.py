from utils.db import db
from dataclasses import dataclass
@dataclass
class Evaluacion_Especialistas(db.Model):
    __tablename__ = 'evaluacion_especialista'

    id_evaluacion=db.Column(db.Integer, primary_key=True) 
    id_resultado = db.Column(db.Integer , db.ForeignKey('resultadostests.id_resultado'))
    id_especialista = db.Column(db.Integer , db.ForeignKey('especialistas.id_especialista'))
    diagnostico=db.Column(db.Text)
    fundamentacion= db.Column(db.Text)

    resultadostests11 = db.relationship('ResultadosTests', backref = 'resultado-evaluacion')
    especialistas4 = db.relationship('Especialistas', backref = 'especialista-evaluacion')
   
    def __init__(self,id_resultado,diagnostico,fundamentacion,id_especialista=None): #definición del constructor
        self.id_resultado = id_resultado
        self.diagnostico = diagnostico
        self.fundamentacion = fundamentacion
        self.id_especialista = id_especialista