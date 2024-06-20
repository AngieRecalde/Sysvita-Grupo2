from flask import Flask
from flask_cors import CORS
from utils.db import db
from services.estudiante_routes import estudiante_routes
from services.especialista_routes import especialista_routes
from services.preguntasrespuestas import preguntas_respuestas
#from services.especialistas import especialistas
#from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION
from flask_cors import CORS
app = Flask(__name__)
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800

db.init_app(app)
app.register_blueprint(estudiante_routes)
app.register_blueprint(especialista_routes)
app.register_blueprint(preguntas_respuestas)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
