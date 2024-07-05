from dotenv import load_dotenv
import os

# Cargar variables de entorno del archivo .env si existe
load_dotenv()

# Usar os.environ.get() con valores por defecto para mayor seguridad
user = os.environ.get('DB_USER', 'default_user')
pwd = os.environ.get('DB_PASSWORD', 'default_password')
host = os.environ.get('DB_HOST', 'default_host')
database = os.environ.get('DB_NAME', 'default_database')
server = os.environ.get('DB_SERVER', 'postgresql')

DATABASE_CONNECTION = f'{server}://{user}:{pwd}@{host}/{database}'
