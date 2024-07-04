from utils.ma import ma
from model.tests import Tests
from marshmallow import fields

class TestsSchema(ma.Schema):
    class Meta:
        model = Tests
        fields = ('id_test','nombre_test','descripcion','tipo_test')
test_schema = TestsSchema()
tests_schema = TestsSchema(many=True)