from flask import Blueprint, flash, jsonify, request, render_template, url_for, redirect
from utils import api_URL
import requests

reservasBp = Blueprint("reservasBp", __name__, template_folder='templates')

@reservasBp.route('/', methods=["GET", "POST"])
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
            'habitacion_id': request.form['habitacion_id']
        }
        api_url = api_URL('reservas')
        headers = {'Content-Type': 'application/json'}
        
        response = requests.post(api_url, json=data, headers=headers)
        if response.status_code == 200:
            codigo_reserva = response.json().get("codigo_reserva")
            return render_template('confirmacion_reserva.html', codigo_reserva=codigo_reserva)
        else:
            flash("Error al crear la reserva: " + response.json().get("message", ""))
            return render_template('reserva.html')
    
    return render_template('reserva.html')

@reservasBp.route('/gestion_reservas')
def gestion_reservas():
    rol = request.cookies.get('rol')
    if rol == 'admin':
        api_url = api_URL('reservas')
        response = requests.get(api_url)
        if response.status_code == 200:
            reservas = response.json().get("reservas", [])
            return render_template('gestion_reservas.html', reservas=reservas)
        else:
            return jsonify({"message": "Error al obtener las reservas"}), 500
    return redirect(url_for('admin'))

    

@reservasBp.route('/estado_reserva')
def estado_reserva():
    api_url = api_URL('reservas')
    response = requests.get(api_url)
    if response.status_code == 200:
        reservas = response.json().get("reservas", [])
        return render_template('gestion_reservas.html', reservas=reservas)
    else:
        return jsonify({"message": "Error al obtener las reservas"}), 500