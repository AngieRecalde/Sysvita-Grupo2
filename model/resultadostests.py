from utils.db import db
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ResultadosTests(db.Model):
    __tablename__ = 'resultadostests'
    id_resultado = db.Column(db.Integer, primary_key=True)
    id_test = db.Column(db.Integer, db.ForeignKey('tests.id_test'))
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    fecha_realizacion = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    puntaje = db.Column(db.Integer)
    respuestas = db.Column(db.String)
    
    test2 = db.relationship('Tests', backref='respuestas_test')
    usuario = db.relationship('Usuarios', backref='respuestas_usuario')
    
    def __init__(self, id_test, id_usuario, fecha_realizacion, puntaje, respuestas):
        self.id_test = id_test
        self.id_usuario = id_usuario
        self.fecha_realizacion = fecha_realizacion
        self.puntaje = puntaje
        self.respuestas = respuestas
