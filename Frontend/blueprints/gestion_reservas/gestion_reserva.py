from flask import Blueprint, jsonify, request, render_template, url_for, redirect
from utils import api_URL
import requests

gestionReservaBp = Blueprint("gestionReservaBp", __name__, template_folder='templates')

@gestionReservaBp.route('/')
def gestion_reservas():
    api_url = api_URL('reservas')
    response = requests.get(api_url)
    if response.status_code == 200:
        reservas = response.json().get("reservas", [])
        print(f"P R I N TTTTTT>>>>>>>{reservas}")
        return render_template('gestion_reservas.html', reservas=reservas)
    else:
        return jsonify({"message": "Error al obtener las reservas"}), 500