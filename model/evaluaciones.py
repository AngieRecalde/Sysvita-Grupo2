from utils.db import db
from model.tests import Tests
from model.especialistas import Especialistas
from sqlalchemy import Date

class Evaluaciones(db.Model):
    __tablename__ = 'evakuaciones'

    id_evaluacion = db.Column(db.Integer, primary_key = True )
    id_test = db.Column(db.Integer , db.ForeignKey('tests.id_test'))
    id_especialista = db.Column(db.Integer , db.ForeignKey('especialistas.id_especialista'))
    fecha_evaluacion = db.Column(Date)
    puntuacion_estado = db.Column(db.String(2))
    puntuacion_rasgo = db.Column(db.String(2))
    nivel_depresion_estado = db.Column(db.String(15))
    nivel_depresion_rasgo = db.Column(db.String(15))
    nivel_ansiedad_estado = db.Column(db.String(15))
    nivel_ansiedad_rasgo = db.Column(db.String(15))
    retroalimentacion = db.Column(db.Text)
    descripcion = db.Column(db.Text)
    recursos = db.Column(db.Text)
    recomendaciones = db.Column(db.Text)

    tests = db.relationship('Tests', backref = 'evaluaciones')
    especialistas = db.relationship('Especialistas', backref = 'evaluaciones')

    def __init__(self,id_evaluacion,id_test,id_especialista,fecha_evaluacion,puntuacion_estado,puntuacion_rasgo,nivel_depresion_estado,nivel_depresion_rasgo,nivel_ansiedad_rasgo,nivel_ansiedad_estado,retroalimentacion,descripcion,recursos,recomendaciones):
        self.id_evaluacion = id_evaluacion
        self.id_test = id_test
        self.id_especialista = id_especialista
        self.fecha_evaluacion = fecha_evaluacion
        self.puntuacion_estado = puntuacion_estado
        self.puntuacion_rasgo = puntuacion_rasgo
        self.nivel_depresion_estado = nivel_depresion_estado
        self.nivel_depresion_rasgo = nivel_depresion_rasgo
        self.nivel_ansiedad_estado = nivel_ansiedad_estado
        self.nivel_ansiedad_rasgo = nivel_ansiedad_rasgo
        self.retroalimentacion = retroalimentacion
        self.descripcion = descripcion
        self.recursos = recursos
        self.recomendaciones = recomendaciones