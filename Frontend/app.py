from flask import Flask, render_template
import requests

from blueprints.weatherAPI.weather import weatherBp
from blueprints.contacto.contacto import contactoBp
from blueprints.reserva.reserva import reservaBp
from blueprints.gestion_reservas.gestion_reserva import gestionReservaBp
from blueprints.gestion_precios.gestion_precios import gestionPreciosBp
from blueprints.admin.reviews import admin_reviewsBp
from blueprints.reviews.reviews import reviewsBp

app = Flask(__name__)
app.register_blueprint(weatherBp)
app.register_blueprint(contactoBp, url_prefix="/contacto")
app.register_blueprint(reservaBp, url_prefix="/reserva")
app.register_blueprint(gestionReservaBp, url_prefix="/gestion_reservas")
app.register_blueprint(gestionPreciosBp, url_prefix="/gestion_precios")
app.register_blueprint(admin_reviewsBp, url_prefix="/admin/reviews")
app.register_blueprint(reviewsBp, url_prefix="/reviews")

@app.route('/')
def home():
    return render_template('home.html')

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


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)