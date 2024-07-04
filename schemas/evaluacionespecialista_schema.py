from utils.ma import ma
from model.evaluacion_especialistas import Evaluacion_Especialistas
from schemas.resultadostests_schema import ResultadosTestsSchema
from schemas.especialistas_schema import EspecialistasSchema
from marshmallow import fields

class  Evaluacion_EspecialistasSchema(ma.Schema):
    class Meta:
        model =  Evaluacion_Especialistas
        fields = ('id_evaluacion','id_resultado','diagnostico','fundamentacion','id_especialista')
    resultadostests11= ma.Nested(ResultadosTestsSchema)
    especialista4 = ma.Nested(EspecialistasSchema)
evaluacion_especialista_schema = Evaluacion_EspecialistasSchema()
evaluacion_especialistas_schema= Evaluacion_EspecialistasSchema(many=True)