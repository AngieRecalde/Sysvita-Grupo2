from flask import Blueprint, jsonify, request
from model.comunicaciones import Comunicaciones
from model.evaluacion_especialistas import Evaluacion_Especialistas
from model.tests import Tests
from model.preguntas import Preguntas
from model.alternativas import Alternativas
from model.resultadostests import ResultadosTests
from model.resultadosniveles import ResultadosNiveles
from model.niveles import Niveles
from model.tratamientos import Tratamientos
from utils.db import db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from model.usuarios import Usuarios
from model.personas import Personas
from model.ubigeos import Ubigeos
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

test_routes = Blueprint('test_routes', __name__)

@test_routes.route('/cargar_test/<int:id_test>', methods=['GET'])
def cargar_test(id_test):
    try:
        test = Tests.query.get(id_test)
        if not test:
            return jsonify({'message': 'Test no encontrado'}), 404

        preguntas = Preguntas.query.filter_by(id_test=id_test).order_by(Preguntas.orden).all()

        resultado = {
            "descripcion": test.descripcion,
            "id_test": test.id_test,
            "nombre_test": f"{test.nombre_test}-{test.tipo_test}",
            "preguntas": []
        }

        for pregunta in preguntas:
            alternativas = Alternativas.query.filter_by(id_pregunta=pregunta.id_pregunta).all()
            
            pregunta_data = {
                "orden": pregunta.orden,
                "texto_pregunta": pregunta.texto_pregunta,
                "alternativas": [
                    {
                        "texto_opcion": alt.texto_opcion,
                        "valor": alt.valor
                    } for alt in alternativas
                ]
            }
            resultado['preguntas'].append(pregunta_data)

        return jsonify(resultado), 200

    except SQLAlchemyError as e:
        return jsonify({
            'message': 'Error al cargar el test',
            'error': str(e)
        }), 500
    

    
@test_routes.route('/respuestas/<int:test_id>', methods=['POST'])
def realizar_test(test_id):
    try:
        data = request.json
        id_usuario = data.get('id_usuario')
        respuestas = data.get('respuestas')

        if not id_usuario or not respuestas:
            return jsonify({'message': 'Faltan datos requeridos'}), 400

        # Definir configuraciones específicas para cada test
        test_configs = {
            1: {'num_respuestas': 22, 'positivas': [1,3,5,7,8,11,14,16,17,20,22], 'negativas': [2,4,6,9,10,12,13,15,18,19,21], 'niveles': [(47, 1), (36, 2), (0, 3)]},
            2: {'num_respuestas': 20, 'positivas': [1,2,6,8,9,10,13,15,18,20], 'negativas': [3,4,5,7,11,12,14,16,17,19], 'niveles': [(43, 1), (34, 2), (0, 3)]},
            3: {'num_respuestas': 20, 'positivas': [3,4,6,7,9,12,13,14,17,18], 'negativas': [1,2,5,8,10,11,15,16,19,20], 'niveles': [(40, 4), (21, 5), (0, 6)]},
            4: {'num_respuestas': 20, 'positivas': [2,3,4,5,8,9,11,12,14,15,17,18,20], 'negativas': [1,6,7,10,13,16,19], 'niveles': [(40, 4), (21, 5), (0, 6)]}
        }

        config = test_configs.get(test_id)
        if not config:
            return jsonify({'message': 'ID de test no válido'}), 400

        if len(respuestas) != config['num_respuestas']:
            return jsonify({'message': f'El número de respuestas debe ser {config["num_respuestas"]}'}), 400

        # Calcular puntuación
        puntuacion_positiva = sum(int(respuestas[i-1]) for i in config['positivas'])
        puntuacion_negativa = sum(5 - int(respuestas[i-1]) if test_id == 3 else int(respuestas[i-1]) for i in config['negativas'])
        puntuacion_total = puntuacion_positiva + puntuacion_negativa

        # Determinar el nivel
        id_nivel = next(nivel for umbral, nivel in config['niveles'] if puntuacion_total >= umbral)

        # Guardar resultado en la tabla ResultadosTests
        nuevo_resultado = ResultadosTests(
            id_test=test_id,
            id_usuario=id_usuario,
            fecha_realizacion=db.func.current_timestamp(),
            respuestas=''.join(respuestas),
            puntaje=puntuacion_total
        )
        db.session.add(nuevo_resultado)
        db.session.flush()

        # Guardar resultado en la tabla ResultadosNiveles
        nuevo_resultado_nivel = ResultadosNiveles(
            id_resultado=nuevo_resultado.id_resultado,
            id_nivel=id_nivel,
            observaciones=f"Puntuación total: {puntuacion_total}"
        )
        db.session.add(nuevo_resultado_nivel)

        # Crear entradas en blanco para Evaluacion_Especialistas, Tratamientos y Comunicaciones
        nueva_evaluacion = Evaluacion_Especialistas(
        id_resultado=nuevo_resultado.id_resultado,
        id_especialista=None,  # Inicialmente null
        diagnostico='',
        fundamentacion=''
        )
        db.session.add(nueva_evaluacion)
        db.session.flush()
        nuevo_tratamiento = Tratamientos(
            id_evaluacion=nueva_evaluacion.id_evaluacion,
            descripcion=''
        )
        db.session.add(nuevo_tratamiento)

        nueva_comunicacion = Comunicaciones(
            id_evaluacion=nueva_evaluacion.id_evaluacion,
            recomendacion=''
        )
        db.session.add(nueva_comunicacion)

        db.session.commit()

        # Obtener información del nivel
        nivel = Niveles.query.get(id_nivel)

        return jsonify({
            'message': f'Test completado exitosamente',
            'puntuacion_total': puntuacion_total,
            'nivel': nivel.nombre_nivel,
            'color': nivel.color
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error al procesar el test',
            'error': str(e)
        }), 500


