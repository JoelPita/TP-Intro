from flask import Blueprint, jsonify, request, render_template, url_for, redirect
import smtplib
import requests
from email.mime.text import MIMEText

gestionReservaBp = Blueprint("gestionReservaBp", __name__, template_folder='templates')

@gestionReservaBp.route('/')
def gestion_reservas():
    api_url = "http://127.0.0.1:5000/reservas"
    response = requests.get(api_url)
    if response.status_code == 200:
        reservas = response.json().get("reservas", [])
        return render_template('gestion_reservas.html', reservas=reservas)
    else:
        return jsonify({"message": "Error al obtener las reservas"}), 500