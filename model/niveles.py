from utils.db import db
from dataclasses import dataclass

@dataclass
class Niveles(db.Model):
    __tablename__ = 'niveles'
    id_nivel = db.Column(db.Integer, primary_key=True) 
    tipo_nivel = db.Column(db.String(50))
    nombre_nivel = db.Column(db.String(50))
    color = db.Column(db.String(20))
    
    def __init__(self, tipo_nivel, nombre_nivel, color):
        self.tipo_nivel = tipo_nivel
        self.nombre_nivel = nombre_nivel
        self.color = color