@test_routes.route('/actualizar_evaluacion/<int:id_resultado>', methods=['PUT'])
def actualizar_evaluacion(id_resultado):
    try:
        data = request.json
        diagnostico = data.get('diagnostico')
        fundamentacion = data.get('fundamentacion')
        descripcion_tratamiento = data.get('descripcion_tratamiento')
        recomendacion = data.get('recomendacion')
        id_especialista = data.get('id_especialista')  # Nuevo campo

        # Actualizar Evaluacion_Especialistas
        evaluacion = Evaluacion_Especialistas.query.filter_by(id_resultado=id_resultado).first()
        if not evaluacion:
            return jsonify({'message': 'Evaluación no encontrada'}), 404

        evaluacion.diagnostico = diagnostico
        evaluacion.fundamentacion = fundamentacion
        if id_especialista:
            evaluacion.id_especialista = id_especialista  # Asignar o actualizar id_especialista

        # Actualizar Tratamientos
        tratamiento = Tratamientos.query.filter_by(id_evaluacion=evaluacion.id_evaluacion).first()
        if tratamiento:
            tratamiento.descripcion = descripcion_tratamiento
        else:
            nuevo_tratamiento = Tratamientos(id_evaluacion=evaluacion.id_evaluacion, descripcion=descripcion_tratamiento)
            db.session.add(nuevo_tratamiento)

        # Actualizar Comunicaciones
        comunicacion = Comunicaciones.query.filter_by(id_evaluacion=evaluacion.id_evaluacion).first()
        if comunicacion:
            comunicacion.recomendacion = recomendacion
        else:
            nueva_comunicacion = Comunicaciones(id_evaluacion=evaluacion.id_evaluacion, recomendacion=recomendacion)
            db.session.add(nueva_comunicacion)

        db.session.commit()

        return jsonify({
            'message': 'Evaluación actualizada exitosamente',
            'id_resultado': id_resultado
        }), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({
            'message': 'Error al actualizar la evaluación',
            'error': str(e)
        }), 500

@test_routes.route('/obtener_tests', methods=['GET'])
def obtener_tests():
    try:
        tests = Tests.query.all()
        tests_data = [
            {
                'id': test.id_test,
                'nombre': f"{test.nombre_test}-{test.tipo_test}"
            }
            for test in tests
        ]
        return jsonify(tests_data), 200
    except SQLAlchemyError as e:
        return jsonify({
            'message': 'Error al obtener los tests',
            'error': str(e)
        }), 500


