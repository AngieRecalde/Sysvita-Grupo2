from utils.db import db
from model.preguntas import Preguntas


class Respuestas(db.Model):
    __tablename__ = 'respuestas'

    id_respuestas = db.Column(db.Integer, primary_key = True)
    id_pregunta = db.Column(db.Integer, db.ForeignKey('preguntas.id_pregunta'))
    valor = db.Column(db.Integer)

    def __init__(self,id_respuestas,id_pregunta,valor):
        self.id_pregunta=id_pregunta
        self.id_respuestas = id_respuestas
        self.valor = valor
