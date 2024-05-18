from utils.db import db
from model.evaluaciones import Evaluaciones
from sqlalchemy import Date

class Retroalimentacion(db.Model):
    __tablename__ = 'retroalimentacion'
    
    id_retroalimentacion = db.Column(db.Integer, primaty_key= True)
    id_evaluacion = db.Column(db.Integer, db.ForeignKey('evaluaciones.id_evaluacion'))
    fecha_seguimiento = db.Column(Date)
    notas = db.Column(db.Text)
    observaciones = db.Column(db.Text)

    evaluaciones = db.relationship('Evaluaciones', backref = 'retroalimentacion')

    def __init__(self,id_retroalimentacion,id_evaluacion,fecha_seguimiento,notas,observaciones):
        self.id_retroalimentacion = id_retroalimentacion
        self.id_evaluacion = id_evaluacion
        self.fecha_seguimiento = fecha_seguimiento
        self.notas = notas
        self.observaciones = observaciones