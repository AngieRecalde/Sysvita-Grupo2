from utils.ma import ma
from model.personas import Personas
from marshmallow import fields
from schemas.ubigeos_schema import UbigeosSchema
class PersonasSchema(ma.Schema):
    class Meta:
        model = Personas
        fields = ('id_persona',
                  'id_ubigeo',
                  'nombres',
                  'apellidos',
                  'fecha_registro',
                  'telefono',
                  'edad',
                  'fechaupdatepers')
    ubigeo = ma.Nested(UbigeosSchema)    
persona_schema = PersonasSchema()
personas_schema = PersonasSchema(many=True)