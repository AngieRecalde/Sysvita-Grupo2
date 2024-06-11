from utils.db import db
from model.estudiantes import Estudiantes
from sqlalchemy import Date


class Tests (db.Model):
    __tablename__ = 'tests'
    id_test=db.Column(db.Integer, primary_key=True) 
    id_estudiante=db.Column(db.Integer, db.ForeignKey('estudiantes.id_estudiante'))
    fecha_test=db.Column(Date)
    tipo_test=db.Column(db.String(10))

    estudiantes = db.relationship('Estudiantes', backref='tests')

    def __init__(self,id_test,id_estudiante,fecha_test,tipo_test): #definición del constructor
        self.id_test=id_test
        self.id_estudiante=id_estudiante
        self.fecha_test = fecha_test
        self.tipo_test = tipo_test
