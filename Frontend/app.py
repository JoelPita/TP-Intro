import os
from flask import Flask, flash, jsonify, make_response, request, render_template, url_for, redirect, current_app
import smtplib
from email.mime.text import MIMEText
import requests
from blueprints.weatherAPI.weather import weatherBp
from blueprints.contacto.contacto import contactoBp
from blueprints.admin.admin import adminBp
from blueprints.index.index import indexBp
from blueprints.reservas.reserva import reservasBp
from blueprints.reviews.reviews import reviewsBp
from blueprints.nosotros.nosotros import nosotrosBp
from flask_login import LoginManager

app = Flask(__name__)
# Configurar la ruta de la API
app.config['API_ROUTE'] = 'http://127.0.0.0:5000/'

app.secret_key = os.urandom(24)

 

app.register_blueprint(weatherBp)
app.register_blueprint(contactoBp, url_prefix="/contacto")
app.register_blueprint(adminBp, url_prefix="/admin")
app.register_blueprint(indexBp, url_prefix='/')
app.register_blueprint(reservasBp, url_prefix="/reserva")
app.register_blueprint(reviewsBp, url_prefix="/reviews")
app.register_blueprint(nosotrosBp, url_prefix="/nosotros")


@app.route('/panel_admin', methods=["GET"])
def panel_admin():
    return render_template('panel_administrador.html')

@app.route('/habitaciones')
def habitaciones():
    return render_template('habitaciones.html')

@app.route('/habitaciones/<id>', methods = ['GET'])
def habitaciones_id(id):
    return render_template('habitacion.html', id=id)

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/nosotros')
def sobre_nosotros():
    return render_template('nosotros.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil.html')

@app.route('/registrar_usuario', methods=["GET", "POST"])
def registrar_usuario():
    if request.method == "POST":

        data = {
            'name': request.form['name'],
            'email': request.form['email'],
            'password': request.form['password'],
            'rol': 'user'
        }

        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "users/add"
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("success"):
                    flash("Su usuario fue creado exitosamente.")
                else:
                    flash("No se pudo crear el usuario. Por favor, inténtelo de nuevo.")
        except requests.exceptions.RequestException as e:
            flash("Error del servidor al iniciar sesión. Intentelo nuevamente")
        return render_template('registrar_usuario.html')
    return render_template('registrar_usuario.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
