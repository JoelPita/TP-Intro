from flask import Blueprint, render_template, current_app
import random
import requests

# Crear el blueprint
indexBp = Blueprint('indexBp', __name__)

@indexBp.route('/', methods = ['GET'])
def home():
    reviews = get_random_reviews()
    return render_template('index.html', reviews=reviews)

#Le pido 3 reviews al azar, principalmente las favoritas, sino cualquiera visible.
def get_random_reviews(limit=7):
    try:
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "reviews/visible"
        response = requests.get(api_url)
        response.raise_for_status()  # Verifica si la solicitud fue exitosa
        reviews = response.json()

        # Filtra las reseñas favoritas y las comunes para mostrar
        favorite_reviews = [review for review in reviews if review['estado'] == 'favorita']
        other_reviews = [review for review in reviews if review['estado'] != 'favorita']

        # Selecciona reseñas favoritas al azar
        if len(favorite_reviews) >= limit:
            selected_reviews = random.sample(favorite_reviews, limit)
        else:
            # Asegurar de que hay suficientes reseñas en 'other_reviews' antes de tomar una muestra
            if len(other_reviews) >= (limit - len(favorite_reviews)):
                selected_reviews = favorite_reviews + random.sample(other_reviews, limit - len(favorite_reviews))
            else:
                # Si no hay suficientes reseñas, simplemente devuelve las favoritas y lo que haya en 'other_reviews'
                selected_reviews = favorite_reviews + other_reviews
        
        return selected_reviews
    except requests.RequestException as e:
        print(f"Error fetching reviews: {e}")
        return []

