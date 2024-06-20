from utils.db import db
from model.testpreguntas import TestPregunta
from model.opciones import Opcion
from model.estudiantes import Estudiantes
from dataclasses import dataclass
@dataclass
class Respuestas(db.Model):
    __tablename__ = 'respuestas'

    id_respuesta = db.Column(db.Integer, primary_key = True)
    id_test_pregunta = db.Column(db.Integer, db.ForeignKey('testpregunta.id_test_pregunta'))
    id_opcion = db.Column(db.Integer, db.ForeignKey('opciones.id_opcion'))
    id_estudiante = db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'))

    test1 = db.relationship('TestPregunta', backref = 'respuesta-tests')
    opcion1 = db.relationship('Opciones', backref = 'respuesta-opcion')
    estudiante2 = db.relationship('Estudiantes', backref = 'respuesta-estudiante')

    def __init__(self,id_test_pregunta,id_pregunta,id_opcion,id_estudiante):
        self.id_pregunta=id_pregunta
        self.id_test_pregunta = id_test_pregunta
        self.id_opcion = id_opcion
        self.id_estudiante = id_estudiante
