from sqlalchemy import DateTime
from utils.db import db
from dataclasses import dataclass
import bcrypt

@dataclass
class Usuarios(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    perfil = db.Column(db.String(255), nullable=False)
    def __init__(self, email, password,perfil):
        self.email = email
        self.set_password(password)
        self.perfil = perfil

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