from sqlalchemy import func

@test_routes.route('/resultados_especialista', methods=['GET'])
def obtener_resultados_especialista():
    try:
        resultados = db.session.query(
            ResultadosTests.id_resultado,
            Usuarios.email,
            ResultadosTests.puntaje,
            ResultadosNiveles.id_nivel,
            Niveles.nombre_nivel,
            Niveles.color,
            func.max(ResultadosTests.fecha_realizacion).label('fecha_realizacion'),
            Personas.nombres,
            Personas.apellidos,
            Personas.id_ubigeo,
            Ubigeos.departamento,
            Ubigeos.provincia,
            Tests.nombre_test,
            Tests.tipo_test,
            Ubigeos.distrito
        ).join(
            Usuarios, Usuarios.id_usuario == ResultadosTests.id_usuario
        ).join(
            Personas, Personas.id_persona == Usuarios.id_persona
        ).join(
            Ubigeos, Ubigeos.id_ubigeo == Personas.id_ubigeo
        ).join(
            ResultadosNiveles, ResultadosNiveles.id_resultado == ResultadosTests.id_resultado
        ).join(
            Niveles, Niveles.id_nivel == ResultadosNiveles.id_nivel
        ).join(
            Tests, Tests.id_test == ResultadosTests.id_test
        ).group_by(
            ResultadosTests.id_resultado,
            Usuarios.email,
            ResultadosTests.puntaje,
            ResultadosNiveles.id_nivel,
            Niveles.nombre_nivel,
            Niveles.color,
            Personas.nombres,
            Personas.apellidos,
            Personas.id_ubigeo,
            Ubigeos.departamento,
            Ubigeos.provincia,
            Tests.nombre_test,
            Tests.tipo_test,
            Ubigeos.distrito
        ).all()

        formatted_results = []
        for resultado in resultados:
            formatted_results.append({
                'id_resultado': resultado.id_resultado,
                'email': resultado.email,
                'nombres': resultado.nombres,
                'apellidos': resultado.apellidos,
                'nombre_test': resultado.nombre_test,
                'tipo_test': resultado.tipo_test,
                'fecha_realizacion': resultado.fecha_realizacion.strftime('%Y-%m-%d %H:%M:%S'),
                'id_ubigeo': resultado.id_ubigeo,
                'ubigeo': f"{resultado.departamento}, {resultado.provincia}, {resultado.distrito}",
                'puntaje': resultado.puntaje,
                'nivel': resultado.nombre_nivel,
                'color': resultado.color
            })

        return jsonify(formatted_results), 200

    except Exception as e:
        return jsonify({
            'message': 'Error al obtener los resultados',
            'error': str(e)
        }), 500

@test_routes.route('/obtener_evaluacion/<int:id_resultado>', methods=['GET'])
def obtener_evaluacion(id_resultado):
    try:
        # Obtener el resultado del test
        resultado_test = ResultadosTests.query.get(id_resultado)
        if not resultado_test:
            return jsonify({'message': 'Resultado no encontrado'}), 404

        # Obtener datos relacionados
        usuario = Usuarios.query.get(resultado_test.id_usuario)
        persona = Personas.query.get(usuario.id_persona)
        test = Tests.query.get(resultado_test.id_test)
        resultado_nivel = ResultadosNiveles.query.filter_by(id_resultado=id_resultado).first()
        nivel = Niveles.query.get(resultado_nivel.id_nivel)
        evaluacion = Evaluacion_Especialistas.query.filter_by(id_resultado=id_resultado).first()
        tratamiento = Tratamientos.query.filter_by(id_evaluacion=evaluacion.id_evaluacion).first() if evaluacion else None
        comunicacion = Comunicaciones.query.filter_by(id_evaluacion=evaluacion.id_evaluacion).first() if evaluacion else None

        # Construir la respuesta
        respuesta = {
            'apellidos_y_nombres': f"{persona.apellidos} {persona.nombres}",
            'edad': persona.edad,
            'telefono': persona.telefono,
            'email': usuario.email,
            'tipo_test': f"{test.nombre_test}-{test.tipo_test}",
            'score': resultado_test.puntaje,
            'nivel': nivel.nombre_nivel,
            'diagnostico': evaluacion.diagnostico if evaluacion else '',
            'fundamentacion': evaluacion.fundamentacion if evaluacion else '',
            'descripcion_tratamiento': tratamiento.descripcion if tratamiento else '',
            'recomendacion': comunicacion.recomendacion if comunicacion else ''
        }

        return jsonify(respuesta), 200

    except SQLAlchemyError as e:
        return jsonify({
            'message': 'Error al obtener los datos de la evaluación',
            'error': str(e)
        }), 500
    

