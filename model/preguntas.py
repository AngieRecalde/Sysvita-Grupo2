from utils.db import db
from dataclasses import dataclass
@dataclass
class Preguntas(db.Model):
    __tablename__ = 'preguntas'
    id_pregunta=db.Column(db.Integer, primary_key=True) 
    id_test = db.Column(db.Integer , db.ForeignKey('tests.id_test'))
    texto_pregunta=db.Column(db.Text)
    orden = db.Column(db.Integer)

    test1 = db.relationship('Tests', backref = 'test-pregunta')

    def __init__(self,id_test,texto_pregunta,orden): #definición del constructor
        self.id_test = id_test
        self.texto_pregunta = texto_pregunta
        self.orden = orden
