from utils.db import db
from dataclasses import dataclass
@dataclass
class Alternativas(db.Model):
    __tablename__ = 'alternativas'
    id_alternativa=db.Column(db.Integer, primary_key=True) 
    id_pregunta = db.Column(db.Integer , db.ForeignKey('preguntas.id_pregunta'))
    texto_opcion=db.Column(db.Text)
    valor = db.Column(db.Integer)

    pregunta = db.relationship('Preguntas', backref = 'pregunta-alternativa')

    def __init__(self,id_pregunta,texto_opcion,valor): #definición del constructor
        self.id_pregunta = id_pregunta
        self.texto_opcion = texto_opcion
        self.valor = valor