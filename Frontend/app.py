import os
from flask import Flask, flash, jsonify, make_response, request, render_template, url_for, redirect
import smtplib
from email.mime.text import MIMEText
import requests
from blueprints.weatherAPI.weather import weatherBp
from blueprints.contacto.contacto import contactoBp
from blueprints.admin.admin import adminBp
from blueprints.index.index import indexBp
from blueprints.reservas.reserva import reservasBp
from blueprints.reviews.reviews import reviewsBp

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


@app.route('/panel_admin', methods=["GET"])
def panel_admin():
    return render_template('panel_administrador.html')

@app.route('/admin', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        api_url = api_URL('users/validar_credenciales')  # Endpoint de la API para el login de admin
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("success"):
                    rol = response_data.get("rol")
                    if rol == "admin":
                        resp = make_response(redirect(url_for('panel_admin')))
                        resp.set_cookie('rol', 'admin')
                        return resp
                    else:
                        flash("Su usuario no tiene permisos para acceder a la administración.")
                else:
                    flash("Credenciales incorrectas. Por favor, inténtelo de nuevo.")
            elif response.status_code == 401:
                flash("Credenciales incorrectas. Por favor, inténtelo de nuevo.")
            elif response.status_code == 404:
                flash("Usuario no encontrado.")
            else:
                flash("Error al iniciar sesión. Intentelo nuevamente")

        except requests.exceptions.RequestException as e:
            flash("Error del servidor al iniciar sesión. Intentelo nuevamente")
    
    # Verificar si el usuario ya está autenticado como admin
    rol = request.cookies.get('rol')
    if rol == 'admin':
        return redirect(url_for('panel_admin'))
    
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

@app.route('/contacto', methods=["GET", "POST"])
def contacto():
    if request.method == "POST":
        nombre = request.form.get("name")
        email = request.form.get("email")
        asunto = request.form.get("subject")
        mensaje_contenido = request.form.get("message")

        mensaje_completo = (f"NOMBRE: {nombre}\n"
                            f"MAIL: {email}\n"
                            f"MENSAJE:\n{mensaje_contenido}")

        mensaje = MIMEText(mensaje_completo)
        mensaje["Subject"] = asunto
        mensaje["From"] = "hotel.glaciar.argentina@gmail.com"
        mensaje["To"] = "hotel.glaciar.argentina@gmail.com"
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
            smtp_server.login("hotel.glaciar.argentina@gmail.com", "oqvu xdib bmnp ymzy")
            smtp_server.sendmail("hotel.glaciar.argentina@gmail.com", "hotel.glaciar.argentina@gmail.com", mensaje.as_string())

        return render_template('contacto.html')
    return render_template('contacto.html')



@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/admin/reviews', methods=['GET'])
def admin_reviews():
    # Hardcodeo la vista por si falla la API
    fallback_reviews = [
    {"id": 00, "nombre_autor": "ERROR", "texto":  "La API no pudo conectarse."},
    {"id": 00, "nombre_autor": "ERROR", "texto":  "La API no pudo conectarse."},
    {"id": 00, "nombre_autor": "ERROR", "texto":  "La API no pudo conectarse."}
    ]
    try:
        # Obtengo las reviews desde la API
        response = requests.get(api_URL('reviews/'))
        my_reviews = response.json()
        return render_template('admin_reviews.html', reviews=my_reviews)
    except requests.exceptions.RequestException as e:
        return render_template('admin_reviews.html', reviews=fallback_reviews)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)