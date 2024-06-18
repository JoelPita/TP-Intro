from flask import Flask, render_template
import requests

from blueprints.weatherAPI.weather import weatherBp
from blueprints.contacto.contacto import contactoBp
from blueprints.reserva.reserva import reservaBp
from blueprints.gestion_reservas.gestion_reserva import gestionReservaBp
from blueprints.admin.admin import adminBp
from blueprints.index.index import indexBp
from blueprints.reviews.reviews import reviewsBp

app = Flask(__name__)
app.secret_key = b'unaClaveSecreta-34weDew4542dsdsggsdsg3333'

# Configurar la ruta de la API
app.config['API_ROUTE'] = 'http://127.0.0.0:5000/'

app.register_blueprint(weatherBp)
app.register_blueprint(contactoBp, url_prefix="/contacto")
app.register_blueprint(reservaBp, url_prefix="/reserva")
app.register_blueprint(gestionReservaBp, url_prefix="/gestion_reservas")
app.register_blueprint(adminBp, url_prefix="/admin")
app.register_blueprint(indexBp, url_prefix='/')
app.register_blueprint(reviewsBp, url_prefix='/reviews')


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
    app.run(host='127.0.0.1', port=5001, debug=True)