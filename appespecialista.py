from flask import Flask
from utils.db import db
from services.especialista_routes import especialista_routes
#from services.especialistas import especialistas
#from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION

appespecialista = Flask(__name__)
appespecialista.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
appespecialista.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLAlchemy(app)

db.init_app(appespecialista) 
appespecialista.register_blueprint(especialista_routes)
#app.register_blueprint(especialistas)

with appespecialista.app_context():  # se ejecuta si la clase contacts no existiera
    db.create_all()

if __name__ == '__main__':
    appespecialista.run(host='0.0.0.0', debug=True, port=5000)