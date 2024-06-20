from utils.ma import ma
from model.tests import Tests
from marshmallow import fields
from schemas.estudiantes_schema import EstudiantesSchema
class TestSchema(ma.Schema):
    class Meta:
        model = Tests
        fields = ('id_test','id_estudiante','fecha_test','tipo_test')
    testsestudi = ma.Nested(EstudiantesSchema)    
test_schema = TestSchema()
tests_schema = TestSchema(many=True)