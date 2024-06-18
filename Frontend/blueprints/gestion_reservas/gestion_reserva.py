from flask import Blueprint, jsonify, request, render_template, url_for, redirect, current_app
import smtplib
import requests
from email.mime.text import MIMEText

gestionReservaBp = Blueprint("gestionReservaBp", __name__, template_folder='templates')

@gestionReservaBp.route('/')
def gestion_reservas():
    api_rute = current_app.config['API_ROUTE']
    api_url = api_rute + "reservas"
    response = requests.get(api_url)
    if response.status_code == 200:
        reservas = response.json().get("reservas", [])
        return render_template('gestion_reservas.html', reservas=reservas)
    else:
        return jsonify({"message": "Error al obtener las reservas"}), 500