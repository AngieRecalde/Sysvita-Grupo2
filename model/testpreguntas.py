from utils.db import db
from model.tests import Tests
from model.preguntas import Preguntas
from dataclasses import dataclass
@dataclass
class TestPregunta(db.Model):
    __tablename__ = 'testpregunta'

    id_test_pregunta = db.Column(db.Integer, primary_key = True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))
    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id_pregunta'))

    test1 = db.relationship('Test', backref = 'respuesta-pregunta')
    pregunta1 = db.relationship('Pregunta', backref = 'respuesta-estudiante')

    def __init__(self,id_test,id_test_pregunta,id_pregunta):
        self.id_test_pregunta=id_test_pregunta
        self.id_test = id_test
        self.id_pregunta = id_pregunta