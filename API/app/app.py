from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from .reviews.routes import reviews_bp
from .reservas.routes import reservas_bp
from .users.routes import users_bp


app = Flask(__name__)

#Deberia estar en un try?
engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')
app.config['engine'] = engine

#Registrar todos los blueprint
app.register_blueprint(reviews_bp, url_prefix='/reviews')
app.register_blueprint(reservas_bp, url_prefix='/reservas')
app.register_blueprint(users_bp, url_prefix='/users')

#Esta podria estar en un archivo route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/habitaciones/<id>', methods = ['GET'])
def habitaciones_id(id):
    return


@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/contacto')
def contacto():
    return render_template('contacto.html')

@app.route('/reserva')
def reserva():
    return render_template('reserva.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == "__main__":
    app.run(host='127.0.0.0.0', port=5000, debug=True) 