@test_routes.route('/notificar_paciente/<int:id_resultado>', methods=['POST'])
def notificar_paciente(id_resultado):
    try:
        print(f"Buscando resultado con id {id_resultado}")
        resultado = ResultadosTests.query.get(id_resultado)
        if not resultado:
            print(f"Resultado con id {id_resultado} no encontrado")
            return jsonify({'message': 'Resultado no encontrado'}), 404

        print(f"Buscando evaluación para el resultado con id {id_resultado}")
        evaluacion = Evaluacion_Especialistas.query.filter_by(id_resultado=id_resultado).first()
        if not evaluacion:
            print(f"Evaluación para el resultado con id {id_resultado} no encontrada")
            return jsonify({'message': 'Evaluación no encontrada'}), 404

        print(f"Buscando usuario del paciente con id {resultado.id_usuario}")
        usuario_paciente = Usuarios.query.filter_by(id_usuario=resultado.id_usuario).first()
        if not usuario_paciente:
            print(f"Usuario paciente con id {resultado.id_usuario} no encontrado")
            return jsonify({'message': 'Usuario paciente no encontrado'}), 404

        persona_paciente = Personas.query.get(usuario_paciente.id_persona)
        if not persona_paciente:
            print(f"Persona paciente con id {usuario_paciente.id_persona} no encontrada")
            return jsonify({'message': 'Persona paciente no encontrada'}), 404

        email_paciente = usuario_paciente.email
        
        print(f"Buscando comunicación para la evaluación con id {evaluacion.id_evaluacion}")
        comunicacion = Comunicaciones.query.filter_by(id_evaluacion=evaluacion.id_evaluacion).first()
        if not comunicacion:
            print(f"Comunicación para la evaluación con id {evaluacion.id_evaluacion} no encontrada")
            return jsonify({'message': 'Comunicación no encontrada'}), 404

        # Configuración del correo de la empresa
        sender_email = "sysvitacitas@gmail.com"  # Correo de la empresa
        sender_password = "wnbo ddsz noma tggt"  # Esto debería manejarse de forma segura

        message = MIMEMultipart("alternative")
        message["Subject"] = "Recomendación de tu evaluación - SYSVITA"
        message["From"] = sender_email
        message["To"] = email_paciente

        text = f"""
        Estimado/a {persona_paciente.nombres} {persona_paciente.apellidos},

        El especialista ha realizado una evaluación de tu test reciente.

        Recomendación:
        {comunicacion.recomendacion}

        Por favor, no dudes en contactarnos si tienes alguna pregunta.

        Saludos cordiales,
        El equipo de SYSVITA
        """

        part1 = MIMEText(text, "plain")
        message.attach(part1)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            try:
                server.login(sender_email, sender_password)
                server.sendmail(sender_email, email_paciente, message.as_string())
            except smtplib.SMTPAuthenticationError as auth_error:
                print(f"Error de autenticación SMTP: {str(auth_error)}")
                return jsonify({'message': 'Error de autenticación al enviar el correo', 'error': str(auth_error)}), 500

        return jsonify({'message': 'Notificación enviada con éxito'}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"Error de SQLAlchemy: {str(e)}")
        return jsonify({
            'message': 'Error al enviar la notificación',
            'error': str(e)
        }), 500
