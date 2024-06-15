from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from .reviews.routes import reviews_bp
from .reservas.routes import reservas_bp
from .users.routes import users_bp
import logging

app = Flask(__name__)

#Creacion de engine
try:
    engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
    app.config['engine'] = engine
except Exception as e:
    print(f"Error connecting to the database: {e}")

#Registrar todos los blueprint
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(users_bp, url_prefix='/users')

if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 
