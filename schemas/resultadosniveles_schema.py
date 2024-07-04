from utils.ma import ma
from model.resultadosniveles import ResultadosNiveles
from schemas.resultadostests_schema import ResultadosTestsSchema
from schemas.niveles_schema import NivelesSchema
from marshmallow import fields

class ResultadosNivelesSchema(ma.Schema):
    class Meta:
        model = ResultadosNiveles
        fields =('id_resultadonivelconc','id_resultado','id_nivel','observaciones')
    resultado = ma.Nested(ResultadosTestsSchema)
    niveles = ma.Nested(NivelesSchema)
resultadosnivel_schema = ResultadosNivelesSchema()
resultadosniveles_schema = ResultadosNivelesSchema(many=True)
