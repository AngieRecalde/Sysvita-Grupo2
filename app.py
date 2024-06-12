from flask import Flask
import os
from dotenv import load_dotenv
from utils.db import db
from services.estudiante_routes import estudiante_routes
#from services.especialistas import especialistas
#from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION
def crear_app():
    app = Flask(__name__)
    # Configuración de la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # SQLAlchemy(app)

    db.init_app(app) 
    app.register_blueprint(estudiante_routes)
    with app.app_context():  # se ejecuta si la clase contacts no existiera
        db.create_all()
    return app

if __name__ == '__main__':
    app = crear_app()
    app.run(host='0.0.0.0', debug=True, port=5000)
