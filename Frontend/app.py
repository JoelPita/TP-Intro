from flask import Flask, jsonify, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
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
engine = create_engine('mysql+mysqlconnector://app_user:appMate123@db/flaskdb')

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