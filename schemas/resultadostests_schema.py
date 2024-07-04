from utils.ma import ma
from model.resultadostests import ResultadosTests
from schemas.usuarios_schema import UsuariosSchema
from schemas.tests_schema import TestsSchema
from marshmallow import fields

class ResultadosTestsSchema(ma.Schema):
    class Meta:
        model = ResultadosTests
        fields = ('id_resultado','id_test','id_usuario','fecha_realizacion','respuestas','puntaje')
    usuario = ma.Nested(UsuariosSchema)
    test2= ma.Nested(TestsSchema)
resultadostest_schema = ResultadosTestsSchema()
resultadostests_schema = ResultadosTestsSchema(many=True)