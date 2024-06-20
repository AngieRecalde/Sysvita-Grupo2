from utils.db import db
from sqlalchemy import Date

class Tests (db.Model):
    __tablename__ = 'tests'
    id_test=db.Column(db.Integer, primary_key=True) 
    id_usuario=db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario'))
    fecha_test=db.Column(Date)
    tipo_test=db.Column(db.String(10))

    usuarios3 = db.relationship('Usuarios', backref='tests')

    def __init__(self,id_test,id_usuario,fecha_test,tipo_test): #definición del constructor
        self.id_test=id_test
        self.id_usuario=id_usuario
        self.fecha_test = fecha_test
        self.tipo_test = tipo_test
