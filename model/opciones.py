from utils.db import db
from model.tests import Tests

class Opciones(db.Model):
    __tablename__ = 'opciones'

    id_opcion = db.Column(db.Integer, primary_key = True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))
    texto_opcion = db.Column(db.String(20))
    valor_opcion = db.Column(db.Integer)
    
    preguntas = db.relationship('Tests', backref = 'tests-opcion')

    def __init__(self,id_opcion,id_test,texto_opcion,valor_opcion):
        self.id_opcion=id_opcion
        self.id_test = id_test
        self.texto_opcion = texto_opcion
        self.valor_opcion = valor_opcion