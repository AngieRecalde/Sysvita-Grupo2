from sqlalchemy import DateTime
from utils.db import db
from dataclasses import dataclass
import bcrypt
from datetime import datetime
@dataclass
class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    id_persona = db.Column(db.Integer , db.ForeignKey('personas.id_persona'))
    id_rol = db.Column(db.Integer , db.ForeignKey('roles.id_rol'))
    email = db.Column(db.String(30), unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    fechaupdateuser = db.Column(DateTime, nullable=True)

    personas3 = db.relationship('Personas', backref = 'persona-usuarios')
    roles = db.relationship('Roles', backref = 'roles-usuarios')

    def __init__(self, id_persona,id_rol,email, password):
        self.id_persona = id_persona
        self.id_rol = id_rol
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

