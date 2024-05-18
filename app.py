from flask import Flask
from utils.db import db
from services.estudiantes import estudiantes_routes
#from services.especialistas import especialistas
#from flask_sqlalchemy import SQLAlchemy
from config import DATABASE_CONNECTION

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SQLAlchemy(app)

db.init_app(app) 
app.register_blueprint(estudiantes_routes)
#app.register_blueprint(especialistas)

with app.app_context():  # se ejecuta si la clase contacts no existiera
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
