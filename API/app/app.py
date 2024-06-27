from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_cors import CORS
from .reviews.routes import reviews_bp
from .reservas.routes import reservas_bp
from .users.routes import users_bp
from .habitaciones.routes import habitaciones_bp
import logging

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#Creacion de engine
try:
    engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
    app.config['engine'] = engine
except Exception as e:
    print(f"Error connecting to the database: {e}")

# Define la URL del frontend
frontend_url = "http://localhost:5001"
# Configura CORS para permitir conexiones desde el frontend a la ruta '/reviews'
CORS(app, resources={r"/reviews/*": {"origins": frontend_url}})

logging.basicConfig(level=logging.INFO)

#Registrar todos los blueprint
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(habitaciones_bp, url_prefix='/habitaciones')

if __name__ == "__main__":
    app.run(host='127.0.0.0', port=5000, debug=True) 
