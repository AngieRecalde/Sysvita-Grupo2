from utils.db import db
from model.tests import Tests

class Preguntas(db.model):
    __tablename__ = 'preguntas'
    id_pregunta = db.Column(db.Integer, primary_key=True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))
    enunciado = db.Column(db.Text)
    tipo_escala = db.Column(db.String(20))
    numero_pregunta = db.Column(db.Integer)

    tests = db.relationship('Tests', backref = 'preguntas')

    def __init__(self,id_pregunta,id_test,enunciado,tipo_escala,numero_pregunta):
        self.id_pregunta = id_pregunta
        self.id_test = id_test
        self.enunciado = enunciado
        self.tipo_escala = tipo_escala
        self.numero_pregunta = numero_pregunta