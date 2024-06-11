from utils.ma import ma
from model.especialistas import Especialistas
from marshmallow import fields


class EspecialistasSchema(ma.Schema):
    class Meta:
        model = Especialistas
        fields = ('id_especialista','nombre','especialidad','email','telefono','fecha_registro','password')

<<<<<<< HEAD
especialista_schema = EspecialistasSchema()
especialistas_schema = EspecialistasSchema(many=True)
=======
especilista_schema = EspecialistasSchema()
especilistas_schema = EspecialistasSchema(many=True)
>>>>>>> 883ebaab710f856466d6edf4802aa0275b06d549
