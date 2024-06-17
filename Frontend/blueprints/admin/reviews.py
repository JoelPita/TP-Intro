from flask import Blueprint, render_template, jsonify, request
from utils import api_URL
import requests

admin_reviewsBp = Blueprint("admin_reviewsBp", __name__, template_folder='templates')

@admin_reviewsBp.route('/', methods=['GET'])
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