from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager  # Añade esta línea
from utils.db import db
from services.registro_routes import registro_routes
from services.tests import test_routes
from services.mapaubigeo import heatmap_routes
from config import DATABASE_CONNECTION
from flask_cors import CORS
app = Flask(__name__)
# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'SYSVIT@123'  # Cambia esto por una clave secreta segura
jwt = JWTManager(app)  # Añade esta línea
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_CONNECTION
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_POOL_SIZE"] = 20
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 30
app.config["SQLALCHEMY_POOL_RECYCLE"] = 1800

db.init_app(app)
app.register_blueprint(registro_routes)
app.register_blueprint(test_routes)
app.register_blueprint(heatmap_routes)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
