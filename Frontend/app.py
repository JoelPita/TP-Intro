from flask import Flask, render_template
import requests

from blueprints.weatherAPI.weather import weatherBp
from blueprints.contacto.contacto import contactoBp
from blueprints.reserva.reserva import reservaBp
from blueprints.gestion_reservas.gestion_reserva import gestionReservaBp
from blueprints.admin.reviews import admin_reviewsBp
from blueprints.reviews.reviews import reviewsBp

app = Flask(__name__)
app.register_blueprint(weatherBp)
app.register_blueprint(contactoBp, url_prefix="/contacto")
app.register_blueprint(reservaBp, url_prefix="/reserva")
app.register_blueprint(gestionReservaBp, url_prefix="/gestion_reservas")
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

@app.route('/actualizar_precios', methods = ['GET'])
def modificar_precios_habitaciones():
    obtener_habitaciones = 'http://127.0.0.1:5000/gestion_precios/obtener-habitaciones' #se reemplazara por el endpoint correspondiente cuando esté disponible
                    #no logro que funcione con url_for('gestion_precios.obtener_habitaciones', _external=True)
    try:                       
        response = requests.get(obtener_habitaciones)
        if response.status_code == 200:
            datos = response.json()
            return render_template('gestion_precios.html', datos=datos)
        elif response.status_code == 404:
            return render_template('404.html')
        else:
            return render_template('404.html')  #deberia ser pagina de error 500
    except requests.RequestException:
        return render_template('404.html')      #deberia ser pagina de error 500
    
@app.route('/actualizar_precios', methods=['POST'])
def enviar_precios_habitaciones():
    id_habitacion = request.form['id']
    nuevo_precio = str(request.form['precio_noche'])
    actualizar_precio = 'http://127.0.0.1:5000/gestion_precios/gestion_precios'
                     #no logro que funcione con url_for('gestion_precios.actualizar_precios_habitaciones', _external=True)
    try:
        response = requests.patch(actualizar_precio, json={'id': id_habitacion, 'precio_noche': nuevo_precio})

        if response.status_code == 200:
            return redirect(url_for('modificar_precios_habitaciones', _external=True)) 
        elif response.status_code == 404:
            return render_template('404.html')
        else:
            return render_template('404.html') #deberia ser pagina de error 500
    except requests.RequestException:
        return render_template('404.html')     #deberia ser pagina de error 500

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)