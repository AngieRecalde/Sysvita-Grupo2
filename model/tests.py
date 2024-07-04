from utils.db import db
from dataclasses import dataclass

@dataclass
class Tests(db.Model):
    __tablename__ = 'tests'
    id_test = db.Column(db.Integer, primary_key=True)
    nombre_test = db.Column(db.String(100))
    descripcion = db.Column(db.Text)
    tipo_test = db.Column(db.String(50))
    
    def __init__(self, nombre_test,descripcion,tipo_test):
        self.nombre_test = nombre_test
        self.descripcion = descripcion
        self.tipo_test = tipo_test