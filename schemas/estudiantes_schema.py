from utils.ma import ma
from model.estudiantes import Estudiantes
from marshmallow import fields

class EstudiantesSchema(ma.Schema):
    class Meta:
        model = Estudiantes
        fields = ('id_estudiante','nombre','genero','password','fecha_registro','edad','email','telefono','carrera')
        
estudiante_schema = EstudiantesSchema()
estudiantes_schema = EstudiantesSchema(many=True)