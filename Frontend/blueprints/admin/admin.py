from flask import Blueprint, render_template, current_app, request
import requests


adminBp = Blueprint("adminBp", __name__, template_folder='templates')

@adminBp.route('/', methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        data = {
            'email': request.form['email'],
            'password': request.form['password']
        }
        api_ruta = current_app.config['API_ROUTE']
        api_url = api_ruta + "users/validar_credenciales" # Endpoint de la API para el login de admin
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(api_url, json=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get("success"):
                    rol = response_data.get("rol")
                    if rol == "admin":
                        resp = make_response(redirect(url_for('panel_admin')))
                        resp.set_cookie('rol', 'admin')
                        return resp
                    else:
                        flash("Su usuario no tiene permisos para acceder a la administración.")
                else:
                    flash("Credenciales incorrectas. Por favor, inténtelo de nuevo.")
            elif response.status_code == 401:
                flash("Credenciales incorrectas. Por favor, inténtelo de nuevo.")
            elif response.status_code == 404:
                flash("Usuario no encontrado.")
            else:
                flash("Error al iniciar sesión. Intentelo nuevamente")

        except requests.exceptions.RequestException as e:
            flash("Error del servidor al iniciar sesión. Intentelo nuevamente")
    
    # Verificar si el usuario ya está autenticado como admin
    rol = request.cookies.get('rol')
    if rol == 'admin':
        return redirect(url_for('panel_admin'))
    
    return render_template('admin.html')

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