from flask import Flask, jsonify
from sqlalchemy import create_engine
from .reviews.routes import reviews_bp
from .reservas.routes import reservas_bp
from .users.routes import users_bp
from .gestion_precios.routes import gestion_precios_bp

app = Flask(__name__)

#Deberia estar en un try?
engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
app.config['engine'] = engine

#Registrar todos los blueprint
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(gestion_precios_bp, url_prefix='/gestion_precios')

#Esta podria estar en un archivo route
@app.route('/')
def home():
    return jsonify({"message": "Hello, Docker!"})


if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 
