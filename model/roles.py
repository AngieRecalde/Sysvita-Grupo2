from utils.db import db
from dataclasses import dataclass
@dataclass
class Roles(db.Model):
    __tablename__ = 'roles'
    id_rol=db.Column(db.Integer, primary_key=True) 
    nombre_rol=db.Column(db.String(50))

    def __init__(self,nombre_rol): #definición del constructor
        self.nombre_rol = nombre_rol