from flask import Flask, jsonify, request, render_template, url_for, redirect
import smtplib
from email.mime.text import MIMEText
import requests
import datetime
"""
    Constantes esenciales para la construcción de la URL de la API del clima.
"""
API_KEY = "dbec3add72c6ecd469b009ae31e34fb5"
LATITUD = "-50.33943088470253"
LONGITUD = "-72.25593247083323"
UNIDAD = "metric"

app = Flask(__name__)

"""
    Método que se encarga de la comunicación con el servicio de Open Weather y se obtiene
    el pronósitico de la fecha actual.
    Se filtra los datos extra y se toman los útiles.
    Retorna un json response válida para enviar al cliente o navegador.
"""
@app.route('/clima_actual')
def obtener_clima_actual():
    url = "https://api.openweathermap.org/data/2.5/weather?"
    parametros = {
        'lat': LATITUD,
        'lon': LONGITUD,
        'appid': API_KEY,
        'units': UNIDAD,
    }
    current_response = requests.get(url, params=parametros)
    data = current_response.json()
    current_weather = {
        'temperatura': data['main']['temp'],
        'temperatura_minima': data['main']['temp_min'],
        'temperatura_maxima': data['main']['temp_max'],
        'velocidad_viento': data['wind']['speed'],
        'humedad': data['main']['humidity'],
        'ciudad': data['name'],
        'estado': data['weather'][0]['main']       
    }
    return jsonify(current_weather)

"""
    Método que se encarga de la comunicación con el servicio de Open Weather con los datos requeridos.
    Se Obtiene el pronóstico de los siguiente cuatro días.
    Se filtra los datos extra y se toman los útiles.
    Retorna un json response válida para enviar al cliente o navegador.
"""
@app.route('/pronostico_clima')
def obtener_pronostico():
    url = "https://api.openweathermap.org/data/2.5/forecast?" + "cnt=40"
    parametros = {
        'lat': LATITUD,
        'lon': LONGITUD,
        'appid': API_KEY,
        'units': UNIDAD,
    }
    forecast_response = requests.get(url, params=parametros)
    forecast_data = forecast_response.json()
    forecast_weather = {}
    for i in range (8, 40, 8):
        fecha_iso = forecast_data['list'][i]['dt_txt']
        fecha_formateada = datetime.datetime.strptime(fecha_iso, "%Y-%m-%d %H:%M:%S")
        dias_español = ["Lun", "Mar", "Miér", "Jue", "Vier", "Sáb", "Dom"]
        dia = dias_español[fecha_formateada.weekday()]

        forecast_weather[dia] = {
            'temperatura_minima': forecast_data['list'][i]['main']['temp_min'],
            'temperatura_maxima': forecast_data['list'][i]['main']['temp_max'],
            'estado': forecast_data['list'][i]['weather'][0]['main']
        }
    return jsonify(forecast_weather)
    
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

@app.route('/reserva', methods=["GET", "POST"])
def reserva():
    if request.method == "POST":
        data = {
            'email_cliente': request.form['email_cliente'],
            'nombre_cliente': request.form['nombre_cliente'],
            'telefono_cliente': request.form['telefono_cliente'],
            'fecha_desde': request.form['fecha_desde'],
            'fecha_hasta': request.form['fecha_hasta'],
            'cantidad_habitaciones': request.form['cantidad_habitaciones'],
            'cantidad_personas': request.form['cantidad_personas'],
            'metodo_pago': request.form['metodo_pago'],
            'estado': "Pendiente",  # Estado predeterminado
            'habitacion_id': request.form['habitacion_id'],
            'precio_total': 0  # to do: calcular precio total
        }
        print("Datos recibidos del formulario:", data)
        api_url = "http://127.0.0.1:5000/reservas"
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(api_url, json=data, headers=headers)
        print("Respuesta de la API:", response.status_code, response.text)
        
        if response.status_code == 200:
            return render_template('confirmacion_reserva.html')
        else:
            return jsonify({"message": "Error al crear la reserva"}), 500
    
    return render_template('reserva.html')

@app.route('/gestion_reservas')
def gestion_reservas():
    api_url = "http://127.0.0.1:5000/reservas"
    response = requests.get(api_url)
    if response.status_code == 200:
        reservas = response.json().get("reservas", [])
        return render_template('gestion_reservas.html', reservas=reservas)
    else:
        return jsonify({"message": "Error al obtener las reservas"}), 500

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5001, debug=True)