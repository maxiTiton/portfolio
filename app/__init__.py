from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()  # Esto es fundamental para cargar las variables de entorno desde .env

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    app.config.from_mapping(
        SENDGRID_KEY=os.environ.get('SENDGRID_KEY'),
    )

    # Cambiar import relativo por import absoluto
    from app import portfolio
    app.register_blueprint(portfolio.bp)

    return app