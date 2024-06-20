from utils.ma import ma
from model.estudiantes import Estudiantes
from marshmallow import fields
from schemas.usuarios_schema import UsuarioSchema
class EstudiantesSchema(ma.Schema):
    class Meta:
        model = Estudiantes
        fields = ('id_estudiante','id_usuario','nombre','genero','fecha_registro','edad','telefono','carrera')
    usuario = ma.Nested(UsuarioSchema)    
estudiante_schema = EstudiantesSchema()
estudiantes_schema = EstudiantesSchema(many=True)