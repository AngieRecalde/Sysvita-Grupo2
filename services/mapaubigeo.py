from flask import Blueprint, jsonify
from model.personas import Personas
from model.ubigeos import Ubigeos
from model.resultadostests import ResultadosTests
from model.niveles import Niveles
from model.resultadosniveles import ResultadosNiveles
from model.usuarios import Usuarios
from model.tests import Tests 
from utils.db import db

heatmap_routes = Blueprint("heatmap_routes", __name__)

@heatmap_routes.route("/mapacalor", methods=["GET"])
def get_heatmap_data():
    
    query = db.session.query(
        Personas, Ubigeos, ResultadosTests, Niveles, ResultadosNiveles, Tests
    ).join(
        Ubigeos, Personas.id_ubigeo == Ubigeos.id_ubigeo
    ).join(
        Usuarios, Usuarios.id_persona == Personas.id_persona
    ).join(
        ResultadosTests, ResultadosTests.id_usuario == Usuarios.id_usuario
    ).join(
        ResultadosNiveles, ResultadosNiveles.id_resultado == ResultadosTests.id_resultado
    ).join(
        Niveles, Niveles.id_nivel == ResultadosNiveles.id_nivel
    ).join(
        Tests, Tests.id_test == ResultadosTests.id_test
    ).all()

    # Procesar los datos para el mapa de calor
    heatmap_data = []
    for row in query:
        persona, ubigeo, resultado_test, nivel, resultado_nivel, test = row
        heatmap_data.append({
            "id_usuario": resultado_test.id_usuario,
            "nombres": persona.nombres,
            "apellidos": persona.apellidos,
            "latitud": float(ubigeo.y),
            "longitud": float(ubigeo.x),
            "fecha_realizacion": resultado_test.fecha_realizacion,
            "peso": 10,  
            "tipo_nivel": nivel.tipo_nivel,
            "nombre_nivel": nivel.nombre_nivel,
            "color": nivel.color,
            "nombre_test": test.nombre_test 
        })

    return jsonify(heatmap_data)
