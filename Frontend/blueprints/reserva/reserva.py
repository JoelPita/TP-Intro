from flask import Blueprint, jsonify, request, render_template, url_for, redirect
from utils import api_URL
import requests

reservaBp = Blueprint("reservaBp", __name__, template_folder='templates')

@reservaBp.route('/', methods=["GET", "POST"])
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
        api_url = api_URL('reservas')
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(api_url, json=data, headers=headers)
        print("Respuesta de la API:", response.status_code, response.text)
        
        if response.status_code == 200:
            return render_template('confirmacion_reserva.html')
        else:
            return jsonify({"message": "Error al crear la reserva"}), 500
    
    return render_template('reserva.html')