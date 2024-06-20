from flask import Blueprint, jsonify
from model.preguntas import Preguntas
from schemas.preguntas_schema import pregunta_schema

preguntas_respuestas = Blueprint('preguntas_respuestas', __name__)

@preguntas_respuestas.route('/preguntas/<int:id_test>', methods=['GET'])
def get_preguntas(id_test):
    result = {}

    preguntas = Preguntas.query.filter_by(id_test=id_test).all()
    preguntas_data = pregunta_schema.dump(preguntas, many=True)
    preguntas_data = []

    for pregunta in preguntas:
        pregunta_data = {
            "id_test": pregunta.id_test,
            "enunciado": pregunta.enunciado,
            "tipo_escala": pregunta.tipo_escala,
            "numero_pregunta": pregunta.numero_pregunta
        }
        preguntas_data.append(pregunta_data)

    result["preguntas"] = preguntas_data
    result["status_code"] = 200
    result["msg"] = "Se recuperaron las preguntas sin inconvenientes"

    return jsonify(result), 200