from flask import Blueprint, render_template, current_app
import requests


adminBp = Blueprint("adminBp", __name__, template_folder='templates')

@adminBp.route('/reviews', methods=["GET"])
def admin_reviews():
    try:
        # Obtengo las reviews desde la API
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "reviews"
        response = requests.get(api_url)
        my_reviews = response.json()
        return render_template('admin_reviews.html', reviews=my_reviews)
    except requests.exceptions.RequestException as e:
        return render_template('admin_reviews.html', reviews=[])