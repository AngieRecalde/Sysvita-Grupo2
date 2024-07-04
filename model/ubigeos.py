from utils.db import db
from dataclasses import dataclass

@dataclass
class Ubigeos(db.Model):
    __tablename__ = 'ubigeos'
    id_ubigeo = db.Column(db.Integer, primary_key=True)
    departamento = db.Column(db.String(50))
    provincia = db.Column(db.String(50))
    distrito = db.Column(db.String(50))
    poblacion = db.Column(db.String(50))
    superficie = db.Column(db.String(50))
    y =db.Column(db.Numeric)
    x = db.Column(db.Numeric)

    def __init__(self, departamento,provincia,distrito,poblacion,superficie,y,x):
        self.departamento = departamento
        self.provincia = provincia
        self.distrito = distrito
        self.poblacion = poblacion
        self.supercie = superficie
        self.y = y
        self.x = x
        