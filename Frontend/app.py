from flask import Flask, render_template
import requests

from blueprints.weatherAPI.weather import weatherBp
from blueprints.contacto.contacto import contactoBp
from blueprints.reserva.reserva import reservaBp
from blueprints.gestion_reservas.gestion_reserva import gestionReservaBp
from blueprints.admin.reviews import admin_reviewsBp
from blueprints.reviews.reviews import reviewsBp
from blueprints.nosotros.nosotros import nosotrosBp

app = Flask(__name__)
app.register_blueprint(weatherBp)
app.register_blueprint(contactoBp, url_prefix="/contacto")
app.register_blueprint(reservaBp, url_prefix="/reserva")
app.register_blueprint(gestionReservaBp, url_prefix="/gestion_reservas")
app.register_blueprint(admin_reviewsBp, url_prefix="/admin/reviews")
app.register_blueprint(reviewsBp, url_prefix="/reviews")
app.register_blueprint(nosotrosBp, url_prefix="/nosotros")

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
    return render_template('habitacion.html', id=id)

@app.route('/servicios')
def servicios():
    return render_template('servicios.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.route('/nosotros')
def sobre_nosotros():
    return render_template('nosotros.html')


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)
