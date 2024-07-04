from utils.db import db
from dataclasses import dataclass
from datetime import datetime
from .niveles import Niveles  # Asegúrese de importar la clase Niveles

@dataclass
class ResultadosNiveles(db.Model):
    __tablename__ = 'resultados_niveles'
    
    id_resultado = db.Column(db.Integer, db.ForeignKey('resultadostests.id_resultado'), nullable=False)
    id_nivel = db.Column(db.Integer, db.ForeignKey('niveles.id_nivel'), nullable=False)
    observaciones = db.Column(db.Text)
    id_resultadonivelconc = db.Column(db.String(20), primary_key=True)
    
    # Relaciones
    resultado = db.relationship('ResultadosTests', backref='tests_niveles')
    nivel = db.relationship('Niveles', backref='resultados_niveles')
    
    def __init__(self, id_resultado, id_nivel, observaciones=None):
        self.id_resultado = id_resultado
        self.id_nivel = id_nivel
        self.observaciones = observaciones
        self.id_resultadonivelconc = f"{id_resultado}_{id_nivel}"